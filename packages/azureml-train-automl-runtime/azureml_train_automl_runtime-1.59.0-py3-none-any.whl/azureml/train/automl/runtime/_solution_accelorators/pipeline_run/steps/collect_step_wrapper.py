# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, Dict, Optional, List
import json
import logging
import os
import shutil

import pandas as pd

from azureml.core import Run
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.shared._diagnostics.automl_error_definitions import HierarchyAllParallelRunsFailedByUserError
from azureml.automl.core.shared.exceptions import UserException
from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared.constants import TimeSeriesInternal

from .setup_step_wrapper import SetupStepWrapper
from .automl_inference_driver import AutoMLPRSInferenceDriver
from ..automl_python_step_wrapper import AutoMLPythonStepWrapper
from ..automl_prs_driver_base import AutoMLPRSDriverBase
from ...constants import PipelineConstants
from ...utilities.json_serializer import HTSRuntimeDecoder
from ...utilities import file_utilities as fu
from ...utilities import logging_utilities as lu
from ...data_models.status_record import StatusRecord
from ...data_models.evaluation_configs import EvaluationConfigs
from ...utilities.events.collect_step_events import (
    CollectStart,
    CollectEnd,
    DumpDataStart,
    DumpDataEnd,
    CheckResultsStart,
    CheckResultsEnd
)
from azureml.training.tabular.models.forecasting_pipeline_wrapper import ForecastingPipelineWrapper
from azureml.train.automl.constants import HTSConstants


logger = logging.getLogger(__name__)


class CollectStepWrapper(AutoMLPythonStepWrapper):
    """The wrapper code for proportions calculation runs."""
    FILE_RUN_INFO_JSON = "run_info.json"
    DIR_RAW_FORECAST = "raw_forecast"
    FILE_PREDICTION_PARQUET = "automl_raw_prediction.parquet"
    FILE_PREDICTION_CSV = "automl_raw_prediction.csv"
    FILE_PREDICTION_JSONL = "automl_predict.jsonl"

    def __init__(
            self, name: str, current_step_run: Optional[Run] = None, is_train: bool = True, **kwargs: Any
    ) -> None:
        """
        The wrapper code for proportions calculation runs.

        :param current_step_run: The current step run.
        """
        super().__init__(name, current_step_run, **kwargs)
        self.input_prs_metadata = self.arguments_dict[PipelineConstants.ARG_INPUT_METADATA]
        self.input_setup_metadata = self.arguments_dict[PipelineConstants.ARG_SETUP_METADATA]
        self.output_metadata = self.arguments_dict[PipelineConstants.ARG_OUTPUT_METADATA]
        self._is_train = is_train
        self.inference_configs = SetupStepWrapper._get_inference_configs_from_metadata_dir(
            self.input_setup_metadata)
        if not is_train:
            self.predict_folder = self.arguments_dict[PipelineConstants.ARG_INPUT_PREDICT]
            self._skip_concat_df = self.inference_configs.skip_concat_results
            self._output_evaluation_configs = self.arguments_dict[PipelineConstants.ARG_OUTPUT_EVALUATION_CONFIGS]
            self._output_evaluation_data = self.arguments_dict[PipelineConstants.ARG_OUTPUT_EVALUTAION_DATA]
        else:
            # train will not use this folder
            self.predict_folder = self.output_metadata
            self._skip_concat_df = False
            # placeholder, this parameter won't be used in training.
            self._output_evaluation_configs = os.path.join(".", "output_evaluation_configs")
            self._output_evaluation_data = os.path.join(".", "output_evaluation_data")
        self._predict_df = None
        self.all_metadata: Dict[str, Any] = {}
        os.makedirs(self.output_metadata, exist_ok=True)

    def _run(self) -> None:
        """Run code for the collect step driver."""
        parent_run = self.get_pipeline_run(self.step_run)
        self._collect()
        self._save_metadata(parent_run)
        self._check_results()

    @lu.event_log_wrapped(CollectStart(), CollectEnd())
    def _collect(self) -> None:
        self._print("Start collect step now.")
        for data_file in os.listdir(self.input_prs_metadata):
            file_type = self.get_intermediate_file_postfix(data_file)
            if file_type is None:
                continue
            if file_type not in self.all_metadata:
                self.all_metadata[file_type] = []
            self.all_metadata[file_type].append(
                self.deserialize_metadata_file(os.path.join(self.input_prs_metadata, data_file)))
        if not self._is_train:
            self._collect_prediction()

    def _collect_prediction(self) -> None:
        if self._skip_concat_df:
            self._predict_df = pd.DataFrame()
            return
        dfs = []
        for f in os.listdir(self.predict_folder):
            self._print("processing predict file name {}".format(f))
            f_path = os.path.join(self.predict_folder, f)
            if os.path.getsize(f_path) > 0:
                dfs.append(pd.read_parquet(f_path))
            else:
                logger.warning(f"The file {f} is empty.")
        self._predict_df = pd.concat(dfs)

    @lu.event_log_wrapped(DumpDataStart(), DumpDataEnd())
    def _save_metadata(self, parent_run: Run) -> None:
        self._print("Start saving metadata now.")
        for k, v in self.get_dump_files_dict().items():
            self._print("The file dict key is {} and value is {}.".format(k, v))
            if k in self.all_metadata:
                logger.info("{} founded in the output metadata.".format(k))
                fu.dump_object_to_json(self.all_metadata[k], os.path.join(self.output_metadata, v))
                fu.upload_object_to_artifact_json_file(self.all_metadata[k], v, parent_run, self.local_mode)
        for f in self._get_copy_files():
            self._print("Copy file {}".format(f))
            shutil.copyfile(
                os.path.join(self.arguments_dict[PipelineConstants.ARG_SETUP_METADATA], f),
                os.path.join(self.arguments_dict[PipelineConstants.ARG_OUTPUT_METADATA], f))
            parent_run.upload_file(f, os.path.join(self.arguments_dict[PipelineConstants.ARG_OUTPUT_METADATA], f))
        if not self._is_train:
            self._save_metadata_prediction()

    def _save_metadata_prediction(self) -> None:
        eval_configs = self._rebuild_evaluation_configs()
        if self._predict_df is not None:
            self._print("Writing raw prediction dataframe {} with columns {}.".format(
                self._predict_df, self._predict_df.columns))
            self._predict_df.to_csv(os.path.join(self.output_metadata, self.FILE_PREDICTION_CSV), index=False)
            self._save_eval_data_file(eval_configs)
        else:
            self._print("Predict_df is None, skipping now...")
        if not self._skip_concat_df:
            _raw_forecast = os.path.join(self.output_metadata, self.DIR_RAW_FORECAST)
            os.makedirs(_raw_forecast, exist_ok=True)
            for f in os.listdir(self.predict_folder):
                # copy all the raw forecasts to output folder
                shutil.copyfile(os.path.join(self.predict_folder, f), os.path.join(_raw_forecast, f))
        fu.dump_object_to_json(eval_configs, self._output_evaluation_configs)

    def _save_eval_data_file(self, eval_configs: EvaluationConfigs) -> None:
        eval_df = self._get_eval_df(eval_configs)
        with open(self._output_evaluation_data, "w") as f:
            f.write(eval_df.to_json(orient='records', lines=True))

    def _get_eval_df(self, eval_configs: EvaluationConfigs) -> pd.DataFrame:
        cols = eval_configs.get_all_columns()
        self._print("All cols needed in eval configs are {}".format(cols))
        if not cols:
            return pd.DataFrame()
        all_cols = [col for col in cols]
        found_cols = []
        if self.inference_configs.forecast_quantiles:
            for q in self.inference_configs.forecast_quantiles:
                col = AutoMLPRSInferenceDriver.generate_quantile_forecast_column_name(q)
                if col not in all_cols:
                    all_cols.append(col)
        for col in all_cols:
            if col not in self.result_df.columns:
                self._print("The eval column {} is not found in the predictions.".format(col))
            else:
                found_cols.append(col)
        self._print("The final columns to be saved are {}".format(found_cols))
        eval_df = self.result_df[found_cols]
        self._print(eval_df.columns)
        return eval_df

    @property
    def result_df(self) -> pd.DataFrame:
        """The dataframe that contains the final results."""
        return self._predict_df

    def _rebuild_evaluation_configs(self) -> EvaluationConfigs:
        """Build evaluation configs by combining part from train and inference."""
        evaluation_configs = SetupStepWrapper._get_evaluation_configs_from_metadata_dir(self.input_setup_metadata)
        evaluation_configs.predictions_column_name = HTSConstants.PREDICTION_COLUMN
        if self.inference_configs.forecast_mode == TimeSeriesInternal.ROLLING:
            evaluation_configs.predictions_column_name = HTSConstants.PREDICTION_COLUMN
            evaluation_configs.ground_truths_column_name = HTSConstants.ACTUAL_COLUMN
            evaluation_configs.horizon_origin_column = AutoMLPRSInferenceDriver.FORECAST_ORIGIN_COLUMN
        if self.inference_configs.forecast_quantiles:
            evaluation_configs.predictions_column_name = \
                AutoMLPRSInferenceDriver.generate_quantile_forecast_column_name(0.5)
        return evaluation_configs

    @lu.event_log_wrapped(CheckResultsStart(), CheckResultsEnd())
    def _check_results(self) -> None:
        self._check_parallel_runs_status()

    def _check_parallel_runs_status(self) -> None:
        """Check the results of all parallel runs."""
        status_records = self.all_metadata[AutoMLPRSDriverBase.FILE_POSTFIX_RUN_INFO_JSON]
        Contract.assert_true(
            status_records is not None and len(status_records) > 0, message="Status records should not be empty.",
            reference_code=ReferenceCodes._HTS_RUNTIME_EMPTY_STATUS_RECORDS, log_safe=True)
        fail_count = 0
        for record in status_records:
            if record.status == StatusRecord.FAILED:
                self._print(
                    "Predictions with data: {} failed with exception: {}".format(record.data, record.error_message)
                )
                logger.warning(
                    "Failed prediction record found."
                )
                fail_count += 1
        if fail_count:
            self.step_run._client.run.post_event_warning(
                "Run",
                "{} group(s) failed during prediction. Forecasts may not be coherent."
                " Check {} for detailed failures.".format(fail_count, CollectStepWrapper.FILE_RUN_INFO_JSON)
            )
        if all([sr.status == StatusRecord.FAILED for sr in status_records]):
            Contract.assert_true(
                all([sr.error_type == StatusRecord.USER_ERROR for sr in status_records]),
                message="Status records should not contain system errors.", log_safe=True,
                reference_code=ReferenceCodes._HTS_RUNTIME_STATUS_RECORDS_SYSTEM_ERROR
            )
            raise UserException._with_error(
                AzureMLError.create(
                    HierarchyAllParallelRunsFailedByUserError,
                    target="status_record", parallel_step=self.step_name, file_name=self.FILE_RUN_INFO_JSON,
                    reference_code=ReferenceCodes._HTS_RUNTIME_STATUS_RECORDS_USER_ERROR
                )
            )

    @staticmethod
    def get_intermediate_file_postfix(filename: str) -> Optional[str]:
        """
        Getting the hts related file postfix from a file name.

        :param filename: A file name.
        :return: The postfix that solution accelerator can process.
        """
        postfix = None
        if filename.endswith(AutoMLPRSDriverBase.FILE_POSTFIX_RUN_INFO_JSON):
            postfix = AutoMLPRSDriverBase.FILE_POSTFIX_RUN_INFO_JSON
        else:
            print("Unknown file to proceed {}".format(filename))
        return postfix

    def get_dump_files_dict(self) -> Dict[str, str]:
        """Get the files that needs to dump."""
        return {
            AutoMLPRSDriverBase.FILE_POSTFIX_RUN_INFO_JSON: CollectStepWrapper.FILE_RUN_INFO_JSON
        }

    def _get_copy_files(self) -> List[str]:
        if self._is_train:
            return [
                SetupStepWrapper.FILE_DATASET_INFO, self.FILE_CONFIGS, SetupStepWrapper.FILE_INFERENCE_CONFIGS,
                SetupStepWrapper.FILE_EVALUATION_CONFIGS
            ]
        else:
            return [SetupStepWrapper.FILE_DATASET_INFO]

    def deserialize_metadata_file(self, full_file_path: str) -> Any:
        if full_file_path.endswith(AutoMLPRSDriverBase.FILE_POSTFIX_RUN_INFO_JSON):
            with open(os.path.join(full_file_path)) as f:
                return json.load(f, cls=HTSRuntimeDecoder)
        return None

    @property
    def _sdk_version(self) -> str:
        return PipelineConstants.SDK_V2

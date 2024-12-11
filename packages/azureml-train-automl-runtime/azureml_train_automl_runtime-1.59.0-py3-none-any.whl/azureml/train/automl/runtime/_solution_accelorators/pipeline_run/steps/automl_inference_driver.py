# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import cast, List, Dict, Optional, Any
import joblib
from abc import abstractmethod
import logging
import os
import pandas as pd
import traceback
import uuid

from azureml.core import Run
from azureml.core.model import Model
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.train.automl.constants import InferenceTypes, HTSConstants
from azureml.automl.core.shared.constants import TimeSeriesInternal
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core._logging.event_logger import EventLogger

from ...data_models.arguments import Arguments
from ...data_models.status_record import StatusRecord
from ...utilities.file_utilities import dump_object_to_json
from ...utilities import logging_utilities as lu
from ...utilities.events.automl_prs_inference_events import (
    AutoMLInferenceDriverRunStart,
    AutoMLInferenceDriverRunEnd
)
from ..automl_prs_driver_base import AutoMLPRSDriverBase
from .automl_prs_train_driver import AutoMLPRSTrainDriver


logger = logging.getLogger(__name__)


class AutoMLPRSInferenceDriver(AutoMLPRSDriverBase):
    """PRS inference driver for AutoML solution accelerators."""
    DIR_RAW_FORECASTS = "raw_forecasts"
    DIR_OUTPUT_METADATA = "metadata"
    FILE_RAW_PREDICTIONS = "raw_predictions.parquet"
    POSTFIX_RAW_PREDICTIONS = "_raw_predictions.parquet"
    FORECAST_ORIGIN_COLUMN = "forecast_origin"

    def __init__(
            self,
            current_step_run: Run,
            args: Arguments,
            **kwargs: Any
    ):
        """
        This class is used for doing batch inference.

        :param current_step_run: Current step run object, parent of AutoML run.
        :param args: The arguments for the run.
        """
        super(AutoMLPRSInferenceDriver, self).__init__(current_step_run, **kwargs)
        self._prediction_dir = cast(str, args.target_path)
        self.output_metadata_dir = cast(str, args.output_path)
        self.input_metadata_dir = args.input_metadata
        self.train_run_id = args.train_run_id
        self.train_exp_name = args.train_exp_name
        self.forecast_quantiles = args.forecast_quantiles
        self.inference_type = args.inference_type or InferenceTypes.FORECAST
        self.forecast_mode = args.forecast_mode
        self.partition_column_names = cast(List[str], args.partition_column_names)
        self.allow_multi_partitions = args.allow_multi_partitions
        self.target_column_name = args.target_column_name
        self.step = args.step
        self.status_records: List[StatusRecord] = []
        self.raw_file: Optional[str] = None
        self.event_logger_additional_fields = cast(Dict[str, str], args.event_logger_dim)
        self.event_logger = EventLogger(run=self.current_step_run)
        os.makedirs(self._prediction_dir, exist_ok=True)
        os.makedirs(self.output_metadata_dir, exist_ok=True)

    @lu.event_log_wrapped(AutoMLInferenceDriverRunStart(), AutoMLInferenceDriverRunEnd())
    def run(self, input_data_file: str, output_data_file: str) -> Any:
        print(
            "Running inference driver with partition {} and input data {} and target {}".format(
                self.partition_column_names, input_data_file, self.target_column_name)
        )
        self.raw_file = input_data_file
        forecast_data = self._get_forecast_data(input_data_file)
        results_list = self._do_inference(forecast_data)
        results_list = [r for r in results_list if r is not None]
        if not results_list:
            result_df = self._get_empty_df()
        else:
            result_df = pd.concat(results_list)

        result_df.to_parquet(output_data_file)
        output_file_name = self._get_raw_predict_parquet_file_path(
            self._prediction_dir, os.path.basename(input_data_file)
        )
        print("Writing files to {}".format(output_file_name))
        result_df.to_parquet(output_file_name)
        for sr in self.status_records:
            dump_object_to_json(
                sr, os.path.join(self.output_metadata_dir, self.get_run_info_filename(str(uuid.uuid4()))))
        return result_df

    def _get_forecast_data(self, input_data_file: str) -> pd.DataFrame:
        return self.read_input_data(input_data_file)

    def _do_inference(self, input_data: pd.DataFrame) -> List[pd.DataFrame]:
        dfs = []
        if self.allow_multi_partitions or not self.partition_column_names:
            df = self._do_inference_one_partition(input_data)
            if df is not None:
                dfs.append(df)
        else:
            for _, single_group in input_data.groupby(self.partition_column_names):
                df = self._do_inference_one_partition(single_group)
                if df is not None:
                    print(f"Raw inference df is {df}")
                    dfs.append(df)
        return dfs

    def _post_process_predictions_rolling(
            self, predictions: pd.DataFrame,
            input_data: pd.DataFrame,
            rename_dict: Dict[Any, str]
    ) -> pd.DataFrame:
        return predictions

    def _post_process_predictions_recursive(self, predictions: pd.DataFrame) -> pd.DataFrame:
        return predictions

    def _post_process_predictions_quantiles(
            self, predictions: pd.DataFrame,
            input_data: pd.DataFrame,
            rename_dict: Dict[Any, str]
    ) -> pd.DataFrame:
        return predictions

    def _do_inference_one_partition(self, input_data: pd.DataFrame) -> Optional[pd.DataFrame]:
        print(f"Doing inference on {input_data}.")
        logger.info("Inference one partition data size is {}".format(input_data.shape))
        model = self._get_model(input_data)
        try:
            data_identifier = AutoMLPRSInferenceDriver._get_data_identifier_from_data(
                input_data, self.partition_column_names)
        except Exception as e:
            print("Meeting errors in get data identifier. {}".format(e))
            data_identifier = []
        if model is not None:
            try:
                df = None
                preprocessed_data = self._preprocess_data_one_partition(input_data)
                if self.inference_type == InferenceTypes.FORECAST or self.inference_type is None:
                    df = self._do_inference_one_partition_forecast(preprocessed_data, model)
                elif self.inference_type == InferenceTypes.PREDICT:
                    df = self._do_inference_one_partition_predict(preprocessed_data, model)
                elif self.inference_type == InferenceTypes.PREDICT_PROBA:
                    df = self._do_inference_one_partition_predict_proba(preprocessed_data, model)
                self.status_records.append(
                    StatusRecord(
                        data_identifier,
                        StatusRecord.SUCCEEDED,
                        self.raw_file,
                        AutoMLPRSInferenceDriver.FILE_RAW_PREDICTIONS
                    )
                )
                return df
            except Exception as e:
                print(e)
                traceback.print_exc()
                logging_utilities.log_traceback(e, logger)
                self.status_records.append(
                    StatusRecord(
                        data_identifier,
                        StatusRecord.FAILED,
                        self.raw_file,
                        None,
                        StatusRecord.get_error_type(e),
                        error_message=str(e)
                    )
                )
        else:
            logger.warn("Data not found in graph.")
            self.status_records.append(StatusRecord(
                data_identifier,
                StatusRecord.FAILED,
                self.raw_file,
                None,
                error_type=StatusRecord.USER_ERROR,
                error_message="Data was not seen at training time."
            ))
        return None

    def _do_inference_one_partition_forecast(self, input_data: pd.DataFrame, model: Model) -> pd.DataFrame:
        print(f"Inference partition schema is {input_data.columns}")
        if self.target_column_name in input_data.columns:
            print(f"Popping target cols {self.target_column_name}")
            y_test = input_data.pop(self.target_column_name).to_numpy()
        else:
            y_test = None
        X_test = input_data
        print(f"ytest: {y_test}")
        if self.forecast_quantiles:
            Contract.assert_true(
                hasattr(model, 'forecast_quantiles'),
                message=f"model {type(model).__name__} doesn't expose forecast_quantiles method",
                log_safe=True)
            self._console_writer.println('Inference using forecast quantiles')
            model.quantiles = self.forecast_quantiles
            prediction_results = model.forecast_quantiles(X_test, y_test, ignore_data_errors=True)
            rename_dict = {q: self.generate_quantile_forecast_column_name(q) for q in model.quantiles}
            prediction_results.rename(columns=rename_dict, inplace=True)
            prediction_results = self._post_process_predictions_quantiles(
                prediction_results, input_data, rename_dict)
        else:
            Contract.assert_true(
                hasattr(model, 'forecast'),
                message=f"model {type(model).__name__} doesn't expose forecast method",
                log_safe=True)
            if self.forecast_mode == TimeSeriesInternal.ROLLING:
                self._console_writer.println('Inference using rolling forecast')
                prediction_results = model.rolling_forecast(X_test, y_test, self.step, ignore_data_errors=True)
                rename_dict = {model.forecast_origin_column_name: AutoMLPRSInferenceDriver.FORECAST_ORIGIN_COLUMN,
                               model.actual_column_name: HTSConstants.ACTUAL_COLUMN,
                               model.forecast_column_name: HTSConstants.PREDICTION_COLUMN}
                prediction_results.rename(columns=rename_dict, inplace=True)
                prediction_results = self._post_process_predictions_rolling(
                    prediction_results, input_data, rename_dict)
            else:
                self._console_writer.println('Inference using recursive forecast')
                y_predictions, X_trans = model.forecast(X_test, y_test, ignore_data_errors=True)
                # Insert predictions to test set
                predictions = input_data
                predictions[HTSConstants.PREDICTION_COLUMN] = y_predictions
                prediction_results = self._post_process_predictions_recursive(predictions)
        return prediction_results

    def _do_inference_one_partition_predict(self, input_data: pd.DataFrame, model: Model) -> pd.DataFrame:
        Contract.assert_true(
            hasattr(model, 'predict'),
            message=f"model {type(model).__name__} doesn't expose predict method",
            log_safe=True)
        self._console_writer.println('Inference using predict')
        y_predictions = model.predict(input_data)
        input_data[HTSConstants.PREDICTION_COLUMN] = y_predictions
        return input_data

    def _do_inference_one_partition_predict_proba(self, input_data: pd.DataFrame, model: Model) -> pd.DataFrame:
        Contract.assert_true(
            hasattr(model, 'predict_proba'),
            message=f"model {type(model).__name__} doesn't expose predict_proba method",
            log_safe=True)
        self._console_writer.println('Inference using predict_proba')
        y_pred_proba = model.predict_proba(input_data)
        if not isinstance(y_pred_proba, pd.DataFrame):
            y_pred_proba = pd.DataFrame(
                y_pred_proba,
                columns=[
                    f"{HTSConstants.PREDICTION_COLUMN}_{x}" for x in range(y_pred_proba.shape[1])])
        predicted_results = pd.concat([input_data, y_pred_proba], axis=1)
        return predicted_results

    def _get_model(self, df: pd.DataFrame) -> Optional[Model]:
        workspace = self.current_step_run.experiment.workspace
        model_name = AutoMLPRSDriverBase.get_model_name_from_df(df, self.partition_column_names, self.run_type)
        model_tags = []
        if self.train_run_id:
            model_tags.append([AutoMLPRSTrainDriver.MODEL_TAG_DICT_RUN_ID, self.train_run_id])
        if self.train_exp_name:
            model_tags.append([AutoMLPRSTrainDriver.MODEL_TAG_DICT_EXP_NAME, self.train_exp_name])
        self._console_writer.println('query the model {} with tags {}'.format(model_name, model_tags))
        model_list = Model.list(workspace, name=model_name,
                                tags=model_tags, latest=True)

        if not model_list:
            self._console_writer.println("Could not find model")
            return None
        self._console_writer.println(f'Got {len(model_list)} models')
        model_path = model_list[0].download(exist_ok=True)
        model = joblib.load(model_path)
        model_name = model_list[0].name
        self._console_writer.println(f'Unpickled the model {model_name}')
        return model

    def _get_empty_df(self) -> pd.DataFrame:
        return pd.DataFrame(columns=self.partition_column_names)

    @staticmethod
    def _get_raw_predict_parquet_file_path(raw_predict_dir: str, basename: str) -> str:
        return os.path.join(raw_predict_dir, "{}{}".format(
            basename.split(".")[0], AutoMLPRSInferenceDriver.POSTFIX_RAW_PREDICTIONS))

    @staticmethod
    def generate_quantile_forecast_column_name(quantile: float) -> str:
        """Generate a column name for quantile forecast from the quantile value."""
        return f'{HTSConstants.PREDICTION_COLUMN}_{str(quantile)}'

    def _preprocess_data_one_partition(self, df: pd.DataFrame) -> pd.DataFrame:
        return df

    @property
    @abstractmethod
    def run_type(self) -> str:
        """The run type of the wrapper."""
        raise NotImplementedError

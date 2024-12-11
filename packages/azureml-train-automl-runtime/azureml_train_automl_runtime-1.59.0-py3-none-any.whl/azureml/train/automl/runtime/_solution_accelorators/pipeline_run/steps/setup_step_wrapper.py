# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
Wrapper file for solution accelerators
"""
import copy
import json
import logging
import os
import shutil
import sys
import time
import uuid
import warnings
from abc import abstractmethod
from typing import Any, Dict, Optional, cast, List

import pandas as pd
from azureml.automl.core.forecasting_parameters import ForecastingParameters
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    ArgumentOutOfRange,
    ArgumentBlankOrEmpty,
    InvalidArgumentType,
    InvalidInputDatatype,
    InputDatasetEmpty,
    MissingColumnsInData,
    HierarchyNoTrainingRun,
    ConflictingTimeoutError,
    ConflictingValueForArguments
)
from azureml.automl.core.shared._diagnostics.automl_error_definitions import ExecutionFailure
from azureml.automl.core.shared.exceptions import (
    ConfigException,
    DataException,
    ConflictingTimeoutException,
    ValidationException
)
from azureml.automl.core.shared.reference_codes import ReferenceCodes

from azureml._common._error_definition import AzureMLError
from azureml._restclient.constants import RunStatus
from azureml._restclient.jasmine_client import JasmineClient
from azureml.automl.core.console_writer import ConsoleWriter
from azureml.automl.runtime.featurizer.transformer.timeseries._validation._timeseries_validation_common \
    import check_memory_limit_by_file_size
from azureml.automl.runtime.shared import memory_utilities
from azureml.core import Run, Experiment
from ..automl_pipeline_step_wrapper_base import AutoMLPipelineStepWrapperBase
from ..automl_python_step_wrapper import AutoMLPythonStepWrapper
from ...constants import PipelineConstants, HTSConstants
from ...data_models.inference_configs import InferenceConfigs
from ...data_models.raw_data_info import RawDataInfo
from ...data_models.evaluation_configs import EvaluationConfigs
from ...utilities import logging_utilities as lu
from ...utilities import run_utilities as ru
from ...utilities.events.partition_events import (
    PartitionStart,
    PartitionEnd
)
from ...utilities.events.setup_events import (
    SetupStart,
    SetupEnd,
    ValidationStart,
    ValidationEnd
)
from ...utilities.file_utilities import (
    dump_object_to_json,
    is_supported_data_file
)
from ...utilities.json_serializer import HTSRuntimeDecoder

logger = logging.getLogger(__name__)
console_writer = ConsoleWriter(sys.stdout)


class SetupStepWrapper(AutoMLPythonStepWrapper):
    """Setup step wrapper for solution accelerators."""
    FILE_DATASET_INFO = "dataset_info.json"
    FILE_INFERENCE_CONFIGS = "inference_configs.json"
    FILE_EVALUATION_CONFIGS = "evaluation_configs.json"

    def __init__(
            self,
            step_name: str,
            current_step_run: Optional[Run] = None,
            is_train: bool = True,
            **kwargs: Any
    ) -> None:
        """
        Setup step wrapper for solution accelerators.

        :param step_name: The step name.
        :param current_step_run: The current step run object.
        """
        super().__init__(step_name, current_step_run, **kwargs)
        logger.info("[{} step] starts to get settings now.".format(self.step_name))
        self.arguments_dict = self._remove_default_inputs_from_arguments_dict(self.arguments_dict)
        self._train_metadata_path = self.arguments_dict.get(PipelineConstants.ARG_TRAIN_METADATA)
        self.is_train = is_train
        self._allow_multi_partitions = False
        self.inference_configs = self._get_inference_configs()
        self.raw_data = self.arguments_dict[PipelineConstants.ARG_RAW_DATA]
        self.raw_data_columns = self._get_raw_data_columns()

        self.settings: Dict[str, Any] = {}
        self.forecasting_parameters = ForecastingParameters(validate_parameters=False)
        if is_train:
            config_path = self.arguments_dict[PipelineConstants.ARG_INPUT_CONFIG]
            self.settings = ru.get_settings(config_path)
            if self._is_forecasting_tasks():
                self.forecasting_parameters = ru.get_forecasting_parameters(self.settings)

        self.dataset_info_path = self.arguments_dict[PipelineConstants.ARG_OUTPUT_METADATA]
        self.preprocessed_data_path = self.arguments_dict[PipelineConstants.ARG_PROCESSED_DATA]
        self.custom_dim = lu.get_additional_logging_custom_dim(self.step_name)
        lu.update_log_custom_dimension(self.custom_dim)
        self.event_logger_additional_fields = lu.get_event_logger_additional_fields(
            self.custom_dim, self.step_run.parent.id)
        self.all_files = self._get_all_files(self.raw_data)
        self._partition_files_dict: Dict[str, str] = {}
        self._collect_files_dict: Dict[str, List[str]] = {}
        self._uri_file_df_unique = True
        self._total_size = 0
        self._fail_early = self._get_default_bool_from_arg_dict(PipelineConstants.ARG_VALIDATION_FAIL_EARLY, True)
        self._label_column_name = ru.get_label_column_name(self.settings)
        self._skip_data_access = self._get_default_bool_from_arg_dict(
            PipelineConstants.ARG_INTERNAL_SKIP_DATA_ACCESS, False)
        os.makedirs(self.dataset_info_path, exist_ok=True)
        os.makedirs(self.preprocessed_data_path, exist_ok=True)

    @lu.event_log_wrapped(SetupStart(), SetupEnd())
    def _run(self):
        """The run methods."""
        self.event_logger.log_event(SetupStart(self.event_logger_additional_fields))

        self.validation()
        self.partition_dataset()
        self.save_meta_data()

        self.event_logger.log_event(SetupEnd(self.event_logger_additional_fields))

    # region Validations
    @lu.event_log_wrapped(ValidationStart(), ValidationEnd())
    def validation(self):
        """Validate if the solution accelerators can run successfully."""
        self._validate_settings()
        if self._is_mltable(self.raw_data):
            logger.info("Using MLTable")
            raise ConfigException._with_error(
                AzureMLError.create(
                    InvalidArgumentType,
                    argument="raw_data", actual_type="mltable", expected_types="uri_folder"
                )
            )
        else:
            logger.info("Using URIFolder with {}.".format(self._fail_early))
            if self._fail_early:
                self._print("Validate uri folder now")
                self._validate_uri_folder()

    def _get_raw_data_info(self) -> RawDataInfo:
        return RawDataInfo(
            data_type="mltable" if self._is_mltable(self.raw_data) else "uri_folder",
            data_size_in_bytes=sum([os.path.getsize(f) for f in self.all_files]),
            is_partition_needed=self.is_partition_needed(),
            number_of_files=len(self.all_files)
        )

    def _validate_uri_folder(self):
        SetupStepWrapper._check_mounted_file_dataset(self.raw_data)
        total_files = len(self.all_files)
        logger.info("Found {} files in the input dataset.".format(total_files))
        SetupStepWrapper.check_valid_file_type(self.all_files)

        file_count = 0
        for f in self.all_files:
            file_count += 1
            if is_supported_data_file(f):
                self._print(
                    "Supported file {}, processing now.  completed {}/{} files".format(f, file_count, total_files))
                df = self.load_data_from_file(f)
                logger.info("The input size is {} and data file size is {}".format(
                    df.shape, os.path.getsize(f)
                ))
                ru.validate_column_consistent(self.raw_data_columns, list(df.columns), "file {}".format(f))
                if self.partition_columns:
                    self._uri_file_df_unique &= self._is_df_uniqueness(df)
                    partition_values = self._get_df_first_row_partition_value_str(df)
                else:
                    partition_values = HTSConstants.HTS_ROOT_NODE_LEVEL
                if not self.allow_multi_partitions:
                    if partition_values not in self._partition_files_dict:
                        self._partition_files_dict[partition_values] = str(uuid.uuid4())
                    new_file_name = self._partition_files_dict[partition_values]
                    if new_file_name not in self._collect_files_dict:
                        self._collect_files_dict[new_file_name] = []
                    self._collect_files_dict[new_file_name].append(f)
                    self._total_size += memory_utilities.get_data_memory_size(df)
            else:
                self._print("Unsupported file {}, ignoring it now.".format(f))
                logger.info("Met unsupported file.")

    @staticmethod
    def _get_new_file_name(file_name_with_extension: str, counter: int) -> str:
        file_name, extension = os.path.splitext(file_name_with_extension)
        return "{}_{}.{}".format(file_name, counter, extension)

    def _is_df_uniqueness(self, df: pd.DataFrame) -> bool:
        """
        Validate the dataframe contains unique values for the training level of a graph.

        :param df: The input dataframe.
        :return: None
        """
        grouped_df = df.groupby(self.partition_columns).size().reset_index(name='number_of_rows')
        if grouped_df.shape[0] > 1:
            self._print("Multi grains in one partition detected {}".format(grouped_df))
            logger.warning("Multi grains in one partition detected.")
        return not (grouped_df.shape[0] > 1)

    def _validate_settings(self):
        if self.is_train:
            ru.get_automl_settings(self.settings, self.additional_params)
            if self._is_forecasting_tasks():
                ru.validate_forecasting_settings(
                    self.forecasting_parameters, self._label_column_name, self.raw_data_columns
                )
            self._check_additional_params()
        else:
            self._validate_inference_settings()
        if not self._fail_early and not self.allow_multi_partitions:
            self._print(
                f"early_validation_failure {self._fail_early} and allow_multi_partitions "
                f"{self.allow_multi_partitions}")
            raise ConfigException._with_error(
                AzureMLError.create(
                    ConflictingValueForArguments,
                    arguments="early_validation_failure can only be set to False while enabling allow_multi_partitions"
                )
            )
        self._validate_prs_settings()
        if not isinstance(self.partition_columns, list):
            raise ConfigException._with_error(
                AzureMLError.create(
                    InvalidArgumentType,
                    argument="partition_columns", actual_type=str(type(self.partition_columns)),
                    expected_types="list of str"
                )
            )

    def _check_additional_params(self):
        for param in self.additional_params:
            if not self.settings.get(param, None):
                raise ConfigException._with_error(
                    AzureMLError.create(
                        ArgumentBlankOrEmpty,
                        argument_name=",".join(self.additional_params),
                        reference_code=ReferenceCodes._MM_EMPTY_PARAMS
                    )
                )

    def _validate_inference_settings(self):
        for col in self.partition_columns:
            if col not in self.raw_data_columns:
                raise ConfigException._with_error(
                    AzureMLError.create(
                        MissingColumnsInData, target="partition_columns", columns=col,
                        data_object_name="{}".format(self.raw_data_columns),
                        reference_code=ReferenceCodes._MANY_MODELS_MISSING_INF_COL))
        self.inference_configs.check_settings()

    def _validate_prs_settings(self) -> None:
        os_cpu_count = os.cpu_count()
        if os_cpu_count is None:
            print("Cannot get cpu count from os.cpu_count(). Using default as 256")
            n_cores = 256
        else:
            n_cores = os_cpu_count
        process_count_per_node = int(self.arguments_dict[PipelineConstants.ARG_NODE_PROCESS_COUNT])
        number_of_processes_per_core = int(process_count_per_node / n_cores)
        if self.is_train:
            experiment = self.step_run.experiment
            jasmine_client = JasmineClient(
                service_context=experiment.workspace.service_context,
                experiment_name=experiment.name,
                experiment_id=experiment.id)
            node_count = int(self.arguments_dict[PipelineConstants.ARG_NODES_COUNT])
            max_concurrent_runs = node_count * process_count_per_node
            validation_output = jasmine_client.validate_many_models_run_input(
                max_concurrent_runs=max_concurrent_runs,
                automl_settings=json.dumps(self.settings),
                number_of_processes_per_core=number_of_processes_per_core)
            validation_results = validation_output.response
            if not validation_output.is_valid and any([d.code != "UpstreamSystem"
                                                       for d in validation_results.error.details]):
                # If validation service meets error thrown by the upstream service, the run will continue.
                print("The validation results are as follows:")
                errors = []
                for result in validation_results.error.details:
                    if result.code != "UpstreamSystem":
                        print(result.message)
                        errors.append(result.message)
                msg = "Validation error(s): {}".format(validation_results.error.details)
                raise ValidationException._with_error(AzureMLError.create(
                    ExecutionFailure, operation_name="data/settings validation", error_details=msg))
        self._check_processes_per_core(process_count_per_node, n_cores)

    def _check_run_invocation_timeout(self):
        experiment_timeout_hours = self.settings.get('experiment_timeout_hours', 0)
        run_invocation_timeout = self.arguments_dict.get(PipelineConstants.ARG_PRS_STEP_TIMEOUT, 0)

        # PRS requires additional buffer to complete after experiment has completed or timed out
        if run_invocation_timeout < experiment_timeout_hours * 60 * 60 + 300:
            raise ConflictingTimeoutException._with_error(
                AzureMLError.create(
                    ConflictingTimeoutError,
                    reference_code=ReferenceCodes._VALIDATE_CONFLICTING_TIMEOUT,
                    target='run_invocation_timeout'))

    @staticmethod
    def _check_processes_per_core(max_concurrency_per_instance: int, number_of_cores: int) -> None:
        if number_of_cores == 0:
            console_writer.println("{} is 0 trying to use default value".format(number_of_cores))
            number_of_cores = 256
        console_writer.println(
            "The current node has {} cores and the max_concurrency_per_instance settings is {}. "
            "The recommend max_concurrency_per_instance is between {} and {}".format(
                number_of_cores, max_concurrency_per_instance, number_of_cores // 2, number_of_cores))
        process_core_ratio = max_concurrency_per_instance / number_of_cores
        if process_core_ratio > 2 or max_concurrency_per_instance < 1:
            console_writer.println(
                "The max_concurrency_per_instance should be less than 2 times of cores of the node.")
            raise ConfigException._with_error(
                AzureMLError.create(
                    ArgumentOutOfRange, target="number_of_processes_per_core",
                    argument_name="number_of_processes_per_core", min=1, max=2 * number_of_cores,
                    reference_code=ReferenceCodes._MM_TOO_MANY_PROCESSES
                )
            )
        elif process_core_ratio > 1:
            warnings.warn(
                "The max_concurrency_per_instance is larger than number of cores of the node. The pipeline run may "
                "not reach its optimal settings")
        elif process_core_ratio < 0.5:
            warnings.warn(
                "The max_concurrency_per_instance is less than half  of the number of cores of the node. "
                "The compute may not be fully utilized")

    @staticmethod
    def _check_mounted_file_dataset(mounted_path: str) -> None:
        """
        Check if mounted FileDataset path point to a single file. If so, throw DataException.

        :param mounted_path: The mounted FileDataset path.
        """
        if os.path.isfile(mounted_path):
            raise DataException._with_error(
                AzureMLError.create(
                    InvalidInputDatatype,
                    target="input_data",
                    input_type="uri_file",
                    supported_types="uri_folder with multiple .csv or .parquet",
                    reference_code=ReferenceCodes._HTS_INVALID_FILE_DATASET
                )
            )

    @staticmethod
    def check_valid_file_type(files_list: List[str]) -> None:
        """
        Check whether data files used for training have valid type.

        :param files_list: A list of files.
        :raises: DataException
        """
        if all([not is_supported_data_file(f) for f in files_list]):
            raise DataException._with_error(
                AzureMLError.create(
                    InputDatasetEmpty, target="InputDataset",
                    reference_code=ReferenceCodes._HTS_PRE_PROPORTIONS_EMPTY_DATA
                )
            )
    # endregion

    # region Partition
    @lu.event_log_wrapped(PartitionStart(), PartitionEnd())
    def partition_dataset(self):
        """Partition the dataset if needed."""
        if self._skip_data_access:
            self._print("All data access is skipped in the setup step.")
            return
        self._print(
            "Collected data will be written at {}".format(self.preprocessed_data_path))
        os.makedirs(self.preprocessed_data_path, exist_ok=True)
        if self.is_partition_needed():
            self._print("Partition the dataset now.")
            logger.info("Partition the dataset now.")
            self._check_memory_limit()
            df = self._load_data(self.raw_data)
            # if the dataset needs to repartition, then reset the partition files dict
            self._partition_files_dict = {}
            for partition_keys, df in df.groupby(self.partition_columns):
                output_file_name = "{}.parquet".format(uuid.uuid4())
                self._partition_files_dict[str(partition_keys)] = output_file_name
                df.to_parquet(os.path.join(self.preprocessed_data_path, output_file_name))
        elif self.allow_multi_partitions:
            # For the allow_multi_partitions scenario, we will directly copy the data
            self._print("Copy the data now.")
            all_file_names = set()
            for f in self.all_files:
                self._print("Copy {} now.".format(f))
                if is_supported_data_file(f):
                    file_dir, filename = os.path.split(f)
                    new_file_name = filename
                    _, file_ext = os.path.splitext(filename)
                    if new_file_name in all_file_names:
                        new_file_name = "{}{}".format(uuid.uuid4(), file_ext)
                        self._print("Found duplicate file names {}, using new name {}.".format(f, new_file_name))
                    self._collect_files_dict[new_file_name] = [f]
                    new_file_path = os.path.join(self.preprocessed_data_path, filename)
                    shutil.copyfile(f, new_file_path)
        else:
            # if no partition needed, copy the files by collect and write them to disk.
            self._print("Generate the dataset now.")
            logger.info("Generate the collected dataset now.")
            self._generate_collected_files(self.preprocessed_data_path)

    def is_partition_needed(self) -> bool:
        """
        Check if partition step is needed for the input data. For file dataset, this value only be correct after
        running validation.
        """
        if self.allow_multi_partitions:
            # For the scenario that multi partition in one file, we will not do any further partition.
            return False
        return not self._uri_file_df_unique

    def _check_memory_limit(self):
        """Check the memory limit based of the input file sizes."""
        check_memory_limit_by_file_size(self._total_size)

    def _generate_collected_files(self, target_file_path: str) -> None:
        """
        Generate collected data files for each node based on the node_files_list and remove the origin files.

        :param target_file_path: The output file path.
        :return:
        """
        os.makedirs(target_file_path, exist_ok=True)
        self._print("{} files will be generated".format(len(self._collect_files_dict)))
        for new_file_name, file_list in self._collect_files_dict.items():
            self._print("Generating {} from {}".format(new_file_name, file_list))
            file_name = '{}.parquet'.format(new_file_name)
            data_df = None
            for f in file_list:
                temp_df = self.load_data_from_file(f)
                data_df = self.concat_df_with_none(data_df, temp_df)
            if data_df is not None:
                data_df.to_parquet(os.path.join(target_file_path, file_name), index=False)
            else:
                logger.warning("Data df for new_file_name {} is None.".format(new_file_name))
    # endregion

    def _add_properties_for_run(self):
        parent_run = ru.get_pipeline_run(self.step_run)
        parent_run.add_properties({
            PipelineConstants.PROPERTIES_PIPELINE_TYPE: PipelineConstants.PROPERTIES_VALUE_TRAINING
            if self.is_train else PipelineConstants.PROPERTIES_VALUE_INFERENCE,
            PipelineConstants.PROPERTIES_RUN_SETTINGS: json.dumps(self.settings),
            PipelineConstants.PROPERTIES_RUN_TYPE: self.run_type
        })

    def save_meta_data(self):
        """Save the metadata to the output_metadata folder."""
        raw_data_info = self._get_raw_data_info()
        evaluation_configs = self._build_evaluation_configs()
        # dump graph and upload to artifact
        dump_object_to_json(raw_data_info, os.path.join(self.dataset_info_path, SetupStepWrapper.FILE_DATASET_INFO))
        dump_object_to_json(
            evaluation_configs, os.path.join(self.dataset_info_path, SetupStepWrapper.FILE_EVALUATION_CONFIGS))
        dump_object_to_json(
            self._partition_files_dict,
            os.path.join(self.dataset_info_path, PipelineConstants.PREPROCESSED_DATA_INFO))
        dump_object_to_json(
            self._collect_files_dict, os.path.join(self.dataset_info_path, PipelineConstants.COLLECTED_DATA_INFO))
        if self.is_train:
            shutil.copyfile(
                self.arguments_dict[PipelineConstants.ARG_INPUT_CONFIG],
                os.path.join(self.dataset_info_path, AutoMLPipelineStepWrapperBase.FILE_CONFIGS))
            # update inference configs before saving
            self.inference_configs.partition_column_names = self.partition_columns
            self.inference_configs.allow_multi_partitions = self.allow_multi_partitions
            self.inference_configs.target_column_name = self._label_column_name
        dump_object_to_json(
            self.inference_configs,
            self._get_inference_config_file_name(self.dataset_info_path)
        )
        self._add_properties_for_run()

    @staticmethod
    def _is_mltable(input_data: str) -> bool:
        """Check if the input is mltable."""
        return os.path.exists(os.path.join(input_data, "MLTable"))

    @property
    def _upload_file_list(self) -> List[str]:
        return [
            SetupStepWrapper.FILE_DATASET_INFO,
            PipelineConstants.PREPROCESSED_DATA_INFO,
            PipelineConstants.COLLECTED_DATA_INFO]

    @property
    @abstractmethod
    def additional_params(self) -> List[str]:
        """Additional params than the one used in automl settings."""
        raise NotImplementedError

    @property
    @abstractmethod
    def partition_columns(self) -> List[str]:
        """The columns that the dataset needs to be partitioned."""
        raise NotImplementedError()

    @staticmethod
    def _get_all_files(dir_path: str) -> List[str]:
        all_files = []
        for d, _, files in os.walk(dir_path):
            for f in files:
                all_files.append(os.path.join(d, f))
        return all_files

    @staticmethod
    def concat_df_with_none(df: Optional[pd.DataFrame], update_df: pd.DataFrame) -> pd.DataFrame:
        """
        Concat two dataframes. If the first one is None, then return the second one. If not,
        return the concat result of these two dataframe.

        :param df: First pd.DataFrame that can be None.
        :param update_df: Second pd.DataFrame.
        :return: The concat pd.DataFrame of these two.
        """
        if df is None:
            return update_df
        else:
            return pd.concat([df, update_df], ignore_index=True)

    def _load_data(self, raw_data: str, sample_data: Optional[bool] = False) -> pd.DataFrame:
        dfs = []
        all_files = self._get_all_files(raw_data)
        for f in all_files:
            if is_supported_data_file(f):
                df = self.load_data_from_file(f)
                if sample_data:
                    return df
                else:
                    dfs.append(df)
        return pd.concat(dfs)

    @staticmethod
    def load_data_from_file(file_path: str) -> pd.DataFrame:
        """
        Load a csv file or a parquet file into memory as pd.DataFrame

        :param file_path: The file path.
        :return: pd.DataFrame
        """
        file_name_with_extension = os.path.basename(file_path)
        file_name, file_extension = os.path.splitext(file_name_with_extension)
        if file_extension.lower() == ".parquet":
            data = pd.read_parquet(file_path)
        else:
            data = pd.read_csv(file_path)
        return data

    def _get_raw_data_columns(self) -> List[str]:
        # for uri folder, retrieve the columns from the first file.
        for d, _, files in os.walk(self.raw_data):
            for f in files:
                if is_supported_data_file(f):
                    return list(self.load_data_from_file(os.path.join(d, f)).columns)
        return []

    def _get_df_first_row_partition_value_str(self, df: pd.DataFrame) -> str:
        return str(df.head(1)[self.partition_columns].values.tolist()[0])

    @property
    def _sdk_version(self) -> str:
        """The sdk version that running the script."""
        return PipelineConstants.SDK_V2

    @property
    @abstractmethod
    def run_type(self) -> str:
        """The run type."""
        raise NotImplementedError

    def _get_default_bool_from_arg_dict(self, arg_dict_key: str, default_value: bool) -> bool:
        input_val = self.arguments_dict.get(arg_dict_key, default_value)
        if input_val is None:
            return default_value
        return ru.str_or_bool_to_boolean(input_val)

    def _build_evaluation_configs(self) -> EvaluationConfigs:
        if self.is_train:
            return self._build_evaluation_configs_train()
        else:
            # if the train metadata is available, honor that one, if not, try to rebuild the one
            # using existing settings.
            if self._train_metadata_path is not None:
                eval_conf = self._get_evaluation_configs_from_metadata_dir(self._train_metadata_path)
                if self._label_column_name is not None and \
                        eval_conf.ground_truths_column_name != self._label_column_name:
                    self._print(
                        "Found inconsistency in the label column name. For train, the value is {} and for "
                        "inference is {}. We will use the one for inference for evaluation configs.".format(
                            eval_conf.ground_truths_column_name, self._label_column_name
                        ))
                return eval_conf
            else:
                if self._is_forecasting_tasks():
                    if self.settings:
                        self.forecasting_parameters = ru.get_forecasting_parameters(self.settings)
                        return self._build_evaluation_configs_train()
                    else:
                        # no previous settings can be found return empty eval configs as we don't have enough
                        # information to build the configs
                        return EvaluationConfigs()
                return EvaluationConfigs()

    def _build_evaluation_configs_train(self) -> EvaluationConfigs:
        if self._is_forecasting_tasks():
            return EvaluationConfigs.get_evaluation_configs_from_forecasting_parameters(
                fp=self.forecasting_parameters, label_column_name=self._label_column_name,
            )
        return EvaluationConfigs()

    def _is_forecasting_tasks(self) -> bool:
        return self.settings.get("task") == "forecasting" or (self.settings.get("is_timeseries") is True)

    # region Inference Utilities
    def _get_inference_configs(self) -> InferenceConfigs:
        if self.is_train:
            # for training run, return an empty inference configs with known settings, partition columns and
            # label columns will be updated before saving it.
            return InferenceConfigs(
                train_run_id=self.get_pipeline_run(self.step_run).id,
                train_experiment_name=self.step_run.experiment.name
            )
        else:
            partition_column_names = self.arguments_dict.get(PipelineConstants.ARG_PARTITION_COLUMN_NAMES)
            train_run_id = self.arguments_dict.get(PipelineConstants.ARG_TRAIN_RUN_ID)
            train_experiment_name = self.arguments_dict.get(PipelineConstants.ARG_EXPERIMENT_NAME)
            target_column_name = self.arguments_dict.get(PipelineConstants.ARG_TARGET_COLUMN_NAME)
            if self._train_metadata_path is not None:
                train_inference_configs = SetupStepWrapper._get_inference_configs_from_metadata_dir(
                    self._train_metadata_path
                )
                warn_msg = "The input {} is not the same as the parameters from train metadata. " \
                           "We will use the input one {}."
                if train_run_id is None:
                    train_run_id = train_inference_configs.train_run_id
                elif train_run_id != train_inference_configs.train_run_id:
                    self._print(warn_msg.format("train_run_id", train_run_id))
                if train_experiment_name is None:
                    train_experiment_name = train_inference_configs.train_experiment_name
                elif train_experiment_name != train_inference_configs.train_experiment_name:
                    self._print(warn_msg.format("train_experiment_name", train_experiment_name))
                if partition_column_names is None:
                    partition_column_names = train_inference_configs.partition_column_names
                elif train_inference_configs.partition_column_names != partition_column_names:
                    self._print(warn_msg.format("partition_column_names", partition_column_names))
                if target_column_name is None:
                    target_column_name = train_inference_configs.target_column_name
                elif target_column_name != train_inference_configs.target_column_name:
                    self._print(warn_msg.format("target_column_name", target_column_name))
            forecast_step_input = self.arguments_dict.get(PipelineConstants.ARG_FORECAST_STEP)
            forecast_step = int(forecast_step_input) if forecast_step_input else 1
            ic = InferenceConfigs(
                partition_column_names=partition_column_names,
                forecast_mode=self.arguments_dict.get(PipelineConstants.ARG_FORECAST_MODE),
                inference_type=self.arguments_dict.get(PipelineConstants.ARG_INFERENCE_TYPE),
                forecast_quantiles=self.arguments_dict.get(PipelineConstants.ARG_FORECAST_QUANTILES),
                allocation_method=self.arguments_dict.get(PipelineConstants.ARG_ALLOCATION_METHOD),
                forecast_level=self.arguments_dict.get(PipelineConstants.ARG_FORECAST_LEVEL),
                train_run_id=train_run_id,
                train_experiment_name=train_experiment_name,
                forecast_step=forecast_step,
                allow_multi_partitions=self.allow_multi_partitions,
                skip_concat_results=ru.str_or_bool_to_boolean(
                    self.arguments_dict.get(PipelineConstants.ARG_SKIP_CONCAT_RESULTS, False)
                ),
                target_column_name=target_column_name
            )
            if ic._forecast_quantiles and 0.5 not in ic.forecast_quantiles:
                self._print("0.5 quantile is automatically added for the evaluation purpose.")
                ic._forecast_quantiles.append(0.5)
            return ic

    @staticmethod
    def _get_inference_config_file_name(metadata_dir: str) -> str:
        return os.path.join(metadata_dir, SetupStepWrapper.FILE_INFERENCE_CONFIGS)

    @staticmethod
    def _get_evaluation_configs_file_path(metadata_dir: str) -> str:
        return os.path.join(metadata_dir, SetupStepWrapper.FILE_EVALUATION_CONFIGS)

    @staticmethod
    def _get_inference_configs_from_metadata_dir(metadata_dir: str) -> InferenceConfigs:
        with open(SetupStepWrapper._get_inference_config_file_name(metadata_dir)) as f:
            return cast(InferenceConfigs, json.load(f, cls=HTSRuntimeDecoder))

    @staticmethod
    def _get_evaluation_configs_from_metadata_dir(metadata_dir: str) -> EvaluationConfigs:
        with open(SetupStepWrapper._get_evaluation_configs_file_path(metadata_dir)) as f:
            return cast(EvaluationConfigs, json.load(f, cls=HTSRuntimeDecoder))

    def _get_settings_from_run(
            self, experiment_name: Optional[str] = None, train_run_id: Optional[str] = None
    ) -> Dict[str, Any]:
        train_run = self._get_train_run(experiment_name, train_run_id)
        train_run.download_file(self.FILE_CONFIGS, self.FILE_CONFIGS)
        return ru.get_settings(self.FILE_CONFIGS)

    def _remove_default_inputs_from_arguments_dict(self, arguments_dict: Dict[str, str]) -> Dict[str, str]:
        new_arg_dict = copy.deepcopy(arguments_dict)
        removed_keys = []
        for k, v in arguments_dict.items():
            if v == self.NO_VALUE or v == [self.NO_VALUE]:
                removed_keys.append(k)
        for k in removed_keys:
            del new_arg_dict[k]
        return new_arg_dict

    def _get_train_run(self, experiment_name: Optional[str] = None, train_run_id: Optional[str] = None) -> Run:
        if not experiment_name:
            experiment_name = self.arguments_dict.get(PipelineConstants.ARG_EXPERIMENT_NAME)
        if experiment_name is None:
            experiment = self.step_run.experiment
        else:
            experiment = Experiment(self.step_run.experiment.workspace, experiment_name)
        if not train_run_id:
            train_run_id = self.arguments_dict.get(PipelineConstants.ARG_TRAIN_RUN_ID)
        if train_run_id is None:
            return self._get_latest_successful_training_run(experiment)
        else:
            return Run(experiment, train_run_id)

    def _get_latest_successful_training_run(self, experiment: Experiment) -> Run:
        """
        Get the latest successful HTS training run for the experiment.

        :param experiment: An AzureML experiment.
        :raises: ConfigException
        :return: The latest successful HTS training run.
        """
        retry_count = 3
        training_runs = []  # type: List[Run]
        root_level_runs = []  # type: List[Run]
        while retry_count > 0 and not root_level_runs:
            root_level_runs = [r for r in Run.list(experiment, status=RunStatus.COMPLETED)]
            retry_count -= 1
        retry_count = 3
        while retry_count > 0 and not training_runs:
            for r in root_level_runs:
                for child in r.get_children(status=RunStatus.COMPLETED):
                    for child_child in child.get_children(
                        status=RunStatus.COMPLETED,
                        properties={
                            PipelineConstants.PROPERTIES_RUN_TYPE: self.run_type,
                            PipelineConstants.PROPERTIES_PIPELINE_TYPE: PipelineConstants.PROPERTIES_VALUE_TRAINING
                        }
                    ):
                        training_runs.append(child_child)
            retry_count -= 1
            if not training_runs and retry_count > 0:
                print(
                    "There is no training runs can be found in the input experiment {},"
                    " another retry will happen after 30s. {} retries is remainin...".format(
                        experiment.name, retry_count
                    ))
                time.sleep(30)
        if not training_runs:
            raise ConfigException._with_error(
                AzureMLError.create(
                    HierarchyNoTrainingRun, target="training_run_id",
                    reference_code=ReferenceCodes._HTS_NO_TRAINING_RUN
                )
            )

        latest_train_run = sorted(
            training_runs, key=lambda r: ru._convert_iso_datetime_str(
                r.get_details().get('endTimeUtc')), reverse=True)[0]
        logger.info("Latest train run used is {}.".format(latest_train_run.id))
        return latest_train_run

    @property
    def allow_multi_partitions(self) -> bool:
        return True if self._allow_multi_partitions else False
    # endregion

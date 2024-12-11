# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, cast, List, Optional
import logging
import os
import sys
import shutil

from azureml.core import Run
from azureml.automl.core.console_writer import ConsoleWriter
from azureml.train.automl.constants import HTSConstants
from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared.exceptions import ConfigException
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    InvalidArgumentWithSupportedValues,
    DataPathNotFound,
    QuantileForecastAggregationNotSupported
)

from ..setup_step_wrapper import SetupStepWrapper
from ....constants import HTSPipelineConstants, PipelineConstants
from ....data_models.hts_graph import Graph
from ....data_models.evaluation_configs import EvaluationConfigs
from ....utilities.file_utilities import (
    dump_object_to_json
)
from ....utilities.run_utilities import (
    get_hierarchy,
    get_training_level,
    get_label_column_name,
    get_settings,
    get_hierarchy_to_training_level,
    validate_hierarchy_settings
)
from ....utilities.logging_utilities import (
    event_log_wrapped
)
from ....utilities.events.hts_setup_events import (
    HierarchyBuilderStart,
    HierarchyBuilderEnd
)


logger = logging.getLogger(__name__)
console_writer = ConsoleWriter(sys.stdout)


class HTSSetupWrapper(SetupStepWrapper):
    """The wrapper code for hierarchy builder runs."""
    FILE_NODE_COLUMNS_INFO_JSON = "node_columns_info.json"
    FILE_PROPORTIONS = "metadata.json"
    FILE_GRAPH = "hts_graph.json"

    def __init__(self, current_step_run: Optional[Run] = None, is_train: bool = True, **kwargs: Any) -> None:
        """
        The wrapper code for hierarchy builder runs.

        :param current_step_run: The current step run.
        """
        super().__init__(
            HTSPipelineConstants.STEP_SETUP if is_train else HTSPipelineConstants.STEP_SETUP_INF,
            current_step_run, is_train, **kwargs
        )
        if not is_train:
            train_metadata = cast(Optional[str], self.arguments_dict.get(PipelineConstants.ARG_TRAIN_METADATA))
            if train_metadata is not None:
                self._print("Try copying files from train metadata")
                self._copy_metadata_file_from_train(train_metadata, self.dataset_info_path)
            else:
                self._print("Try downloading files from train")
                self._train_run = self._get_train_run()
                self._download_metadata()
            self.settings = get_settings(os.path.join(self.dataset_info_path, self.FILE_CONFIGS))
            self.graph = Graph.get_graph_from_file(self._get_graph_json_file_path_v2(self.dataset_info_path))
            if self.inference_configs.train_experiment_name is None:
                self.inference_configs.train_experiment_name = self._train_run.experiment.name
            if self.inference_configs.train_run_id is None:
                self.inference_configs.train_run_id = self._train_run.id
            self.inference_configs.partition_column_names = self.graph.hierarchy_to_training_level
            self.inference_configs.target_column_name = self.graph.label_column_name
        self.hierarchy = get_hierarchy(self.settings)
        self.training_level = get_training_level(self.settings)

    def _validate_settings(self) -> None:
        super(HTSSetupWrapper, self)._validate_settings()
        if self.is_train:
            self._validate_hts_settings()
        else:
            if self.inference_configs.forecast_quantiles:
                valid_levels = self.get_hierarchy_valid_quantile_forecast_levels()
                if self.inference_configs.forecast_level not in valid_levels:
                    raise ConfigException._with_error(
                        AzureMLError.create(
                            QuantileForecastAggregationNotSupported,
                            forecast_level_param='hierarchy_forecast_level',
                            valid_forecast_levels=valid_levels,
                            reference_code=ReferenceCodes._HTS_QUANTILE_FORECAST_AGGREGATION,
                            target='hierarchy_forecast_level'
                        )
                    )

    def _validate_hts_settings(self) -> None:
        validate_hierarchy_settings(
            self.hierarchy, self.training_level, self.forecasting_parameters, get_label_column_name(self.settings),
            self.raw_data_columns
        )

    def _build_evaluation_configs(self) -> EvaluationConfigs:
        eval_conf = super()._build_evaluation_configs()
        if not self.is_train:
            eval_conf.update_timeseries_id_columns(
                self.graph.get_hierarchy_to_level(cast(str, self.inference_configs.forecast_level)))
        return eval_conf

    def save_meta_data(self) -> None:
        # for inference the graph file is downloaded into metadata dir.
        if self.is_train:
            graph = self.hierarchy_builder()
            dump_object_to_json(graph.serialize(), self._get_graph_json_file_path_v2(self.dataset_info_path))
        super(HTSSetupWrapper, self).save_meta_data()

    def _download_metadata(self) -> None:
        for f in self._train_metadata_files_list:
            self._train_run.download_file(f, self.dataset_info_path)

    def _copy_metadata_file_from_train(self, input_dir: str, output_dir: str) -> None:
        for fn in self._train_metadata_files_list:
            if not os.path.isfile(os.path.join(input_dir, fn)):
                raise ConfigException._with_error(
                    AzureMLError.create(
                        DataPathNotFound,
                        dprep_error=f"{fn} cannot be found in the train_metadata folder. "
                                    f"Please make sure it is from an HTS train run."
                    )
                )
            shutil.copyfile(
                os.path.join(input_dir, fn), os.path.join(output_dir, fn)
            )

    def _get_target_column_name(self):
        return self.graph.label_column_name

    @property
    def _train_metadata_files_list(self) -> List[str]:
        return [
            HTSSetupWrapper.FILE_CONFIGS, HTSSetupWrapper.FILE_GRAPH, HTSSetupWrapper.FILE_PROPORTIONS,
            HTSSetupWrapper.FILE_NODE_COLUMNS_INFO_JSON
        ]

    @event_log_wrapped(HierarchyBuilderStart(), HierarchyBuilderEnd())
    def hierarchy_builder(self) -> Graph:
        """
        The driver code for pre_proportions_calculation step.

        :return: None
        """
        graph = Graph(
            hierarchy=self.hierarchy,
            training_level=self.training_level,
            forecasting_parameters=self.forecasting_parameters,
            label_column_name=get_label_column_name(self.settings)
        )
        all_files = self._get_all_files(self.preprocessed_data_path)
        for f in all_files:
            df = self.load_data_from_file(f)
            logger.info("Processing file: shape {}, size {}".format(df.shape, os.path.getsize(f)))
            graph.make_or_update_hierarchy(df)
        # dump graph and upload to artifact
        return graph

    @property
    def partition_columns(self) -> List[str]:
        return cast(List[str], get_hierarchy_to_training_level(self.settings))

    @property
    def additional_params(self) -> List[str]:
        return [HTSConstants.HIERARCHY, HTSConstants.TRAINING_LEVEL]

    @property
    def run_type(self) -> str:
        """The run type of the wrapper."""
        return PipelineConstants.RUN_TYPE_HTS

    def _validate_inference_settings(self) -> None:
        super(HTSSetupWrapper, self)._validate_inference_settings()
        self.inference_configs._check_allocation_method_has_value()
        forecast_level = self.inference_configs.forecast_level
        if forecast_level not in self.hierarchy and forecast_level != HTSConstants.HTS_ROOT_NODE_LEVEL:
            raise ConfigException._with_error(
                AzureMLError.create(
                    InvalidArgumentWithSupportedValues,
                    arguments="{} in forecast_level".format(forecast_level),
                    supported_values="hierarchy column names and {}".format(HTSConstants.HTS_ROOT_NODE_LEVEL),
                    reference_code=ReferenceCodes._MM_FORECAST_LEVEL_BAD_VALUE
                )
            )

    def get_hierarchy_valid_quantile_forecast_levels(self) -> List[str]:
        """
        Get a list of valid levels for a quantile forecasting scenario.

        Quantile forecasts do not currently support aggregation, so this method returns
        a list of levels equal to and below the training level.

        :return: A list of valid forecast levels
        """
        hierarchy = get_hierarchy(self.settings)
        training_level = get_training_level(self.settings)
        if training_level == HTSConstants.HTS_ROOT_NODE_LEVEL:
            return cast(List[str], [HTSConstants.HTS_ROOT_NODE_LEVEL] + hierarchy)
        return cast(List[str], hierarchy[hierarchy.index(training_level):])

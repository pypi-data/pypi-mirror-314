# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, Dict, Optional, List
import logging
import os
import pandas as pd
import tempfile

from azureml.core import Run

from ...data_models.hts_graph import Graph
from ...data_models.arguments import Arguments
from ...data_models.node_columns_info import NodeColumnsInfo
from ..automl_prs_run_base import AutoMLPRSRunBase
from ..automl_prs_step_wrapper import AutoMLPRSStepWrapper
from .setup_step_wrapper import SetupStepWrapper
from ...constants import PipelineConstants


logger = logging.getLogger(__name__)


class AutoMLPRSInferenceWrapper(AutoMLPRSStepWrapper):
    """The wrapper code for automl inference runs."""
    def __init__(
            self,
            step_name: str,
            current_run_step: Optional[Run] = None,
            **kwargs: Any
    ) -> None:
        """
        The wrapper code for automl inference runs.

        :param working_dir: The working dir of the script.
        :param current_step_run: The current step run.
        """
        super().__init__(
            step_name, tempfile.TemporaryDirectory(prefix=self.__class__.__name__).name, current_run_step, **kwargs)
        self._input_metadata = self.arguments_dict[PipelineConstants.ARG_SETUP_METADATA]
        self._inference_configs = SetupStepWrapper._get_inference_configs_from_metadata_dir(self._input_metadata)

    def _get_run_class(self) -> AutoMLPRSRunBase:
        """Get the run class."""
        raise NotImplementedError

    def _init_prs(self) -> None:
        pass

    def _get_graph(self) -> Graph:
        raise NotImplementedError

    @property
    def _sdk_version(self) -> str:
        return PipelineConstants.SDK_V2


class AutoMLPRSInference(AutoMLPRSRunBase):
    """AutoML solution accelerator train base class."""
    def __init__(
            self,
            current_step_run: Run,
            arguments_dict: Dict[str, str],
            event_log_dim: Dict[str, str],
            partition_column_names: List[str],
            graph: Optional[Graph] = None,
            forecast_quantiles: Optional[List[float]] = None,
            forecast_mode: Optional[str] = None,
            step: Optional[int] = None,
            inference_type: Optional[str] = None,
            train_exp_name: Optional[str] = None,
            train_run_id: Optional[str] = None,
            node_columns_info: Optional[Dict[str, NodeColumnsInfo]] = None,
            allow_multi_partitions: bool = False,
            target_column_name: Optional[str] = None,
            **kwargs: Any
    ) -> None:
        """
        AutoML inference and validation run class.

        :param current_step_run: A run object that the script is running.
        :param arguments_dict: The dict contains all the PRS run arguments.
        :param event_log_dim: The event log dim.
        :param graph: The hts graph.
        """
        super().__init__(
            current_step_run, process_count_per_node=int(arguments_dict.get("process_count_per_node", 10)), **kwargs)
        self.arguments_dict = arguments_dict
        self.event_logger_additional_fields = event_log_dim
        self.graph = graph
        self.partition_column_names = partition_column_names
        self.input_metadata = self.arguments_dict[PipelineConstants.ARG_SETUP_METADATA]
        self.target_path = self.arguments_dict[PipelineConstants.ARG_OUTPUT_PREDICT]
        self.output_path = self.arguments_dict[PipelineConstants.ARG_OUTPUT_METADATA]
        self.forecast_quantiles = forecast_quantiles
        self.train_exp_name = train_exp_name
        self.train_run_id = train_run_id
        self.node_columns_info = node_columns_info
        self.allow_multi_partitions = allow_multi_partitions
        self.forecast_mode = forecast_mode
        self.inference_type = inference_type
        self.step = step
        self.target_column_name = target_column_name
        os.makedirs(self.output_path, exist_ok=True)

    def get_automl_run_prs_scenario(self) -> str:
        raise NotImplementedError

    def get_run_result(self, output_file: str) -> pd.DataFrame:
        """Get the result of the run."""
        return pd.read_parquet(output_file)

    def get_prs_run_arguments(self) -> Arguments:
        """Get the arguments for the PRS runs."""
        return Arguments(
            process_count_per_node=self.process_count_per_node, target_path=self.target_path,
            output_path=self.output_path, event_logger_dim=self.event_logger_additional_fields,
            partition_column_names=self.partition_column_names, forecast_quantiles=self.forecast_quantiles,
            train_exp_name=self.train_exp_name, train_run_id=self.train_run_id, hts_graph=self.graph,
            node_columns_info=self.node_columns_info, allow_multi_partitions=self.allow_multi_partitions,
            inference_type=self.inference_type, forecast_mode=self.forecast_mode, step=self.step,
            target_column_name=self.target_column_name
        )

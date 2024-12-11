# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, Dict, Optional, Union
import pandas as pd
from pathlib import Path
import os

from azureml.core import Run

from ....data_models.hts_graph import Graph
from ....data_models.arguments import Arguments
from ....constants import HTSPipelineConstants
from ...automl_prs_run_base import AutoMLPRSRunBase
from ...automl_prs_step_wrapper import AutoMLPRSStepWrapper
from ...automl_prs_driver_factory_v2 import AutoMLPRSDriverFactoryV2
from ....constants import PipelineConstants


class HTSDataAggregationWrapperV2(AutoMLPRSStepWrapper):
    """The wrapper code for data aggregation runs."""
    def __init__(
            self,
            working_dir: Union[str, Path],
            current_run_step: Optional[Run] = None,
            **kwargs: Any
    ) -> None:
        """
        The wrapper code for data aggregation runs.

        :param working_dir: The working dir of the script.
        :param current_run_step: The current step run.
        """
        super().__init__(
            HTSPipelineConstants.STEP_DATA_AGGREGATION, working_dir, current_run_step, **kwargs)
        self._settings = self._get_automl_settings_dict_v2(
            self.arguments_dict[PipelineConstants.ARG_INPUT_METADATA])

    def _init_prs(self) -> None:
        """Init the prs parameters."""
        self._graph = self._get_graph()

    def _get_run_class(self) -> AutoMLPRSRunBase:
        """Get the run class for the actual run."""
        return HTSDataAggregationV2(
            self.step_run,
            self._settings,
            self.arguments_dict, self.event_logger_dim, self.graph)

    @property
    def _sdk_version(self) -> str:
        return PipelineConstants.SDK_V2

    def _get_graph(self) -> Graph:
        return self._get_graph_from_metadata_v2(self.arguments_dict[PipelineConstants.ARG_INPUT_METADATA])


class HTSDataAggregationV2(AutoMLPRSRunBase):
    """HTS data aggregation class."""
    def __init__(
            self,
            current_step_run: Run,
            automl_settings: Dict[str, Any],
            arguments_dict: Dict[str, str],
            event_log_dim: Dict[str, str],
            graph: Graph,
            **kwargs: Any
    ) -> None:
        """
        HTS data aggregation and validation run class.

        :param current_step_run: A run object that the script is running.
        :param arguments_dict: The dict contains all the PRS run arguments.
        :param event_log_dim: The event log dim.
        :param graph: The hts graph.
        """
        super().__init__(
            current_step_run,
            automl_settings=automl_settings,
            process_count_per_node=int(arguments_dict.get("process_count_per_node", 10)),
            **kwargs)

        self._console_writer.println("dir info")

        self.output_path = arguments_dict[PipelineConstants.ARG_OUTPUT_METADATA]
        self.target_path = arguments_dict[PipelineConstants.ARG_OUTPUT_AGG_DATA]
        os.makedirs(os.path.dirname(self.target_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        self.event_log_dim = event_log_dim
        self.hts_graph = graph

    def get_automl_run_prs_scenario(self) -> str:
        """Get automl PRS run scenario."""
        return AutoMLPRSDriverFactoryV2.HTS_DATA_AGGREGATION

    def get_run_result(self, output_file: str) -> pd.DataFrame:
        """Get the result of the run."""
        return pd.read_parquet(output_file)

    def get_prs_run_arguments(self) -> Arguments:
        """Get the arguments used for the subprocess driver code."""
        return Arguments(
            process_count_per_node=self.process_count_per_node, hts_graph=self.hts_graph,
            output_path=self.output_path, target_path=self.target_path,
            event_logger_dim=self.event_log_dim
        )

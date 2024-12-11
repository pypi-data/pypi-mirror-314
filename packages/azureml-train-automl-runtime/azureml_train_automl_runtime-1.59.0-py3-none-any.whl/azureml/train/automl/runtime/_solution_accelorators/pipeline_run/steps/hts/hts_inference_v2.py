# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, cast, Dict, Optional, List
import os
import json

from azureml.core import Run

from ....data_models.hts_graph import Graph
from ....data_models.node_columns_info import NodeColumnsInfo
from ....constants import HTSPipelineConstants, PipelineConstants
from ....utilities.json_serializer import HTSRuntimeDecoder
from ...automl_prs_run_base import AutoMLPRSRunBase
from ...automl_prs_driver_factory_v2 import AutoMLPRSDriverFactoryV2
from ..automl_prs_inference import AutoMLPRSInference, AutoMLPRSInferenceWrapper
from .hts_setup_wrapper import HTSSetupWrapper


class HTSInferenceWrapperV2(AutoMLPRSInferenceWrapper):
    """The wrapper code for many models forecast."""
    RUN_TAG_TRAIN_ID = "hts_training_run"

    def __init__(
            self,
            current_run_step: Optional[Run] = None,
            **kwargs: Any
    ) -> None:
        """
        The wrapper code for many models forecast.

        :param current_step_run: The current step run.
        """
        super().__init__(
            HTSPipelineConstants.STEP_INFERENCE, current_run_step, **kwargs)
        self._input_metadata = self.arguments_dict[PipelineConstants.ARG_SETUP_METADATA]
        self._pipeline_run: Optional[Run] = None
        self.node_columns_info: Optional[Dict[str, NodeColumnsInfo]] = None

    def _init_prs(self) -> None:
        """Init the prs parameters."""
        self.pipeline_run.set_tags({self.RUN_TAG_TRAIN_ID: self._inference_configs.train_run_id})
        self._graph = self._get_graph()
        self.node_columns_info = self.get_node_columns_info_from_artifacts()

    def _get_run_class(self) -> AutoMLPRSRunBase:
        return HTSInferenceV2(
            self.step_run, self.arguments_dict, self.event_log_dim, cast(Graph, self._graph),
            cast(str, self._inference_configs.train_experiment_name),
            cast(str, self._inference_configs.train_run_id),
            self.node_columns_info,
            forecast_mode=self._inference_configs.forecast_mode,
            step=self._inference_configs.forecast_step,
            target_column_name=self._inference_configs.target_column_name,
            forecast_quantiles=self._inference_configs.forecast_quantiles
        )

    @property
    def pipeline_run(self) -> Run:
        """The pipeline run."""
        if self._pipeline_run is None:
            self._pipeline_run = self.get_pipeline_run(self.step_run)
        return self._pipeline_run

    @property
    def run_type(self) -> str:
        """Run type for the run."""
        return PipelineConstants.RUN_TYPE_HTS

    def get_node_columns_info_from_artifacts(self) -> Dict[str, NodeColumnsInfo]:
        """
        Get the node-columns info from artifacts.

        """
        info_file = os.path.join(self._input_metadata, HTSSetupWrapper.FILE_NODE_COLUMNS_INFO_JSON)
        with open(info_file) as f:
            node_columns_info = json.load(f, cls=HTSRuntimeDecoder)

        return self._parse_columns_info(node_columns_info)

    @staticmethod
    def _parse_columns_info(raw_node_columns_info_data: List[NodeColumnsInfo]) -> Dict[str, NodeColumnsInfo]:
        """
        Convert the json node columns info to node_id-columns info dict.

        :param raw_node_columns_info_data: The raw node column info.
        :return: A dict mapping the columns names to the NodeColumnInfo.
        """
        parsed_vocabulary = {}
        for node_columns_info in raw_node_columns_info_data:
            parsed_vocabulary[node_columns_info.node_id] = node_columns_info
        return parsed_vocabulary

    def _get_graph(self) -> Graph:
        return self._get_graph_from_metadata_v2(self._input_metadata)


class HTSInferenceV2(AutoMLPRSInference):
    """Inference class for HTS."""
    def __init__(
            self,
            current_step_run: Run,
            arguments_dict: Dict[str, str],
            event_log_dim: Dict[str, str],
            graph: Graph,
            train_exp_name: str,
            train_run_id: str,
            node_columns_info: Optional[Dict[str, NodeColumnsInfo]],
            forecast_mode: Optional[str],
            step: Optional[int],
            target_column_name: Optional[str],
            forecast_quantiles: Optional[List[float]],
            **kwargs: Any
    ) -> None:
        """
        HTS data aggregation and validation run class.

        :param current_step_run: A run object that the script is running.
        :param arguments_dict: The dict contains all the PRS run arguments.
        :param event_log_dim: The event log dim.
        """
        super().__init__(
            current_step_run,
            arguments_dict=arguments_dict,
            event_log_dim=event_log_dim,
            graph=graph,
            partition_column_names=graph.hierarchy_to_training_level,
            train_exp_name=train_exp_name,
            train_run_id=train_run_id,
            node_columns_info=node_columns_info,
            forecast_mode=forecast_mode,
            step=step,
            target_column_name=target_column_name,
            forecast_quantiles=forecast_quantiles,
            **kwargs
        )

    def get_automl_run_prs_scenario(self) -> str:
        """Get the PRS run scenario."""
        return AutoMLPRSDriverFactoryV2.HTS_INFERENCE

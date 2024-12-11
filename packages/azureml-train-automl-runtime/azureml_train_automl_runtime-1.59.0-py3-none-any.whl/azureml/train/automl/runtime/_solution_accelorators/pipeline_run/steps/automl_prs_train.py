# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, cast, Dict, Optional, Union, List
from abc import abstractmethod
import copy
import logging
import os
import pandas as pd
from pathlib import Path
import tempfile

from azureml.core import Run

from ...data_models.hts_graph import Graph
from ...data_models.arguments import Arguments
from ...utilities.run_utilities import str_or_bool_to_boolean
from ..automl_prs_run_base import AutoMLPRSRunBase
from ..automl_prs_step_wrapper import AutoMLPRSStepWrapper
from ...constants import PipelineConstants


logger = logging.getLogger(__name__)


class AutoMLPRSTrainWrapper(AutoMLPRSStepWrapper):
    """The wrapper code for hts automl train runs."""
    def __init__(
            self,
            step_name: str,
            working_dir: Union[str, Path],
            current_run_step: Optional[Run] = None,
            **kwargs: Any
    ) -> None:
        """
        The wrapper code for hts automl train runs.

        :param working_dir: The working dir of the script.
        :param current_step_run: The current step run.
        """
        super().__init__(
            step_name, working_dir, current_run_step, **kwargs)
        self._settings: Optional[Dict[str, Any]] = None

    def _init_prs(self) -> None:
        """Init the prs parameters."""
        self._settings = self._get_automl_settings_dict_v2(
            self.arguments_dict[PipelineConstants.ARG_INPUT_METADATA])

    def _get_run_class(self) -> AutoMLPRSRunBase:
        """Get the run class for the actual run."""
        raise NotImplementedError

    def _get_graph(self) -> Graph:
        return self._get_graph_from_metadata_v2(self.arguments_dict[PipelineConstants.ARG_INPUT_METADATA])

    @property
    @abstractmethod
    def partition_columns(self) -> List[str]:
        raise NotImplementedError

    @property
    def automl_settings(self) -> Dict[str, Any]:
        if self._settings is None:
            self._settings = self._get_automl_settings_dict_v2(
                self.arguments_dict[PipelineConstants.ARG_INPUT_METADATA])
        return self._settings

    @property
    def _sdk_version(self) -> str:
        return PipelineConstants.SDK_V2


class AutoMLPRSTrain(AutoMLPRSRunBase):
    """AutoML solution accelerator train base class."""
    PIPELINE_FETCH_MAX_BATCH_SIZE = 15

    def __init__(
            self,
            current_step_run: Run,
            arguments_dict: Dict[str, str],
            event_log_dim: Dict[str, str],
            settings: Dict[str, Any],
            partition_column_names: List[str],
            retrain_failed_models: Optional[bool] = False,
            graph: Optional[Graph] = None,
            **kwargs: Any
    ) -> None:
        """
        HTS data aggregation and validation run class.

        :param current_step_run: A run object that the script is running.
        :param arguments_dict: The dict contains all the PRS run arguments.
        :param event_log_dim: The event log dim.
        :param graph: The hts graph.
        """
        super().__init__(current_step_run, **kwargs)

        self._console_writer.println("dir info")

        self.output_path = arguments_dict[PipelineConstants.ARG_OUTPUT_METADATA]
        self.input_metadata = arguments_dict[PipelineConstants.ARG_INPUT_METADATA]
        self.process_count_per_node = int(arguments_dict.get("process_count_per_node", 10))
        os.makedirs(self.output_path, exist_ok=True)

        # Get settings
        self.automl_settings = copy.deepcopy(settings)
        self.automl_settings['many_models'] = True
        self.automl_settings['many_models_process_count_per_node'] = self.process_count_per_node
        self.automl_settings['pipeline_fetch_max_batch_size'] = self.automl_settings.get(
            'pipeline_fetch_max_batch_size', self.PIPELINE_FETCH_MAX_BATCH_SIZE)

        debug_log = self.automl_settings.get('debug_log', None)
        if debug_log is not None:
            self.automl_settings['debug_log'] = os.path.join(self.log_dir, debug_log)
            self.automl_settings['path'] = tempfile.mkdtemp()
            self._console_writer.println("{}.AutoML debug log:{}".format(__file__, self.automl_settings['debug_log']))

        self.event_logger_dim = event_log_dim
        self.retrain_failed_models = retrain_failed_models
        self.hts_graph = graph
        self.partition_column_names = partition_column_names
        self.engineered_explanation = str_or_bool_to_boolean(
            arguments_dict.get(PipelineConstants.ARG_ENGINEERED_EXPLANATION, False))

    def get_automl_run_prs_scenario(self) -> str:
        """Get automl PRS run scenario."""
        raise NotImplementedError

    def get_run_result(self, output_file: str) -> pd.DataFrame:
        """Get the result of the run."""
        if os.path.exists(output_file):
            return pd.read_parquet(output_file)
        return pd.DataFrame({})

    def get_prs_run_arguments(self) -> Arguments:
        """Get the arguments used for the subprocess driver code."""
        return Arguments(
            process_count_per_node=self.process_count_per_node, hts_graph=self.hts_graph,
            output_path=self.output_path, event_logger_dim=self.event_logger_dim,
            retrain_failed_models=self.retrain_failed_models,
            partition_column_names=self.partition_column_names,
            input_metadata=self.input_metadata,
            engineered_explanation=self.engineered_explanation
        )

# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, Dict, Optional, Union, List
import logging
from pathlib import Path

from azureml.core import Run

from ....constants import HTSPipelineConstants, HTSConstants
from ....data_models.hts_graph import Graph
from ....utilities.run_utilities import str_or_bool_to_boolean
from ...automl_prs_driver_factory_v2 import AutoMLPRSDriverFactoryV2
from ...automl_prs_run_base import AutoMLPRSRunBase
from ..automl_prs_train import AutoMLPRSTrainWrapper, AutoMLPRSTrain, PipelineConstants


logger = logging.getLogger(__name__)


class HTSAutoMLTrainWrapperV2(AutoMLPRSTrainWrapper):
    """The wrapper code for hts automl train runs."""
    def __init__(self, working_dir: Union[str, Path], current_run_step: Optional[Run] = None, **kwargs: Any):
        """
        The wrapper code for hts automl train runs.

        :param working_dir: The working dir of the script.
        :param current_run_step: The current step run.
        """
        super().__init__(HTSPipelineConstants.STEP_AUTOML_TRAIN, working_dir, current_run_step, **kwargs)
        self._graph = None

    def _init_prs(self) -> None:
        """Init the prs parameters."""
        self._graph = self._get_graph()

    def _get_run_class(self) -> AutoMLPRSRunBase:
        """Get the run class for the actual run."""
        return HTSAutoMLTrainV2(
            self.step_run, self.automl_settings, self.arguments_dict, self.event_logger_dim,
            self.partition_columns, self.graph)

    @property
    def partition_columns(self) -> List[str]:
        """The partition column names."""
        return self.graph.hierarchy_to_training_level


class HTSAutoMLTrainV2(AutoMLPRSTrain):
    """HTS AutoML train class."""
    def __init__(
            self,
            current_step_run: Run,
            automl_settings: Dict[str, Any],
            arguments_dict: Dict[str, str],
            event_log_dim: Dict[str, str],
            partition_column_names: List[str],
            graph: Graph,
            **kwargs: Any
    ):
        """
        HTS data aggregation and validation run class.

        :param current_step_run: A run object that the script is running.
        :param working_dir: The working dir of the parent run.
        :param arguments_dict: The dict contains all the PRS run arguments.
        :param event_log_dim: The event log dim.
        :param graph: The hts graph.
        """
        super(HTSAutoMLTrainV2, self).__init__(
            current_step_run,
            arguments_dict,
            event_log_dim,
            automl_settings,
            partition_column_names,
            retrain_failed_models=False,
            graph=graph,
            **kwargs)
        self.enable_engineered_explanations = str_or_bool_to_boolean(
            arguments_dict[HTSConstants.ENGINEERED_EXPLANATION])
        self.hts_graph = graph
        # overwrite the input metadata using the updated one.
        self.input_metadata = arguments_dict[PipelineConstants.ARG_DATA_AGG_METADATA]

    def get_automl_run_prs_scenario(self) -> str:
        """Get automl PRS run scenario."""
        return AutoMLPRSDriverFactoryV2.HTS_AUTOML_TRAIN

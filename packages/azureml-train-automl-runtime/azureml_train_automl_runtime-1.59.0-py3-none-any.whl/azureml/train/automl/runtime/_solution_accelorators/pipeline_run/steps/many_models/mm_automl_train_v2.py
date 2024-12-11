# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, Dict, Optional, Union, List
import logging
from pathlib import Path

from azureml.core import Run

from ....constants import ManyModelsPipelineConstants, PipelineConstants
from ...automl_prs_driver_factory_v2 import AutoMLPRSDriverFactoryV2
from ...automl_prs_run_base import AutoMLPRSRunBase
from ..automl_prs_train import AutoMLPRSTrainWrapper, AutoMLPRSTrain
from ....utilities.run_utilities import str_or_bool_to_boolean

logger = logging.getLogger(__name__)


class MMAutoMLTrainWrapperV2(AutoMLPRSTrainWrapper):
    """The wrapper code for hts automl train runs."""

    def __init__(
            self, working_dir: Union[str, Path], current_run_step: Optional[Run] = None, **kwargs: Any
    ) -> None:
        """
        The wrapper code for hts automl many models train runs.

        :param working_dir: The working dir of the script.
        :param current_step_run: The current step run.
        """
        super().__init__(
            ManyModelsPipelineConstants.STEP_AUTOML_TRAIN, working_dir, current_run_step, **kwargs)
        self._retrain_failed_models = str_or_bool_to_boolean(
            self.arguments_dict.get(PipelineConstants.ARG_RETRAIN_FAILED_MODEL, False))

    @property
    def partition_columns(self) -> List[str]:
        """The partition column names"""
        return self._get_partition_columns_from_settings(self.automl_settings)

    def _get_run_class(self) -> AutoMLPRSRunBase:
        return MMAutoMLTrainV2(
            current_step_run=self.step_run, automl_settings=self.automl_settings,
            arguments_dict=self.arguments_dict, event_log_dim=self.event_logger_dim,
            partition_column_names=self.partition_columns, retrain_failed_models=self._retrain_failed_models
        )


class MMAutoMLTrainV2(AutoMLPRSTrain):
    """HTS AutoML train class."""
    def __init__(
            self,
            current_step_run: Run,
            automl_settings: Dict[str, Any],
            arguments_dict: Dict[str, str],
            event_log_dim: Dict[str, str],
            partition_column_names: List[str],
            retrain_failed_models: bool,
            **kwargs: Any
    ) -> None:
        """
        HTS data aggregation and validation run class.

        :param current_step_run: A run object that the script is running.
        :param working_dir: The working dir of the parent run.
        :param arguments_dict: The dict contains all the PRS run arguments.
        :param event_log_dim: The event log dim.
        :param graph: The hts graph.
        """
        super().__init__(
            current_step_run,
            arguments_dict,
            event_log_dim,
            automl_settings,
            partition_column_names,
            retrain_failed_models=retrain_failed_models,
            graph=None,
            **kwargs)

    def get_automl_run_prs_scenario(self) -> str:
        """Get automl PRS run scenario."""
        return AutoMLPRSDriverFactoryV2.MM_AUTOML_TRAIN

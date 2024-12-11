# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
Class for AutoML pipeline step wrapper base class.
"""
from typing import Any, List, Optional, Union
from abc import abstractmethod
import logging
from pathlib import Path
import pandas as pd

from azureml.core import Run
from azureml.automl.core._run import run_lifecycle_utilities
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared._diagnostics.automl_events import RunSucceeded, RunFailed
from azureml.train.automl.constants import HTSConstants
import azureml.train.automl.runtime._hts.hts_runtime_utilities as hru
from azureml.train.automl.runtime._hts.hts_graph import Graph
from .automl_prs_run_base import AutoMLPRSRunBase
from .automl_pipeline_step_wrapper_base import AutoMLPipelineStepWrapperBase
from ..constants import PipelineConstants


logger = logging.getLogger(__name__)


class AutoMLPRSStepWrapper(AutoMLPipelineStepWrapperBase):
    """Wrapper base class for AutoML PRS step runs."""
    def __init__(
            self,
            step_name: str,
            working_dir: Union[str, Path],
            current_step_run: Optional[Run] = None,
            **kwargs: Any
    ) -> None:
        """
        Wrapper base class for AutoML PRS step runs.

        :param step_name: The step name.
        :param current_step_run: The current run step.
        """
        super(AutoMLPRSStepWrapper, self).__init__(step_name, current_step_run, **kwargs)
        self._graph = None  # type: Optional[Graph]
        self.working_dir = working_dir

    def is_prs_step(self) -> bool:
        """Whether the step is prs or not."""
        return True

    def init_prs(self) -> None:
        """Init parameters for the PRS runs."""
        if self._is_init_with_log():
            self._init_prs_with_log()
        else:
            self._init_prs()

    def run_prs(self, prs_input: Union[pd.DataFrame, List[str]]) -> pd.DataFrame:
        """Run the PRS code."""
        print(f'run method start: {__file__}, run({prs_input})')
        event_log_dim = hru.get_event_logger_additional_fields(
            self.event_logger_dim, self.step_run.parent.id, script_type="run",
            should_emit=self.arguments_dict.get(HTSConstants.ENABLE_EVENT_LOGGER, "False"))
        run_class = self._get_run_class()

        try:
            logger.info("{} wrapper started.".format(self.step_name))
            result_list = run_class.run(prs_input)
            self.event_logger.log_event(RunSucceeded(self.step_run.id, event_log_dim))
        except Exception as e:
            logging_utilities.log_traceback(e, logger)
            error_code, error_str = run_lifecycle_utilities._get_error_code_and_error_str(e)
            self.event_logger.log_event(RunFailed(self.step_run.id, error_code, error_str, event_log_dim))
            raise
        return result_list

    def _init_prs_with_log(self) -> None:
        """Init PRS run with logs."""
        try:
            custom_dim = hru.get_additional_logging_custom_dim(self.step_name)
            print(
                "Init for {} with run id {} from parent {}.".format(
                    self.step_name, self.step_run.id, self.step_run.parent.id))
            self.event_log_dim = hru.get_event_logger_additional_fields(
                custom_dim, self.step_run.parent.id, script_type="init",
                should_emit=self.arguments_dict.get(HTSConstants.ENABLE_EVENT_LOGGER, "False"))
            hru.init_logger(
                path=str(Path(__file__).parent.absolute()), handler_name=__name__, custom_dimensions=custom_dim,
                run=self.step_run)
            print("{} init part start.".format(self.step_name))
            self._init_prs()
            print("{} init part completed.".format(self.step_name))
            self.event_logger.log_event(RunSucceeded(self.step_run.id, self.event_log_dim))
        except Exception as e:
            logging_utilities.log_traceback(e, logger)
            # we should let PRS handle the run failure in this case.
            error_code, error_str = run_lifecycle_utilities._get_error_code_and_error_str(e)
            self.event_logger.log_event(RunFailed(self.step_run.id, error_code, error_str, self.event_log_dim))
            raise

    def _is_init_with_log(self) -> bool:
        """Check whether the step should using init with event logs."""
        return (self.step_name in HTSConstants.HTS_SCRIPTS_SCENARIO_ARG_DICT) or \
               (self._sdk_version == PipelineConstants.SDK_V2)

    def _run(self) -> None:
        """The run part. PRS will not use run_prs instead."""
        pass

    @abstractmethod
    def _get_run_class(self) -> AutoMLPRSRunBase:
        """Get PRS run class."""
        pass

    @abstractmethod
    def _init_prs(self) -> None:
        """Init PRS actual run."""
        pass

    @abstractmethod
    def _get_graph(self) -> Graph:
        """Get the hts graph for the run."""
        pass

    @property
    def graph(self) -> Graph:
        """The hts graph."""
        if self._graph is None:
            self._graph = self._get_graph()
        return self._graph

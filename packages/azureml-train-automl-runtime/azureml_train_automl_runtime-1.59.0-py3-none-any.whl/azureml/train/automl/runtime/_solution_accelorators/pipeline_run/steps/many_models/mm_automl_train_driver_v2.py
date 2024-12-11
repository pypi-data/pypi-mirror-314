# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, Dict
import logging

from azureml.core import Run

from ....data_models.arguments import Arguments
from ....utilities import logging_utilities as lu
from ....utilities.events.mm_automl_train_events import (
    MMAutoMLTrainDriverRunStart,
    HMMAutoMLTrainDriverRunEnd
)
from ....constants import PipelineConstants
from ..automl_prs_train_driver import AutoMLPRSTrainDriver


logger = logging.getLogger(__name__)


class MMAutoMLTrainDriverV2(AutoMLPRSTrainDriver):
    def __init__(
            self,
            current_step_run: Run,
            automl_settings: Dict[str, Any],
            args: Arguments
    ) -> None:
        super().__init__(current_step_run, automl_settings, args)

    @lu.event_log_wrapped(MMAutoMLTrainDriverRunStart(), HMMAutoMLTrainDriverRunEnd())
    def run(self, input_data_file: str, output_data_file: str) -> Any:
        super(MMAutoMLTrainDriverV2, self).run(input_data_file, output_data_file)

    @property
    def run_type(self) -> str:
        return PipelineConstants.RUN_TYPE_MM

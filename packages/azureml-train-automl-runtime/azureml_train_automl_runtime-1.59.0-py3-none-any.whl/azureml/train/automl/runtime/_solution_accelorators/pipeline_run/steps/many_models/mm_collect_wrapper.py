# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, Optional
import logging

from azureml.core import Run
from ..collect_step_wrapper import CollectStepWrapper
from ....constants import ManyModelsPipelineConstants


logger = logging.getLogger(__name__)


class MMCollectWrapper(CollectStepWrapper):
    """The wrapper code for collect runs."""
    def __init__(self, current_step_run: Optional[Run] = None, is_train: bool = True, **kwargs: Any) -> None:
        """
        The wrapper code for proportions calculation runs.

        :param current_step_run: The current step run.
        """
        super().__init__(
            ManyModelsPipelineConstants.STEP_COLLECT if is_train else ManyModelsPipelineConstants.STEP_COLLECT_INF,
            current_step_run, is_train, **kwargs
        )

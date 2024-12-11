# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import cast, List, Optional, Any

from azureml.core import Run

from ....data_models.arguments import Arguments
from ....constants import PipelineConstants
from ..automl_inference_driver import AutoMLPRSInferenceDriver


class MMInferenceDriverV2(AutoMLPRSInferenceDriver):
    def __init__(
            self,
            current_step_run: Run,
            args: Arguments,
            **kwargs: Any
    ) -> None:
        """
        This class is used for doing batch inference.

        :param current_step_run: Current step run object, parent of AutoML run.
        :param args: The arguments for the run.
        """
        super().__init__(current_step_run, args, **kwargs)

    @property
    def run_type(self) -> str:
        # This run_type needs to be consistent in train and inference drivers in order to correctly
        # retrieve the model.
        return PipelineConstants.RUN_TYPE_MM

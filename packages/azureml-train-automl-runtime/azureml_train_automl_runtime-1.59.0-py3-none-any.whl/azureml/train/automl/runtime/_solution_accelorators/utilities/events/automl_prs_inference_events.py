# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, Dict, Optional

from azureml.automl.core.shared._diagnostics.automl_events import AutoMLBaseEvent


class AutoMLInferenceDriverRunStart(AutoMLBaseEvent):
    """Start event for solution accelerator setup run."""
    def __init__(self, additional_fields: Optional[Dict[str, Any]] = None) -> None:
        super(AutoMLInferenceDriverRunStart, self).__init__(additional_fields)


class AutoMLInferenceDriverRunEnd(AutoMLBaseEvent):
    """End event for solution accelerator setup run."""
    def __init__(self, additional_fields: Optional[Dict[str, Any]] = None) -> None:
        super(AutoMLInferenceDriverRunEnd, self).__init__(additional_fields)

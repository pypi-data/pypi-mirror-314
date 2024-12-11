# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""The base class to hold all the HTS events."""
from typing import Any, Dict, Optional

from azureml.automl.core.shared._diagnostics.automl_events import AutoMLBaseEvent


class SetupStart(AutoMLBaseEvent):
    """Start event for solution accelerator setup run."""
    def __init__(self, additional_fields: Optional[Dict[str, Any]] = None) -> None:
        super(SetupStart, self).__init__(additional_fields)


class SetupEnd(AutoMLBaseEvent):
    """End event for solution accelerator setup run."""
    def __init__(self, additional_fields: Optional[Dict[str, Any]] = None) -> None:
        super(SetupEnd, self).__init__(additional_fields)


class ValidationStart(AutoMLBaseEvent):
    """Validation start event for solution accelerator setup run."""
    def __init__(self, additional_fields: Optional[Dict[str, Any]] = None) -> None:
        super(ValidationStart, self).__init__(additional_fields)


class ValidationEnd(AutoMLBaseEvent):
    """Validation end event for solution accelerator setup run."""
    def __init__(self, additional_fields: Optional[Dict[str, Any]] = None) -> None:
        super(ValidationEnd, self).__init__(additional_fields)

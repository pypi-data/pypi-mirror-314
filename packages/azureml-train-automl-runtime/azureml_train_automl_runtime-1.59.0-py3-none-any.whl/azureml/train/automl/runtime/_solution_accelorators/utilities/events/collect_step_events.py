# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""The events used for collect step."""
from typing import Any, Dict, Optional

from azureml.automl.core.shared._diagnostics.automl_events import AutoMLBaseEvent


class CollectStart(AutoMLBaseEvent):
    """Start event for solution accelerator setup run."""
    def __init__(self, additional_fields: Optional[Dict[str, Any]] = None) -> None:
        super(CollectStart, self).__init__(additional_fields)


class CollectEnd(AutoMLBaseEvent):
    """End event for solution accelerator setup run."""
    def __init__(self, additional_fields: Optional[Dict[str, Any]] = None) -> None:
        super(CollectEnd, self).__init__(additional_fields)


class DumpDataStart(AutoMLBaseEvent):
    """Start event for solution accelerator setup run."""
    def __init__(self, additional_fields: Optional[Dict[str, Any]] = None) -> None:
        super(DumpDataStart, self).__init__(additional_fields)


class DumpDataEnd(AutoMLBaseEvent):
    """End event for solution accelerator setup run."""
    def __init__(self, additional_fields: Optional[Dict[str, Any]] = None) -> None:
        super(DumpDataEnd, self).__init__(additional_fields)


class CheckResultsStart(AutoMLBaseEvent):
    """Start event for solution accelerator setup run."""
    def __init__(self, additional_fields: Optional[Dict[str, Any]] = None) -> None:
        super(CheckResultsStart, self).__init__(additional_fields)


class CheckResultsEnd(AutoMLBaseEvent):
    """End event for solution accelerator setup run."""
    def __init__(self, additional_fields: Optional[Dict[str, Any]] = None) -> None:
        super(CheckResultsEnd, self).__init__(additional_fields)

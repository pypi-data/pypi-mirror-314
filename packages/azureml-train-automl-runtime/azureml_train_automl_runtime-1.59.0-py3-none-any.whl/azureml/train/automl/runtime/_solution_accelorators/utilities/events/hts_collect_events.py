# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""The Events used for HTS collect step."""
from typing import Any, Dict, Optional

from azureml.automl.core.shared._diagnostics.automl_events import AutoMLBaseEvent


class ProportionsCalculationStart(AutoMLBaseEvent):
    """Start event for solution accelerator setup run."""
    def __init__(self, additional_fields: Optional[Dict[str, Any]] = None) -> None:
        super(ProportionsCalculationStart, self).__init__(additional_fields)


class ProportionsCalculationEnd(AutoMLBaseEvent):
    """End event for solution accelerator setup run."""
    def __init__(self, additional_fields: Optional[Dict[str, Any]] = None) -> None:
        super(ProportionsCalculationEnd, self).__init__(additional_fields)


class AllocationStart(AutoMLBaseEvent):
    """Start event for solution accelerator setup run."""
    def __init__(self, additional_fields: Optional[Dict[str, Any]] = None) -> None:
        super(AllocationStart, self).__init__(additional_fields)


class AllocationEnd(AutoMLBaseEvent):
    """End event for solution accelerator setup run."""
    def __init__(self, additional_fields: Optional[Dict[str, Any]] = None) -> None:
        super(AllocationEnd, self).__init__(additional_fields)


class ExplainStart(AutoMLBaseEvent):
    """Start event for solution accelerator setup run."""
    def __init__(self, additional_fields: Optional[Dict[str, Any]] = None) -> None:
        super(ExplainStart, self).__init__(additional_fields)


class ExplainEnd(AutoMLBaseEvent):
    """End event for solution accelerator setup run."""
    def __init__(self, additional_fields: Optional[Dict[str, Any]] = None) -> None:
        super(ExplainEnd, self).__init__(additional_fields)

# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""The base class to hold all the HTS events."""
from typing import Any, Dict, Optional

from azureml.automl.core.shared._diagnostics.automl_events import AutoMLBaseEvent


class HierarchyBuilderStart(AutoMLBaseEvent):
    """Events for HTS partition tabular dataset start."""
    def __init__(self, additional_fields: Optional[Dict[str, Any]] = None) -> None:
        super(HierarchyBuilderStart, self).__init__(additional_fields)


class HierarchyBuilderEnd(AutoMLBaseEvent):
    """Events for HTS partition tabular dataset start."""
    def __init__(self, additional_fields: Optional[Dict[str, Any]] = None) -> None:
        super(HierarchyBuilderEnd, self).__init__(additional_fields)

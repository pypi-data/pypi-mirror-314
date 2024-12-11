# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""The base class to hold all the HTS events."""
from typing import Any, Dict, Optional

from azureml.automl.core.shared._diagnostics.automl_events import AutoMLBaseEvent


class HTSDataAggregationStart(AutoMLBaseEvent):
    """Events for HTS partition tabular dataset start."""
    def __init__(self, additional_fields: Optional[Dict[str, Any]] = None) -> None:
        super(HTSDataAggregationStart, self).__init__(additional_fields)


class HTSDataAggregationEnd(AutoMLBaseEvent):
    """Events for HTS partition tabular dataset start."""
    def __init__(self, additional_fields: Optional[Dict[str, Any]] = None) -> None:
        super(HTSDataAggregationEnd, self).__init__(additional_fields)


class HTSDataAggregationAggregateData(AutoMLBaseEvent):
    """Events for HTS partition tabular dataset start."""
    def __init__(self, additional_fields: Optional[Dict[str, Any]] = None) -> None:
        super(HTSDataAggregationAggregateData, self).__init__(additional_fields)


class HTSDataAggregationPropCalc(AutoMLBaseEvent):
    """Events for HTS partition tabular dataset start."""
    def __init__(self, additional_fields: Optional[Dict[str, Any]] = None) -> None:
        super(HTSDataAggregationPropCalc, self).__init__(additional_fields)

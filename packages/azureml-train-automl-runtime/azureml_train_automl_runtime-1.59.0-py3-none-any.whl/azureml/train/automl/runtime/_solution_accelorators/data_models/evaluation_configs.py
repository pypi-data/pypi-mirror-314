# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Class for the configs used for evaluation."""
from typing import cast, List, Optional
import inspect

from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.forecasting_parameters import ForecastingParameters


class EvaluationConfigs:
    """Evaluation configs."""
    def __init__(
            self,
            time_column_name: Optional[str] = None,
            time_series_id_column_names: Optional[List[str]] = None,
            predictions_column_name: Optional[str] = None,
            ground_truths_column_name: Optional[str] = None,
            horizon_origin_column: Optional[str] = None,
    ):
        self.time_column_name = time_column_name
        self.time_series_id_column_names = time_series_id_column_names
        self.predictions_column_name = predictions_column_name
        self.ground_truths_column_name = ground_truths_column_name
        self.horizon_origin_column = horizon_origin_column

    def __eq__(self, other: object) -> bool:
        Contract.assert_type(other, "other", EvaluationConfigs)
        other = cast(EvaluationConfigs, other)
        return self.time_column_name == other.time_column_name and\
            self.time_series_id_column_names == other.time_series_id_column_names and\
            self.predictions_column_name == other.predictions_column_name and\
            self.ground_truths_column_name == other.ground_truths_column_name and\
            self.horizon_origin_column == other.horizon_origin_column

    @staticmethod
    def get_args_list() -> List[str]:
        """Return the list of arguments for this class."""
        return inspect.getfullargspec(EvaluationConfigs).args[1:]

    @staticmethod
    def get_evaluation_configs_from_forecasting_parameters(
            fp: ForecastingParameters,
            label_column_name: Optional[str] = None
    ) -> 'EvaluationConfigs':
        ground_truths_col = label_column_name
        return EvaluationConfigs(
            time_column_name=fp.time_column_name,
            time_series_id_column_names=fp.formatted_time_series_id_column_names,
            ground_truths_column_name=ground_truths_col
        )

    def get_all_columns(self) -> List[str]:
        """Get all the cols used in current eval configs."""
        all_cols = []
        if self.time_column_name:
            all_cols.append(self.time_column_name)
        if self.time_series_id_column_names:
            all_cols.extend(self.time_series_id_column_names)
        if self.ground_truths_column_name:
            all_cols.append(self.ground_truths_column_name)
        if self.predictions_column_name:
            all_cols.append(self.predictions_column_name)
        if self.horizon_origin_column:
            all_cols.append(self.horizon_origin_column)
        return all_cols

    def update_timeseries_id_columns(self, grains: List[str]) -> None:
        all_grains = [g for g in grains]
        if self.time_series_id_column_names:
            for col in self.time_series_id_column_names:
                if col not in all_grains:
                    all_grains.append(col)
        self.time_series_id_column_names = all_grains

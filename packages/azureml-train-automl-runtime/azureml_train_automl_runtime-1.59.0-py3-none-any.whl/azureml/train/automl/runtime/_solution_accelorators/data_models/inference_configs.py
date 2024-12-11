# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, cast, List, Optional, Union
import inspect
import re
import warnings

from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.train.automl.constants import InferenceTypes
from azureml.automl.core.shared.exceptions import ConfigException
from azureml.automl.core.shared.constants import TimeSeriesInternal
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    InvalidArgumentWithSupportedValues
)

from ..constants import HTSConstants


class InferenceConfigs:
    """
    Configs used for inference jobs.
    """

    _RE_FLOAT = re.compile('\\d*[.]\\d+')

    def __init__(
            self,
            partition_column_names: Optional[List[str]] = None,
            inference_type: Optional[str] = None,
            forecast_mode: Optional[str] = None,
            forecast_quantiles: Optional[List[Union[float, str]]] = None,
            allocation_method: Optional[str] = None,
            forecast_level: Optional[str] = None,
            train_run_id: Optional[str] = None,
            train_experiment_name: Optional[str] = None,
            forecast_step: int = 1,
            allow_multi_partitions: bool = False,
            skip_concat_results: bool = False,
            target_column_name: Optional[str] = None
    ):
        """
        Configs used for inference jobs.

        :param partition_column_names: The partition column names used for the setup step.
        :param inference_type: The inference type that inside the model. Possible values are forecast, predict and
            predict_proba. If None, then using forecast as default
        :param forecast_mode: The forecast mode. Possible values are recursive and rolling. If None, then using
            recursive as default.
        :param forecast_quantiles: The forecast quantiles for forecast inference.
        :param allocation_method: The allocation method used for HTS runs. Possible values are
            proportions_of_historical_average and average_historical_proportions.
        :param forecast_level: The forecast level that used in HTS jobs. This level must be within the hierarchy
            provided in the train jobs.
        :param train_experiment_name: The experiment name that used in the train.
        :param train_run_id: The train run id.
        :param forecast_step: The forecast steps used for rolling forecast.
        """
        self.partition_column_names = partition_column_names
        self.inference_type = inference_type
        self.forecast_mode = forecast_mode
        self._forecast_quantiles = forecast_quantiles
        self.allocation_method = allocation_method
        self.forecast_level = forecast_level
        self.train_run_id = train_run_id
        self.train_experiment_name = train_experiment_name
        self.forecast_step = forecast_step
        self.allow_multi_partitions = allow_multi_partitions
        self.skip_concat_results = skip_concat_results
        self.target_column_name = target_column_name

    @staticmethod
    def get_args_list() -> List[str]:
        """Return the list of arguments for this class."""
        args_list = inspect.getfullargspec(InferenceConfigs).args[1:]
        for idx, val in enumerate(args_list):
            if val == "forecast_quantiles":
                args_list[idx] = "_forecast_quantiles"
        return args_list

    def __eq__(self, other: object) -> bool:
        Contract.assert_type(other, "other", InferenceConfigs)
        other = cast(InferenceConfigs, other)
        return self.inference_type == other.inference_type and\
            self.partition_column_names == other.partition_column_names and\
            self.forecast_mode == other.forecast_mode and\
            self.forecast_quantiles == other.forecast_quantiles and\
            self.allocation_method == other.allocation_method and\
            self.forecast_level == other.forecast_level and\
            self.train_run_id == other.train_run_id and\
            self.train_experiment_name == other.train_experiment_name and\
            self.forecast_step == other.forecast_step and\
            self.allow_multi_partitions == other.allow_multi_partitions and\
            self.skip_concat_results == other.skip_concat_results and\
            self.target_column_name == other.target_column_name

    @property
    def forecast_quantiles(self) -> List[float]:
        """Get formatted forecast quantiles."""
        quantiles = []  # type: List[float]
        if not self._forecast_quantiles:
            return quantiles
        for q in self._forecast_quantiles:
            if not isinstance(q, str):
                quantiles.append(q)
            else:
                for v in InferenceConfigs._RE_FLOAT.findall(q):
                    quantiles.append(float(v))
        return quantiles

    def check_settings(self) -> None:
        """Check the settings of inference configs."""
        if self.inference_type == InferenceTypes.FORECAST or self.inference_type is None:
            self._check_forecast()
        elif self.inference_type == InferenceTypes.PREDICT or self.inference_type == InferenceTypes.PREDICT_PROBA:
            self._check_non_forecast()
        else:
            raise ConfigException._with_error(
                AzureMLError.create(
                    InvalidArgumentWithSupportedValues,
                    arguments="inference_type",
                    supported_values=",".join([
                        InferenceTypes.FORECAST, InferenceTypes.PREDICT, InferenceTypes.PREDICT_PROBA]),
                    reference_code=ReferenceCodes._MM_INFERENCE_BAD_TYPE
                )
            )

    def _check_forecast(self):
        if self.forecast_mode == TimeSeriesInternal.ROLLING:
            if self.forecast_quantiles is not None:
                warnings.warn("For rolling forecast, forecast_quantile value will be neglected.")
        elif self.forecast_mode == TimeSeriesInternal.RECURSIVE or self.forecast_mode is None:
            if self.forecast_step is not None:
                warnings.warn("For recursive forecast, forecast_step value will be neglected.")
        else:
            raise ConfigException._with_error(
                AzureMLError.create(
                    InvalidArgumentWithSupportedValues,
                    arguments="forecast_mode",
                    supported_values=",".join([
                        TimeSeriesInternal.ROLLING, TimeSeriesInternal.RECURSIVE]),
                    reference_code=ReferenceCodes._MM_FORECAST_BAD_MODE
                )
            )

    def _check_non_forecast(self):
        if self.forecast_mode is not None:
            warnings.warn("For regression models, forecast_mode value will be neglected.")
        if self.forecast_step is not None:
            warnings.warn("For regression models, forecast_step value will be neglected.")
        if self.forecast_quantiles is not None:
            warnings.warn("For regression models, forecast_quantile value will be neglected.")

    def _check_allocation_method_has_value(self):
        if self.allocation_method != HTSConstants.PROPORTIONS_OF_HISTORICAL_AVERAGE and \
                self.allocation_method != HTSConstants.AVERAGE_HISTORICAL_PROPORTIONS:
            raise ConfigException._with_error(
                AzureMLError.create(
                    InvalidArgumentWithSupportedValues,
                    arguments="allocation_method",
                    supported_values=",".join([
                        HTSConstants.PROPORTIONS_OF_HISTORICAL_AVERAGE, HTSConstants.AVERAGE_HISTORICAL_PROPORTIONS]),
                    reference_code=ReferenceCodes._MM_FORECAST_BAD_MODE
                )
            )

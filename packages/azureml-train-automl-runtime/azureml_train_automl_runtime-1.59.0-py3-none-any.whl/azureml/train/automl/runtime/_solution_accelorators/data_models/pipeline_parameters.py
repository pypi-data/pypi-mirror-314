# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging
from typing import Any, Dict, List, Optional, Union
from abc import ABC, abstractmethod

from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared.constants import TimeSeriesInternal
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    ArgumentBlankOrEmpty,
    DNNNotSupportedForManyModel,
    InvalidArgumentType,
    InvalidParameterSelection,
    QuantileForecastRollingModeNotSupported
)
from azureml.automl.core.shared.exceptions import (
    ConfigException,
    InvalidValueException,
    InvalidTypeException
)
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.train.automl.automlconfig import AutoMLConfig
from azureml.train.automl._constants_azureml import EnvironmentSettings


logger = logging.getLogger(__name__)


class TrainPipelineParameters(ABC):

    _MIN_TIMEOUT_DIFF = 300

    def __init__(self, automl_settings: Union[AutoMLConfig, Dict[str, Any]]):
        if isinstance(automl_settings, AutoMLConfig):
            self.automl_settings = automl_settings.as_serializable_dict()
            self.automl_settings["task"] = self.automl_settings.pop("task_type")
            if '_ignore_package_version_incompatibilities' in self.automl_settings:
                del self.automl_settings['_ignore_package_version_incompatibilities']
            if EnvironmentSettings.SCENARIO in self.automl_settings:
                del self.automl_settings[EnvironmentSettings.SCENARIO]
            if EnvironmentSettings.ENVIRONMENT_LABEL in self.automl_settings:
                del self.automl_settings[EnvironmentSettings.ENVIRONMENT_LABEL]
            if self.automl_settings.get("experiment_timeout_minutes", None) is not None:
                self.automl_settings["experiment_timeout_hours"] = round(
                    self.automl_settings.pop("experiment_timeout_minutes") / 60, 2
                )
        else:
            self.automl_settings = automl_settings
            message = "Please use 'AutoMLConfig' class with 'ForecastingParameters' class to define "\
                      "'automl_settings' instead of directly supplying 'automl_settings' dictionary "\
                      "in '{}' class.".format(type(self).__name__)
            logger.warning(message)

    def validate(self, run_invocation_timeout):
        if self.automl_settings.get("enable_dnn", False):
            raise ConfigException._with_error(
                AzureMLError.create(
                    DNNNotSupportedForManyModel,
                    reference_code=ReferenceCodes._VALIDATE_DNN_ENABLED_MANY_MODELS))
        if "experiment_timeout_hours" not in self.automl_settings:
            self.automl_settings["experiment_timeout_hours"] = round((
                run_invocation_timeout - self._MIN_TIMEOUT_DIFF) / 3600, 2)
            message = "As the experiment_timeout_hours must be smaller than run_invocation_timeout - "\
                      "{}, we have set the value to {} automatically as we didn't find it in the settings.".\
                      format(self._MIN_TIMEOUT_DIFF, self.automl_settings["experiment_timeout_hours"])
            logger.warning(message)


class InferencePipelineParameters(ABC):
    def __init__(self,
                 forecast_mode: str = TimeSeriesInternal.RECURSIVE,
                 step: int = 1,
                 forecast_quantiles: Optional[Union[float, List[float]]] = None):
        self.forecast_mode = forecast_mode
        self.step = step
        self.forecast_quantiles = [forecast_quantiles] if isinstance(forecast_quantiles, float) else forecast_quantiles

    @abstractmethod
    def validate(self):
        if self.forecast_mode not in (TimeSeriesInternal.RECURSIVE, TimeSeriesInternal.ROLLING):
            raise InvalidValueException._with_error(
                AzureMLError.create(
                    InvalidParameterSelection,
                    target="forecast_mode",
                    parameter="forecast_mode",
                    values=f"{TimeSeriesInternal.RECURSIVE} or {TimeSeriesInternal.ROLLING}"
                )
            )
        if not isinstance(self.step, int):
            raise InvalidTypeException._with_error(
                AzureMLError.create(
                    InvalidArgumentType,
                    target="step",
                    argument="step",
                    actual_type=type(self.step),
                    expected_types=int
                )
            )

        if self.step < 1:
            raise InvalidValueException._with_error(
                AzureMLError.create(
                    InvalidParameterSelection,
                    target="step",
                    parameter="step",
                    values=">=1"
                )
            )

        if self.forecast_quantiles is not None:
            if self.forecast_mode == TimeSeriesInternal.ROLLING:
                raise InvalidValueException._with_error(
                    AzureMLError.create(
                        QuantileForecastRollingModeNotSupported,
                        target="forecast_mode",
                    )
                )

            if not isinstance(self.forecast_quantiles, list) or \
               not all(isinstance(arg, float) for arg in self.forecast_quantiles):
                raise InvalidTypeException._with_error(
                    AzureMLError.create(
                        InvalidArgumentType,
                        target="forecast_quantiles",
                        argument="forecast_quantiles",
                        actual_type=type(self.forecast_quantiles),
                        expected_types='float, List[float]'
                    )
                )

            if len(self.forecast_quantiles) == 0:
                raise InvalidValueException._with_error(
                    AzureMLError.create(
                        ArgumentBlankOrEmpty,
                        argument_name='forecast_quantiles',
                        target='forecast_quantiles'
                    )
                )

            if not all((arg > 0. and arg < 1.) for arg in self.forecast_quantiles):
                raise InvalidValueException._with_error(
                    AzureMLError.create(
                        InvalidParameterSelection,
                        target="forecast_quantiles",
                        parameter="forecast_quantiles",
                        values=">0, <1"
                    )
                )

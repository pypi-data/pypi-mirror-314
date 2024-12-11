# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, Dict, List, Optional, Union

from azureml.train.automl.automlconfig import AutoMLConfig
from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.shared.exceptions import ValidationException
from azureml.automl.core.shared._diagnostics.automl_error_definitions import RollingForecastMissingTargetColumn
from azureml.automl.core.shared.constants import TimeSeriesInternal

from .pipeline_parameters import TrainPipelineParameters, InferencePipelineParameters


class ManyModelsTrainParameters(TrainPipelineParameters):
    """
    Parameters used for ManyModels train pipeline.

    :param automl_settings: The dict containing automl settings or ``AutoMLConfig`` object.
    :type automl_settings: azureml.train.automl.automlconfig.AutoMLConfig or dict
    :param partition_column_names: The names of columns used to group your models. For timeseries, the groups must
        not split up individual time-series. That is, each group must contain one or more whole time-series.
    :type partition_column_names: str
    """
    PARTITION_COLUMN_NAMES_KEY = "partition_column_names"

    def __init__(
        self,
        automl_settings: Union[AutoMLConfig, Dict[str, Any]],
        partition_column_names: str
    ):
        super(ManyModelsTrainParameters, self).__init__(automl_settings)

        self.partition_column_names = partition_column_names
        self._modify_automl_settings()

    def validate(self, run_invocation_timeout):
        """
        Validates the supplied parameters.

        :param run_invocation_timeout: Specifies timeout for each AutoML run.
        :type run_invocation_timeout: int
        """
        super(ManyModelsTrainParameters, self).validate(run_invocation_timeout)

    def _modify_automl_settings(self):
        self.automl_settings[ManyModelsTrainParameters.PARTITION_COLUMN_NAMES_KEY] = self.partition_column_names


class ManyModelsInferenceParameters(InferencePipelineParameters):
    """
    Parameters used for ManyModels inference pipeline.

    :param partition_column_names: The names of columns used to group your models. For timeseries, the groups must
        not split up individual time-series. That is, each group must contain one or more whole time-series.
    :type partition_column_names: str
    :param time_column_name: Time column name only if the inference dataset is a timeseries.
    :type time_column_name: str
    :param target_column_name: Target column name only if the inference dataset has the target column.
    :type target_column_name: str
    :param inference_type: Which inference method to use on the model. Possible values are
        'forecast', 'predict_proba', and 'predict'.
    :type inference_type: str
    :param forecast_mode: The type of forecast to be used, either 'rolling' or 'recursive', defaults to 'recursive'.
    :type forecast_mode: str
    :param step: Number of periods to advance the forecasting window in each iteration
        **(for rolling forecast only)**, defaults to 1.
    :type step: int
    :param forecast_quantiles: Optional list of quantiles to get forecasts for.
    :type: List[float]
    """

    def __init__(
            self,
            partition_column_names: str,
            time_column_name: Optional[str] = None,
            target_column_name: Optional[str] = None,
            inference_type: Optional[str] = None,
            forecast_mode: str = TimeSeriesInternal.RECURSIVE,
            step: int = 1,
            forecast_quantiles: Optional[Union[float, List[float]]] = None
    ):
        super(ManyModelsInferenceParameters, self).__init__(forecast_mode=forecast_mode,
                                                            step=step,
                                                            forecast_quantiles=forecast_quantiles)

        self.partition_column_names = partition_column_names
        self.time_column_name = time_column_name
        self.target_column_name = target_column_name
        self.inference_type = inference_type

    def validate(self):
        """Validates the supplied parameters."""
        super(ManyModelsInferenceParameters, self).validate()

        if self.forecast_mode == TimeSeriesInternal.ROLLING and self.target_column_name is None:
            raise ValidationException._with_error(
                AzureMLError.create(
                    RollingForecastMissingTargetColumn,
                    reference_code=ReferenceCodes._ROLLING_FORECAST_MISSING_TARGET_COLUMN
                )
            )

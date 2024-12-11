# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, cast, Dict, Optional, List

from azureml.core import Run

from ....constants import ManyModelsPipelineConstants
from ...automl_prs_run_base import AutoMLPRSRunBase
from ...automl_prs_driver_factory_v2 import AutoMLPRSDriverFactoryV2
from ..automl_prs_inference import AutoMLPRSInference, AutoMLPRSInferenceWrapper


class MMInferenceWrapperV2(AutoMLPRSInferenceWrapper):
    """The wrapper code for many models forecast."""

    def __init__(
            self,
            current_run_step: Optional[Run] = None,
            **kwargs: Any
    ) -> None:
        """
        The wrapper code for many models forecast.

        :param current_step_run: The current step run.
        """
        super().__init__(
            ManyModelsPipelineConstants.STEP_INFERENCE, current_run_step, **kwargs)
        self._partition_columns = cast(List[str], self._inference_configs.partition_column_names)

    def _get_run_class(self) -> AutoMLPRSRunBase:
        return MMInferenceV2(
            current_step_run=self.step_run,
            arguments_dict=self.arguments_dict,
            event_log_dim=self.event_logger_dim,
            partition_column_names=self._partition_columns,
            forecast_quantiles=self._inference_configs.forecast_quantiles,
            train_exp_name=self._inference_configs.train_experiment_name,
            allow_multi_partitions=self._inference_configs.allow_multi_partitions,
            inference_type=self._inference_configs.inference_type,
            forecast_mode=self._inference_configs.forecast_mode,
            step=self._inference_configs.forecast_step,
            target_column_name=self._inference_configs.target_column_name,
            train_run_id=self._inference_configs.train_run_id
        )


class MMInferenceV2(AutoMLPRSInference):
    """Inference class for many models v2."""
    def __init__(
            self,
            current_step_run: Run,
            arguments_dict: Dict[str, str],
            event_log_dim: Dict[str, str],
            partition_column_names: List[str],
            forecast_quantiles: Optional[List[float]],
            train_exp_name: Optional[str],
            train_run_id: Optional[str],
            allow_multi_partitions: bool,
            inference_type: Optional[str],
            forecast_mode: Optional[str],
            step: Optional[int],
            target_column_name: Optional[str],
            **kwargs: Any
    ) -> None:
        """
        Many Models inference V2 run class.

        :param current_step_run: A run object that the script is running.
        :param arguments_dict: The dict contains all the PRS run arguments.
        :param event_log_dim: The event log dim.
        """
        super().__init__(
            current_step_run,
            arguments_dict=arguments_dict, event_log_dim=event_log_dim,
            partition_column_names=partition_column_names,
            forecast_quantiles=forecast_quantiles,
            train_exp_name=train_exp_name,
            train_run_id=train_run_id,
            allow_multi_partitions=allow_multi_partitions,
            inference_type=inference_type,
            forecast_mode=forecast_mode,
            step=step,
            target_column_name=target_column_name,
            **kwargs
        )

    def get_automl_run_prs_scenario(self) -> str:
        """Get the run scenario."""
        return AutoMLPRSDriverFactoryV2.MM_INFERENCE

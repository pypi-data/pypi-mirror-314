# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, cast, Dict, List, Optional
import logging

from azureml.core import Run
from ..setup_step_wrapper import SetupStepWrapper
from ....data_models.evaluation_configs import EvaluationConfigs
from ....utilities import run_utilities as ru
from ....constants import PipelineConstants, ManyModelsPipelineConstants


logger = logging.getLogger(__name__)


class MMSetupWrapper(SetupStepWrapper):
    """The wrapper code for many models setup runs."""
    def __init__(self, current_step_run: Optional[Run] = None, is_train: bool = True, **kwargs: Any) -> None:
        super().__init__(
            ManyModelsPipelineConstants.STEP_SETUP if is_train else ManyModelsPipelineConstants.STEP_SETUP_INF,
            current_step_run, is_train=is_train, **kwargs
        )
        if is_train:
            self._partition_columns = self._get_partition_columns_from_settings(self.settings)
            self._allow_multi_partitions = self.settings.get(
                ManyModelsPipelineConstants.ALLOW_MULTI_PARTITIONS, False)
        else:
            partition_columns_from_train_run = None
            target_column_name_from_train_run = None
            try:
                self.settings = self._get_settings_from_run(
                    self.inference_configs.train_experiment_name, self.inference_configs.train_run_id)
                partition_columns_from_train_run = self._get_partition_columns_from_settings(self.settings)
                target_column_name_from_train_run = ru.get_label_column_name(self.settings)
            except Exception as e:
                if self.inference_configs.partition_column_names is None:
                    raise
                else:
                    self._print("Get latest train run met {}".format(e))
            if self.inference_configs.partition_column_names is None:
                self.inference_configs.partition_column_names = partition_columns_from_train_run
            if self.inference_configs.target_column_name is None:
                self.inference_configs.target_column_name = target_column_name_from_train_run
            self._partition_columns = cast(List[str], self.inference_configs.partition_column_names)
            self._allow_multi_partitions = self._get_allow_multi_partitions(self.settings)
            self._label_column_name = self.inference_configs.target_column_name
            self.inference_configs.allow_multi_partitions = self.allow_multi_partitions

    def _build_evaluation_configs(self) -> EvaluationConfigs:
        eval_conf = super()._build_evaluation_configs()
        if not self.is_train:
            eval_conf.update_timeseries_id_columns(self.partition_columns)
        return eval_conf

    @property
    def partition_columns(self) -> List[str]:
        return self._partition_columns

    @property
    def additional_params(self) -> List[str]:
        return [PipelineConstants.PARTITION_COLUMN_NAMES]

    @property
    def run_type(self) -> str:
        return PipelineConstants.RUN_TYPE_MM

    def _get_allow_multi_partitions(self, settings: Dict[str, Any]) -> bool:
        if self.is_train:
            return settings.get(  # type: ignore
                ManyModelsPipelineConstants.ALLOW_MULTI_PARTITIONS, False)
        else:
            _allow_multi_partitions_str = cast(
                Optional[str], self.arguments_dict.get(PipelineConstants.ARG_ALLOW_MULIT_PARTITIONS))
            _allow_multi_partitions_from_train = settings.get(
                ManyModelsPipelineConstants.ALLOW_MULTI_PARTITIONS, False)
            if _allow_multi_partitions_str is None:
                # no input, use the training default.
                return cast(bool, _allow_multi_partitions_from_train)
            else:
                _allow_multi_partitions = ru.str_or_bool_to_boolean(_allow_multi_partitions_str)
                if _allow_multi_partitions != _allow_multi_partitions_from_train:
                    self._print(
                        "The input config allow_multi_partitions is not the same as the one in the train."
                    )
                    logger.warning("Different settings for allow_multi_partitions in train and inference.")
                if _allow_multi_partitions:
                    self._print(
                        "Multi partitions in one fie is allowed. This needs the inference data have the same "
                        "partition presented as the train data to found the model. To avoid this, a new partition"
                        "can be created on top of the existing ones.")
                    logger.warning("allow_multi_partitions is enabled.")
                return _allow_multi_partitions

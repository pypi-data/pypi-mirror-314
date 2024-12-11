# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, cast, Dict, Optional
from logging import Logger

from azureml._restclient.experiment_client import ExperimentClient
from azureml._restclient.models.create_run_dto import CreateRunDto
from azureml._restclient.models.run_type_v2 import RunTypeV2

from azureml.core import Run

from ..data_models.arguments import Arguments
from .automl_prs_driver_base import AutoMLPRSDriverBase
from .steps.hts.hts_data_aggregation_driver_v2 import HTSDataAggregationDriverV2
from .steps.hts.hts_automl_train_driver_v2 import HTSAutoMLTrainDriverV2
from .steps.hts.hts_inference_driver_v2 import HTSInferenceDriverV2
from .steps.many_models.mm_automl_train_driver_v2 import MMAutoMLTrainDriverV2
from .steps.many_models.mm_inference_driver_v2 import MMInferenceDriverV2


class AutoMLPRSDriverFactoryV2:
    HTS_DATA_AGGREGATION = "HTSDataAggregationV2"
    HTS_AUTOML_TRAIN = "HTSAutoMLTrainV2"
    HTS_INFERENCE = "HTSInferenceV2"
    MM_AUTOML_TRAIN = "MMAutoMLTrainV2"
    MM_INFERENCE = "MMInferenceV2"

    AUTOML_HTS_TRAIN_TRAIT = "AutoMLHTSTrain"
    AUTOML_HTS_INFERENCE_TRAIT = "AutoMLHTSInference"
    AUTOML_MANY_MODELS_TRAIN_TRAIT = "AutoMLManyModelsTrain"
    AUTOML_MANY_MODELS_INFERENCE_TRAIT = "AutoMLManyModelsInference"

    SCENARIOS = {
        HTS_DATA_AGGREGATION, HTS_AUTOML_TRAIN, HTS_INFERENCE,
        MM_AUTOML_TRAIN, MM_INFERENCE
    }

    @staticmethod
    def add_run_trait(
            scenario_trait: str,
            current_step_run: Run
    ) -> None:
        """
        Add trait based on the scenario to the run for telemetry purposes.

        :param scenario_trait: The MM/HTS training or inference run.
        :param current_step_run: The current PRS run.
        """
        create_run_dto = CreateRunDto(current_step_run.id, run_type_v2=RunTypeV2(traits=[scenario_trait]))

        experiment = current_step_run.experiment
        experiment_client = ExperimentClient(
            experiment.workspace.service_context,
            experiment.name,
            experiment_id=experiment.id
        )
        experiment_client.create_run(current_step_run.id, create_run_dto=create_run_dto)

    @staticmethod
    def get_automl_prs_driver(
            scenario: str,
            current_step_run: Run,
            logger: Logger,
            args: Arguments,
            automl_settings: Optional[Dict[str, Any]] = None,
    ) -> AutoMLPRSDriverBase:
        """
        Get AutoML PRS driver code based on scenario.

        :param scenario: The PRS run scenario.
        :param current_step_run: The current PRS run.
        :param logger: The logger.
        :param args: The args used in the PRS run.
        :param automl_settings: The automl settings dict.
        :return: An AutoMLPRSDriverBase that used in PRS step.
        """
        driver = None  # type: Optional[AutoMLPRSDriverBase]
        if scenario == AutoMLPRSDriverFactoryV2.HTS_DATA_AGGREGATION:
            driver = HTSDataAggregationDriverV2(
                current_step_run, cast(Dict[str, Any], automl_settings), args
            )
        elif scenario == AutoMLPRSDriverFactoryV2.HTS_AUTOML_TRAIN:
            driver = HTSAutoMLTrainDriverV2(current_step_run, cast(Dict[str, Any], automl_settings), args)
            AutoMLPRSDriverFactoryV2.add_run_trait(
                AutoMLPRSDriverFactoryV2.AUTOML_HTS_TRAIN_TRAIT, current_step_run)
        elif scenario == AutoMLPRSDriverFactoryV2.MM_AUTOML_TRAIN:
            driver = MMAutoMLTrainDriverV2(current_step_run, cast(Dict[str, Any], automl_settings), args)
            AutoMLPRSDriverFactoryV2.add_run_trait(
                AutoMLPRSDriverFactoryV2.MM_AUTOML_TRAIN, current_step_run)
        elif scenario == AutoMLPRSDriverFactoryV2.HTS_INFERENCE:
            driver = HTSInferenceDriverV2(current_step_run, args)
            AutoMLPRSDriverFactoryV2.add_run_trait(
                AutoMLPRSDriverFactoryV2.AUTOML_HTS_INFERENCE_TRAIT, current_step_run)
        elif scenario == AutoMLPRSDriverFactoryV2.MM_INFERENCE:
            driver = MMInferenceDriverV2(current_step_run, args)
            AutoMLPRSDriverFactoryV2.add_run_trait(
                AutoMLPRSDriverFactoryV2.AUTOML_MANY_MODELS_INFERENCE_TRAIT, current_step_run)

        driver = cast(AutoMLPRSDriverBase, driver)

        return driver

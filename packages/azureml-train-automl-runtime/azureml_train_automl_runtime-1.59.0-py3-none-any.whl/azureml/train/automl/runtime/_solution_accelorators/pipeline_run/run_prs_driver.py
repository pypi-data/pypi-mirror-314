# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging
import os
import sys

from azureml.core import Run, Experiment, Workspace
from azureml.train.automl.runtime._many_models.automl_prs_driver_factory import AutoMLPRSDriverFactory

from azureml.train.automl.runtime._solution_accelorators.data_models.arguments import Arguments
from azureml.train.automl.runtime._solution_accelorators.data_models.metadata_file_handler import MetadataFileHandler
from azureml.train.automl.runtime._solution_accelorators.pipeline_run.automl_prs_driver_factory_v2 import (
    AutoMLPRSDriverFactoryV2
)

# TODO: Remove once Batch AI has fixed this issue.
# Exclude mounted blobfuse folders from sys.path, preventing Python from scanning
# folders in the blob container when resolving import statements. This significantly reduces traffic
# to the storage account.

sys.path = [p for p in sys.path if not p.startswith('/mnt/batch')]

logger = logging.getLogger(__name__)


def run_prs_driver() -> None:
    """Run AutoML PRS driver codes."""
    data_file_path = sys.argv[1]
    data_dir = sys.argv[2]
    prs_scenario = sys.argv[3]
    output_file = sys.argv[4]
    metadata_file_handler = MetadataFileHandler(data_dir)
    args = metadata_file_handler.load_args()
    automl_settings = metadata_file_handler.load_automl_settings()
    run_dto = metadata_file_handler.load_run_dto()
    try:
        experiment, run_id = Run._load_scope()
    except Exception as e:
        # This section is used by local emulator
        print(e)
        subscription_id = os.environ['AZUREML_ARM_SUBSCRIPTION']
        resource_group = os.environ["AZUREML_ARM_RESOURCEGROUP"]
        experiment_name = os.environ["AZUREML_ARM_PROJECT_NAME"]
        workspace_name = os.environ["AZUREML_ARM_WORKSPACE_NAME"]
        run_id = os.environ['AZUREML_RUN_ID']
        ws = Workspace(subscription_id, resource_group, workspace_name)
        experiment = Experiment(ws, experiment_name)

    current_step_run = Run(experiment, run_id, _run_dto=run_dto)
    if prs_scenario in AutoMLPRSDriverFactoryV2.SCENARIOS:
        prs_driver = AutoMLPRSDriverFactoryV2.get_automl_prs_driver(
            prs_scenario, current_step_run, logger, args, automl_settings)
    else:
        # default to use V1 scenario
        prs_driver = AutoMLPRSDriverFactory.get_automl_prs_driver(
            prs_scenario, current_step_run, logger, args, automl_settings)
    logs = prs_driver.run(data_file_path, output_file)
    metadata_file_handler.write_logs_to_disk(logs)


if __name__ == '__main__':
    run_prs_driver()

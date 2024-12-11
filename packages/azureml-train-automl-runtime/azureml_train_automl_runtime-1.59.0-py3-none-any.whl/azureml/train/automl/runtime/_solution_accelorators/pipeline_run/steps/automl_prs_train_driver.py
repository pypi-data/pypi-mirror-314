# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, cast, Dict, List, Optional, Tuple
from abc import abstractmethod
import logging
import os
import pandas as pd
from datetime import datetime

from azureml.automl.core.shared import constants
from azureml.automl.core.shared.exceptions import (AutoMLException, ClientException)
from azureml.automl.core.shared.utilities import get_error_code
from azureml.automl.core._logging.event_logger import EventLogger
from azureml.core import Run
from azureml.core.model import Model
from azureml.exceptions import AzureMLException
from azureml._restclient.constants import RunStatus
from azureml.automl.core.shared import logging_utilities

from ...data_models.arguments import Arguments
from ..automl_prs_driver_base import AutoMLPRSDriverBase
from ...data_models.status_record import StatusRecord
from ...constants import PipelineConstants
from ...utilities.file_utilities import dump_object_to_json
from ...utilities.run_utilities import get_automl_config


logger = logging.getLogger(__name__)


class AutoMLPRSTrainDriver(AutoMLPRSDriverBase):
    """The driver code for Many models AutoML train run."""
    MODEL_TAG_DICT_HASH = 'Hash'
    MODEL_TAG_DICT_DATA_TAGS = 'DataTags'
    MODEL_TAG_DICT_RUN_ID = 'RunId'
    MODEL_TAG_DICT_STEP_RUN_ID = 'StepRunId'
    MODEL_TAG_DICT_EXP_NAME = 'ExperimentName'
    MODEL_TAG_DICT_MODEL_TYPE = "ModelType"
    MODEL_TAG_DICT_AUTOML = "AutoML"
    MODEL_TAG_DICT_INPUT_DATA = "InputData"

    def __init__(
            self,
            current_step_run: Run,
            automl_settings: Dict[str, Any],
            args: Arguments
    ):
        """The driver code for Many models AutoML train run."""
        super(AutoMLPRSTrainDriver, self).__init__(current_step_run)
        self.automl_settings = automl_settings
        self.args = args
        self._automl_run_properties: Dict[str, Any] = {'many_models_run': True}
        self.event_logger_additional_fields = cast(Dict[str, str], args.event_logger_dim)
        self.event_logger = EventLogger(run=self.current_step_run)
        self.output_path = cast(str, args.output_path)
        os.environ['AUTOML_IGNORE_PACKAGE_VERSION_INCOMPATIBILITIES'] = "True"
        self.partition_column_names = cast(List[str], args.partition_column_names)

    def run(self, input_data_file: str, output_data_file: str) -> Any:
        """Run the data file."""
        self._console_writer.println(output_data_file)
        timestamp_column = self.automl_settings.get('time_column_name', None)

        model_name = ''
        current_run = None
        tags_dict = {}  # type: Dict[str, str]

        date1 = datetime.now()
        self._console_writer.println('start (' + input_data_file + ') ' + str(datetime.now()))

        file_name_with_extension = os.path.basename(input_data_file)
        file_name, file_extension = os.path.splitext(file_name_with_extension)

        parse_date = [timestamp_column] if timestamp_column is not None else None

        try:
            data = self.read_input_data(input_data_file, parse_date)
            self.pre_run(data, file_name_with_extension)
            tags_dict = self.get_tag_dict(file_name_with_extension)

            if self.args.retrain_failed_models:
                trained_model_logs = self.get_trained_models_logs(tags_dict, file_name, date1)
                if trained_model_logs is not None:
                    return trained_model_logs

            fitted_model, current_run, best_child_run = self._train_model(
                input_data_file, data, self.automl_settings, self.current_step_run)

            model_name = self.get_model_name(
                tags_dict[AutoMLPRSTrainDriver.MODEL_TAG_DICT_HASH], self.run_type)

            logs = self.post_run(
                tags_dict, best_child_run, current_run, fitted_model, date1, input_data_file, model_name
            )
        except (ClientException, AzureMLException, AutoMLException) as error:
            logs = self.post_run_exception(
                tags_dict, current_run, date1, input_data_file, model_name, error
            )

        return logs

    def _train_model(
            self,
            file_path: str,
            data: pd.DataFrame,
            automl_settings: Dict[str, Any],
            current_step_run: Run) -> Tuple[Model, Run, Run]:
        """
        Train AutoML model.

        :param file_path: The path to training file.
        :param data: The training data.
        :param automl_settings: The settings for training.
        :param current_step_run: current run.
        :return: the tuple with fitted model, local parent run and
                 the best child run.
        """
        file_name = os.path.basename(file_path)
        self._console_writer.println(file_name)
        self._console_writer.println("in train_model")
        self._console_writer.println('data')
        self._console_writer.println(str(data.head(5)))
        self._console_writer.println(str(automl_settings))
        automl_settings['training_data'] = data
        automl_config = get_automl_config(automl_settings, [])

        self._console_writer.println("submit_child")
        local_run = current_step_run.submit_child(automl_config, show_output=True)

        self._console_writer.println(str(local_run))

        best_child_run, fitted_model = local_run.get_output()

        return fitted_model, local_run, best_child_run

    def get_tag_dict(self, file_name_with_extension: str) -> Dict[str, str]:
        """
        Get the tags, which will be set to model.

        :param file_name_with_extension: The
        :return: The dictionary with tags.
        """
        tags_dict = {AutoMLPRSTrainDriver.MODEL_TAG_DICT_MODEL_TYPE: AutoMLPRSTrainDriver.MODEL_TAG_DICT_AUTOML}
        tags_dict.update(self._automl_run_properties[AutoMLPRSTrainDriver.MODEL_TAG_DICT_DATA_TAGS])

        tags_dict.update({AutoMLPRSTrainDriver.MODEL_TAG_DICT_INPUT_DATA: file_name_with_extension})
        tags_dict.update({AutoMLPRSTrainDriver.MODEL_TAG_DICT_STEP_RUN_ID: self.current_step_run.id})
        tags_dict.update({AutoMLPRSTrainDriver.MODEL_TAG_DICT_RUN_ID: self.current_step_run.parent.id})
        tags_dict.update({AutoMLPRSTrainDriver.MODEL_TAG_DICT_EXP_NAME: self.current_step_run.experiment.name})

        tags_dict.update({AutoMLPRSTrainDriver.MODEL_TAG_DICT_HASH: AutoMLPRSDriverBase.get_hashed_model_string_v2(
            self._automl_run_properties[AutoMLPRSTrainDriver.MODEL_TAG_DICT_DATA_TAGS],
            self.partition_column_names
        )})

        return tags_dict

    def modify_run_properties(self, data: pd.DataFrame, file_name_with_extension: str) -> None:
        """
        Modify AutoML run properties based on input data and input file name.

        :param data: Input data.
        :param file_name_with_extension: The input data file name.
        """
        group_columns_dict = AutoMLPRSTrainDriver._get_partition_data_tag_dict(data, self.partition_column_names)
        self._automl_run_properties.update({
            AutoMLPRSTrainDriver.MODEL_TAG_DICT_DATA_TAGS: group_columns_dict,
            PipelineConstants.PROPERTIES_INPUT_FILE: file_name_with_extension,
            PipelineConstants.PROPERTIES_RUN_TYPE: self.run_type})

    def get_trained_models_logs(
            self, tags_dict: Dict[str, str], file_name: str, start_time: datetime
    ) -> Optional[List[Any]]:
        """
        Return the logging record about the models found by tags.

        :param tags_dict: The dictionary of tags to get the models.
        :param file_name: Input file name.
        :param start_time: the start of training.
        :return: If the model can be found, return the logs, else return None.
        """
        self._console_writer.println('querying for existing models')
        try:
            tags = [[k, v] for k, v in tags_dict.items()]
            models = Model.list(self.current_step_run.experiment.workspace, tags=tags, latest=True)

            if models:
                self._console_writer.println(
                    "Model already exists for the dataset {}. Skipping now.".format(models[0].name))
                return self._compose_logs(file_name, start_time, models[0])
            else:
                self._console_writer.println('No models can be found.')
        except Exception as error:
            self._console_writer.println('Failed to list the models. ' + 'Error message: ' + str(error))
        return None

    def pre_run(self, data: pd.DataFrame, file_name_with_extension: str) -> None:
        """
        Pre-automl training run execution.

        :param data: Input data.
        :param file_name_with_extension: The input file name.
        """
        self.modify_run_properties(data, file_name_with_extension)

    def post_run(
            self, tags_dict: Dict[str, str], best_child_run: Run, current_run: Run, fitted_model: Model,
            start_time: datetime, input_data_file: str, model_name: str
    ) -> List[Any]:
        """Register the model and generating the logs."""

        current_run.add_properties({
            k: str(self._automl_run_properties[k])
            for k in self._automl_run_properties
        })

        logs = []  # type: List[Any]

        try:
            self._console_writer.println('done training')

            self._console_writer.println('Trained best model ' + model_name)

            self._console_writer.println(str(best_child_run))
            self._console_writer.println(str(fitted_model))
            self._console_writer.println(model_name)

            self._console_writer.println('register model')

            best_child_run.register_model(
                model_name=model_name, model_path=constants.MODEL_PATH, description='AutoML', tags=tags_dict)
            self._console_writer.println('Registered ' + model_name)
        except Exception as error:
            raise AzureMLException('Failed to register the model. Error message: {}'.format(error)) from error

        status = self._get_run_status(current_run)

        if status is not None and status.lower() in {RunStatus.COMPLETED.lower(), RunStatus.CANCELED.lower()}:
            self._record_successful_run(input_data_file, current_run)
        else:
            self._record_failed_run(input_data_file, current_run)

        self._console_writer.println("Training and model registration done.")
        return logs

    def post_run_exception(
            self, tags_dict: Dict[str, str], current_run: Run,
            start_time: datetime, input_data_file: str, model_name: str, error: BaseException
    ) -> List[Any]:
        """Handle the exception the AutoML run meet."""
        logs = []  # type: List[Any]
        date2 = datetime.now()
        error_message = 'Failed to train the model. ' + 'Error : ' + str(error)

        logs.append('AutoML')
        logs.append(input_data_file)
        logs.append('Failed')

        if current_run:
            logs.append(current_run.id)
            logs.append(current_run.get_status())
        else:
            logs.append(current_run)
            logs.append('Failed')

        logs.append(model_name)
        logs.append(tags_dict)
        logs.append(str(start_time))
        logs.append(str(date2))
        if isinstance(error, AutoMLException):
            logs.append(error.error_type)
        else:
            logs.append(None)
        logs.append(get_error_code(error))
        logs.append(error_message)

        self._console_writer.println(error_message)
        self._console_writer.println('ending (' + input_data_file + ') ' + str(date2))

        error_type = StatusRecord.get_error_type(error)
        failed_reason = "Pipeline parent run {}. failed reason: {}\n\n".format(
            self.current_step_run.id, error)
        self._console_writer.println(
            "Pipeline parent run {}. failed reason: {}\n\n".format(self.current_step_run.id, error))

        logging_utilities.log_traceback(error, logger)

        self._record_failed_run(input_data_file, current_run, error_type, failed_reason)

        return logs

    def _record_successful_run(self, input_data_file: str, local_run: Optional[Run] = None) -> None:
        """Record the successful run and save the status record"""
        run_id = self._get_run_id(local_run)
        status_record = StatusRecord(
            self._data_identifier, StatusRecord.SUCCEEDED,
            os.path.basename(input_data_file), run_id)
        self._save_status_records_to_file(
            status_record,
            os.path.join(self.output_path, self.get_run_info_filename(self._get_file_name(input_data_file))))

    def _record_failed_run(
            self,
            input_data_file: str,
            local_run: Optional[Run] = None,
            error_type: Optional[str] = None,
            failed_reason: Optional[str] = None) -> None:
        # There are 2 types of exceptions: 1) exceptions raises during the run and
        # 2) exceptions not raise but the run failed. We will treat the second one as system error now.
        if error_type is None and failed_reason is None:
            error_type = StatusRecord.SYSTEM_ERROR
            if local_run is not None:
                failed_reason = local_run.get_details().get("error")
        status_record = StatusRecord(
            self._data_identifier, StatusRecord.FAILED, os.path.basename(input_data_file),
            self._get_run_id(local_run), error_type=error_type, error_message=failed_reason
        )

        self._save_status_records_to_file(
            status_record,
            os.path.join(self.output_path, self.get_run_info_filename(self._get_file_name(input_data_file))))

    def _save_status_records_to_file(self, status_record: StatusRecord, file_path: str) -> None:
        dump_object_to_json(status_record, file_path)

    def _get_run_status(self, current_run: Run) -> Optional[str]:
        return None if current_run is None else current_run.status

    def _get_run_id(self, current_run: Run) -> Optional[str]:
        return None if current_run is None else current_run.id

    def _get_file_name(self, filename_with_path: str) -> str:
        file_name, _ = os.path.splitext(os.path.basename(filename_with_path))
        return file_name

    @property
    def _data_identifier(self) -> List[str]:
        return self._get_data_identifier(
            self._automl_run_properties[AutoMLPRSTrainDriver.MODEL_TAG_DICT_DATA_TAGS],
            self.partition_column_names
        )

    def _compose_logs(
            self,
            input_data_file: str,
            start_time: datetime,
            model: Optional[Model] = None
    ) -> List[Any]:
        logs = [
            'AutoML', input_data_file, None, None,
            model.name if model is not None else None,
            model.tags if model is not None else None, start_time, datetime.now(), None, None, None
        ]  # type: List[Any]
        return logs

    @property
    @abstractmethod
    def run_type(self) -> str:
        """The run type of the driver."""
        raise NotImplementedError

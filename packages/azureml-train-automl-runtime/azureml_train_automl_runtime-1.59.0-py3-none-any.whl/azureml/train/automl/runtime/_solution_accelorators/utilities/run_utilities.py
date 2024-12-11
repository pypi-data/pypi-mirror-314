# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Dict, Any, List, Optional, cast, Union
import copy
import yaml
import json
from random import randint
import logging
import os
from time import sleep
import argparse
import hashlib

from azureml.core import Run
from azureml.train.automl.constants import HTSConstants
from azureml.automl.core.featurization import FeaturizationConfig
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared.exceptions import UserException
from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.constants import SupportedTransformers
from azureml.train.automl.automlconfig import AutoMLConfig
from azureml.train.automl import _azureautomlsettings
from azureml.automl.core.automl_base_settings import AutoMLBaseSettings
from azureml.automl.core.shared._diagnostics.automl_error_definitions import HierarchyAllParallelRunsFailedByUserError
from azureml.train.automl._hts.hts_client_utilities import (
    get_hierarchy,
    get_training_level,
    get_hierarchy_to_training_level,
    get_label_column_name,
    get_forecasting_parameters,
    get_latest_successful_training_run,
    load_settings_dict_file,
    validate_hierarchy_settings,
    validate_forecasting_settings,
    validate_column_consistent,
    _convert_iso_datetime_str
)

from ..data_models.status_record import StatusRecord
from ..constants import PipelineConstants


logger = logging.getLogger(__name__)


def stagger_randomized_secs(arguments_dict: Dict[str, Any]) -> None:
    """
    Stagger the node for the a randomized seconds based on preocess_count_per_node and nodes_count.

    :param arguments_dict: The arguements_dict contains all the running arguemnts.
    """
    max_concurrent_runs = arguments_dict.get("process_count_per_node", 10)
    node_count = int(arguments_dict.get(HTSConstants.NODES_COUNT, 1))
    traffic_ramp_up_period_in_seconds = min(max_concurrent_runs * node_count, 600)
    worker_sleep_time_in_seconds = randint(1, traffic_ramp_up_period_in_seconds)
    print("Traffic ramp up period: {} seconds".format(traffic_ramp_up_period_in_seconds))
    print(
        "Sleeping this worker for {} seconds to stagger traffic "
        "ramp-up...".format(worker_sleep_time_in_seconds))
    sleep(worker_sleep_time_in_seconds)


def get_arguments_dict(
        script_scenario: str,
        is_parallel_run_step: bool = False,
        sdk_version: str = PipelineConstants.SDK_V1,
        argv: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Get the arguments dict for the driver script.

    :param script_scenario: The different scenarios.
    :param is_parallel_run_step: If the driver scripts is a pipeline run. Pipeline run will add some arguments other
                                 the the default ones.
    :param sdk_version: The SDK version of the step.
    :return: Dict[str, str]
    """
    print("Loading arguments for scenario {} using {}".format(script_scenario, sdk_version))
    argument_dict = {}
    parser = argparse.ArgumentParser("Parsing input arguments.")
    if sdk_version == PipelineConstants.SDK_V1:
        scripts_scenario_arg_dict = HTSConstants.HTS_SCRIPTS_SCENARIO_ARG_DICT
        output_args_dict = HTSConstants.HTS_OUTPUT_ARGUMENTS_DICT
    else:
        scripts_scenario_arg_dict = PipelineConstants.SCRIPTS_SCENARIO_ARG_DICT
        output_args_dict = PipelineConstants.OUTPUT_ARGUMENTS_DICT
    for arg in scripts_scenario_arg_dict[script_scenario]:
        print("adding argument {}".format(arg))
        if sdk_version == PipelineConstants.SDK_V2 and arg in PipelineConstants.LIST_ARGS:
            parser.add_argument(arg, dest=output_args_dict[arg], required=False, nargs="+", default=None)
        else:
            kwargs = HTSConstants.HTS_ARGUMENTS_PARSE_KWARGS_DICT.get(arg, {})
            parser.add_argument(arg, dest=output_args_dict[arg], required=False, **kwargs)
    parser.add_argument(
        "--process_count_per_node", default=1, type=int, help="number of processes per node", required=False)

    args, _ = parser.parse_known_args(argv)
    if is_parallel_run_step:
        # process_count_per_node and nodes_count can be used for help with concurrency
        argument_dict["process_count_per_node"] = args.process_count_per_node

    for arg in scripts_scenario_arg_dict[script_scenario]:
        argument_dict[arg] = getattr(args, output_args_dict[arg])
    print("Input arguments dict is {}".format(argument_dict))

    return argument_dict


def get_model_hash(str_list: List[str]) -> str:
    """
    Get the model hash from a str list.

    :param str_list: The str list using for hast.
    :return: str
    """
    model_string = '_'.join(str(v) for v in str_list).lower()
    sha = hashlib.sha256()
    sha.update(model_string.encode())
    return sha.hexdigest()


def check_parallel_runs_status(status_records: List[StatusRecord], parallel_step: str, uploaded_file: str) -> None:
    """Check the results of all parallel runs."""
    Contract.assert_true(
        status_records is not None and len(status_records) > 0, message="Status records should not be empty.",
        reference_code=ReferenceCodes._HTS_RUNTIME_EMPTY_STATUS_RECORDS, log_safe=True)
    if all([sr.status == StatusRecord.FAILED for sr in status_records]):
        Contract.assert_true(
            all([sr.error_type == StatusRecord.USER_ERROR for sr in status_records]),
            message="Status records should not contain system errors.", log_safe=True,
            reference_code=ReferenceCodes._HTS_RUNTIME_STATUS_RECORDS_SYSTEM_ERROR
        )
        raise UserException._with_error(
            AzureMLError.create(
                HierarchyAllParallelRunsFailedByUserError,
                target="status_record", parallel_step=parallel_step, file_name=uploaded_file,
                reference_code=ReferenceCodes._HTS_RUNTIME_STATUS_RECORDS_USER_ERROR
            )
        )


def get_input_dataset_name(input_dataset_name: Optional[str]) -> str:
    """
    Get the input dataset name.

    :param input_dataset_name: The input dataset name.
    :return: return HTSConstants.HTS_INPUT is input_input_dataset_name is None or '' or
        HTSConstants.DEFAULT_ARG_VALUE.
    """
    if input_dataset_name is None or input_dataset_name == '' or input_dataset_name == HTSConstants.DEFAULT_ARG_VALUE:
        return cast(str, HTSConstants.HTS_INPUT)
    return input_dataset_name


def get_settings(input_config: str) -> Dict[str, Any]:
    try:
        logger.info("Try to load yml file")
        with open(input_config) as f:
            settings = _reconstruct_yml_settings(yaml.safe_load(f))
    except Exception as e:
        print(e)
        logger.warning("Load yml file failed, falling back to load json file instead.")
        settings = load_settings_dict_file(input_config)
    # overwrite the params used for MM/HTS runs
    settings["track_child_runs"] = False
    settings["many_models"] = True
    return settings


def _reconstruct_yml_settings(settings: Dict[str, Any]) -> Dict[str, Any]:
    mapped_new_params = {
        'timeout_minutes': 'experiment_timeout_minutes',
        'max_trials': 'iterations',
        'trial_timeout': 'iteration_timeout_minutes',
        'trial_timeout_minutes': 'iteration_timeout_minutes',
        'target_column_name': 'label_column_name',
        'max_concurrent_trials': 'max_concurrent_iterations',
        'max_cores_per_trial': 'max_cores_per_iteration',
        'enable_early_termination': 'enable_early_stopping',
        'enable_model_explainability': 'model_explainability',
        'allowed_training_algorithms': 'allowed_models',
        'frequency': 'freq',
        'enable_dnn_training': 'enable_dnn',
        'blocked_training_algorithms': 'blocked_models',
        'enable_vote_ensemble': 'enable_voting_ensemble',
        'exit_score': 'experiment_exit_score',
        'log_verbosity': 'verbosity',
        'column_name_and_types': '_column_purposes',
        'blocked_transformers': '_blocked_transformers',
        'transformer_params': '_transformer_params',
        'drop_columns': '_drop_columns',
        'imputer': SupportedTransformers.Imputer
    }
    expand_params = {"limits", "forecasting", "training"}
    exclude_params = {
        "$schema",
        "experiment_name", "description", "compute", "training_data", "test_data", "validation_data", "type"}
    new_settings: Dict[str, Any] = {}
    settings = copy.deepcopy(settings)
    for k in exclude_params:
        if k in settings:
            del settings[k]
    if 'featurization' in settings and settings.get('featurization') is not None:
        new_settings['featurization'] = _convert_yml_featurization_to_dict(
            cast(dict, settings['featurization']), mapped_new_params)
        del settings['featurization']

    for param in expand_params:
        if param in settings:
            for k, v in settings[param].items():
                new_settings[_get_converted_settings(k, mapped_new_params)] = v
            del settings[param]
    for k, v in settings.items():
        if k != 'log_verbosity':
            new_settings[_get_converted_settings(k, mapped_new_params)] = v
        else:
            verbosity_mappings = {
                'notset': 0, 'debug': 10, 'info': 20, 'warning': 30, 'error': 40, 'critical': 50}
            new_settings[_get_converted_settings(k, mapped_new_params)] = verbosity_mappings.get(v.lower(), 30)
    return new_settings


def _convert_yml_featurization_to_dict(
        featurization_settings: Dict[str, Any], convert_dict: Dict[str, str]
) -> Optional[Union[str, Dict[str, Any]]]:
    if featurization_settings.get('mode') != 'custom':
        return featurization_settings.get('mode')
    del featurization_settings['mode']
    new_settings: Dict[str, Any] = {}
    if 'transformer_params' in featurization_settings:
        params_key = _get_converted_settings('transformer_params', convert_dict)
        new_settings[params_key] = {}
        for k, v in featurization_settings['transformer_params'].items():
            new_settings[params_key][_get_converted_settings(k, convert_dict)] = _covert_yml_transformer(v)
        del featurization_settings['transformer_params']

    for k, v in featurization_settings.items():
        new_settings[_get_converted_settings(k, convert_dict)] = copy.deepcopy(v)
    return new_settings


def _get_converted_settings(settings_param: str, convert_dict: Dict[str, str]) -> str:
    return convert_dict.get(settings_param, settings_param)


def _covert_yml_transformer(transformer_settings: List[Dict[str, Any]]) -> List[List[Any]]:
    return [[setting['fields'], setting['parameters']] for setting in transformer_settings]


def str_or_bool_to_boolean(v: Union[str, bool]) -> bool:
    """
    Convert the value which can be string or boolean to boolean.

    :param str_or_bool: the value, which can be string or boolean.
    :return: the corresponding boolean value.
    """
    if v is None:
        return False
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'True', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'False', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_pipeline_run(run: Optional[Run] = None) -> Run:
    """
    Get the pipeline run.

    :param run: If run is passed in then use the property of that run,
    :return: Run
    """
    if run is None:
        run = Run.get_context()
    parent_run = Run(run.experiment, run.properties.get('azureml.pipelinerunid'))
    return parent_run


def get_parsed_metadata_from_artifacts(run: Run, output_dir: str) -> Dict[str, Any]:
    """
    Get the metadata parsed as a dict from artifacts.

    :param run: The pipeline run.
    :param output_dir: The temp output dir.
    :return: Dict[str, Any]
    """
    run.download_file(HTSConstants.HTS_FILE_PROPORTIONS_METADATA_JSON, output_dir)
    raw_metadata_file = os.path.join(output_dir, HTSConstants.HTS_FILE_PROPORTIONS_METADATA_JSON)
    with open(raw_metadata_file) as f:
        raw_metadata = json.load(f)

    parsed_metadata = {}
    for metadata_node in raw_metadata[HTSConstants.METADATA_JSON_METADATA]:
        node_id = metadata_node[HTSConstants.NODE_ID]
        parsed_metadata[node_id] = {
            HTSConstants.PROPORTIONS_OF_HISTORICAL_AVERAGE:
                metadata_node[HTSConstants.PROPORTIONS_OF_HISTORICAL_AVERAGE],
            HTSConstants.AVERAGE_HISTORICAL_PROPORTIONS:
                metadata_node[HTSConstants.AVERAGE_HISTORICAL_PROPORTIONS]
        }
    os.remove(raw_metadata_file)
    return parsed_metadata


def get_automl_config(settings: Dict[str, Any], remove_keys: List[str]) -> AutoMLConfig:
    """
    Get automl config from a settings dict.

    :param settings: A settings dict.
    :return: AutoMLBaseSettings
    """
    automl_settings_dict = copy.deepcopy(settings)
    _remove_keys_from_dict(automl_settings_dict, remove_keys)
    if isinstance(automl_settings_dict.get('featurization'), dict):
        featurization_config = FeaturizationConfig()
        featurization_config._from_dict(automl_settings_dict.get('featurization'))
        automl_settings_dict['featurization'] = featurization_config
    return AutoMLConfig(**automl_settings_dict)


def get_automl_settings(settings: Dict[str, Any], remove_keys: List[str]) -> AutoMLBaseSettings:
    """
    Get automl settings from a settings dict.

    :param settings: A settings dict.
    :param remove_keys: The keys need to be removed from settings.
    :return: AutoMLBaseSettings
    """
    config = get_automl_config(settings, remove_keys)
    settings_dict = {k: v for (k, v) in config.user_settings.items() if k not in config._get_fit_params()}
    return cast(AutoMLBaseSettings, _azureautomlsettings.AzureAutoMLSettings(**settings_dict))


def _remove_keys_from_dict(input_dict: Dict[str, Any], remove_keys: List[str]) -> None:
    for k in remove_keys:
        if k in input_dict:
            del input_dict[k]

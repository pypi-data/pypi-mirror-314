# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, Dict, List, Optional, cast
import json
import os

from azureml.core import Run
from azureml.train.automl.constants import HTSConstants

from .json_serializer import HTSRuntimeEncoder, HTSRuntimeDecoder
from ..data_models.node_columns_info import NodeColumnsInfo


def dump_object_to_json(o: Any, path: str) -> None:
    """
    Dumps object to json with a readable format.

    :param o: Any object.
    :param path: The path to save the json.
    """
    with open(path, "w") as f:
        json.dump(o, f, ensure_ascii=False, indent=4, cls=HTSRuntimeEncoder)


def _parse_columns_info(raw_node_columns_info_data: List[NodeColumnsInfo]) -> Dict[str, NodeColumnsInfo]:
    """
    Convert the json node columns info to node_id-columns info dict.

    :param raw_node_columns_info_data: The raw node column info.
    :return: A dict mapping the columns names to the NodeColumnInfo.
    """
    parsed_vocabulary = {}
    for node_columns_info in raw_node_columns_info_data:
        parsed_vocabulary[node_columns_info.node_id] = node_columns_info
    return parsed_vocabulary


def get_node_columns_info_from_artifacts(run: Run, output_dir: str) -> Dict[str, NodeColumnsInfo]:
    """
    Get the node-columns info from artifacts.

    :param run: The pipeline run.
    :param output_dir: The temp output dir.
    """
    run.download_file(HTSConstants.HTS_FILE_NODE_COLUMNS_INFO_JSON, output_dir)
    info_file = os.path.join(output_dir, HTSConstants.HTS_FILE_NODE_COLUMNS_INFO_JSON)
    with open(info_file) as f:
        node_columns_info = json.load(f, cls=HTSRuntimeDecoder)
    os.remove(info_file)

    return _parse_columns_info(node_columns_info)


def upload_object_to_artifact_json_file(
        input_object: Any, artifact_file_name: str, run: Run, local_mode: bool) -> None:
    """
    Upload object to artifact as a json file.

    :param input_object: An object that can be json serialized.
    :param artifact_file_name: The artifiact file name.
    :param run: The AzureML Run.
    :param local_mode: If the local mode is enabled.
    :return:
    """
    temp_file_path = os.path.join(os.getcwd(), artifact_file_name)
    # Save and upload run info data.
    dump_object_to_json(input_object, temp_file_path)
    run.upload_file(artifact_file_name, temp_file_path)
    if not local_mode:
        # Remove the temp file. If local_mode, the file cannot be removed as the offlineRun object is tracking this.
        os.remove(temp_file_path)


def is_supported_data_file(file_path: str) -> bool:
    """
    Check whether a data file is supported by hts.

    :param file_path: The file path.
    :return: bool
    """
    return file_path.endswith(".parquet") or file_path.endswith(".csv")


def get_intermediate_file_postfix(filename: str) -> Optional[str]:
    """
    Getting the hts related file postfix from a file name.

    :param filename: A file name.
    :return: The postfix that HTS can process.
    """
    postfix = None
    if filename.endswith(HTSConstants.HTS_FILE_POSTFIX_RUN_INFO_JSON):
        postfix = HTSConstants.HTS_FILE_POSTFIX_RUN_INFO_JSON
    elif filename.endswith(HTSConstants.HTS_FILE_POSTFIX_NODE_COLUMNS_INFO_JSON):
        postfix = HTSConstants.HTS_FILE_POSTFIX_NODE_COLUMNS_INFO_JSON
    elif filename.endswith(HTSConstants.HTS_FILE_POSTFIX_METADATA_CSV):
        postfix = HTSConstants.HTS_FILE_POSTFIX_METADATA_CSV
    elif filename.endswith(HTSConstants.HTS_FILE_POSTFIX_EXPLANATION_INFO_JSON):
        postfix = HTSConstants.HTS_FILE_POSTFIX_EXPLANATION_INFO_JSON
    else:
        print("Unknown file to proceed {}".format(filename))
    return cast(Optional[str], postfix)


def get_json_dict_from_file(file_dir: str, filename: str) -> Dict[str, Any]:
    """
    Load a json file to a dict from the file_dir and file name.

    :param file_dir: The file dir.
    :param filename: The file name.
    :return: Dict[str, Any]
    """
    with open(os.path.join(file_dir, filename)) as f:
        result = json.load(f)
    return cast(Dict[str, Any], result)


def get_proportions_csv_filename(filename: str) -> str:
    """
    Get the file name of the intermediate proportions csv file.

    :param filename: The base file name.
    :return: str
    """
    return "{}{}".format(filename, HTSConstants.HTS_FILE_POSTFIX_METADATA_CSV)


def get_node_columns_info_filename(filename: str) -> str:
    """
    Get the file name of the intermediate column vocabulary file.

    :param filename: The base file name.
    :return: str
    """
    return "{}{}".format(filename, HTSConstants.HTS_FILE_POSTFIX_NODE_COLUMNS_INFO_JSON)


def get_explanation_info_file_name(filename: str) -> str:
    """
    Get the name of an intermediate explanation result file.

    :param filename: The base file name.
    :return: The name of a file.
    """
    return "{}{}".format(filename, HTSConstants.HTS_FILE_POSTFIX_EXPLANATION_INFO_JSON)


def get_run_info_filename(filename: str) -> str:
    """
    Get the file name of the intermediate run info file.

    :param filename: The base file name.
    :return: The run_info file name.
    """
    return "{}{}".format(filename, HTSConstants.HTS_FILE_POSTFIX_RUN_INFO_JSON)


def get_engineered_column_info_name(node_id: str) -> str:
    """
    Get the file name for the featurization info.

    :param node_id: The ID of the node for which the featurization info is being generated.
    :return: The file name.
    """
    return "{}{}".format(node_id, HTSConstants.HTS_FILE_POSTFIX_ENG_COL_INFO_JSON)


def get_explanation_artifact_name(raw: bool, node_id: str) -> str:
    """
    Get the name of a JSON serialized dictionary with raw or engineered features explanations.

    :param raw: If true the name of a raw feature artifact will be returned.
    :param node_id: The node id in the graph.
    """
    return '{}_explanation_{}.json'.format(
        HTSConstants.EXPLANATIONS_RAW_FEATURES if raw else
        HTSConstants.EXPLANATIONS_ENGINEERED_FEATURES, node_id)

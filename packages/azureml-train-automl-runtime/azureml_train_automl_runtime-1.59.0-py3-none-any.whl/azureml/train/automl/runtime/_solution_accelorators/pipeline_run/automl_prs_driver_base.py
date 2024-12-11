# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, Dict, Optional, List
from abc import ABC, abstractmethod
import hashlib
import pandas as pd
import os
import sys

from azureml.core import Run
from azureml.automl.core.console_writer import ConsoleWriter


class AutoMLPRSDriverBase(ABC):
    FILE_POSTFIX_RUN_INFO_JSON = "_run_info.json"
    PREFIX_MODEL_NAME = 'automl_'

    """Base class for AutoML PRS run."""
    def __init__(
            self,
            current_step_run: Run,
            **kwargs: Any
    ) -> None:
        """
        Base class for AutoML PRS run.

        :param current_step_run: The current step run.
        """
        self.current_step_run = current_step_run
        self._console_writer = ConsoleWriter(sys.stdout)

    @abstractmethod
    def run(self, input_data_file: str, output_data_file: str) -> Any:
        """Run method."""
        pass

    @staticmethod
    def read_input_data(data_path: str, parse_date: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Read input data from the data path specified.

        :param data_path: The path to the data.
        :param parse_date: Parse date for date columns if read csv file.
        :return: A DataFrame contains the data of the data_path.
        """
        _, file_extension = os.path.splitext(os.path.basename(data_path))
        if file_extension.lower() == ".parquet":
            data = pd.read_parquet(data_path)
        else:
            data = pd.read_csv(data_path, parse_dates=parse_date)
        return data

    @staticmethod
    def get_run_info_filename(filename: str) -> str:
        """
        Get the file name of the intermediate run info file.

        :param filename: The base file name.
        :return: The run_info file name.
        """
        return "{}{}".format(filename, AutoMLPRSDriverBase.FILE_POSTFIX_RUN_INFO_JSON)

    @staticmethod
    def get_hashed_model_string_v2(data_tags: Dict[str, Any], partition_column_names: List[str]) -> str:
        """Get hashed model string."""
        return AutoMLPRSDriverBase._get_hashed_model_string_from_data_identifier(
            AutoMLPRSDriverBase._get_data_identifier(data_tags, partition_column_names))

    @staticmethod
    def _get_hashed_model_string_from_df(df: pd.DataFrame, partition_column_names: List[str]) -> str:
        """Get hashed model string."""
        return AutoMLPRSDriverBase._get_hashed_model_string_from_data_identifier(
            AutoMLPRSDriverBase._get_data_identifier_from_data(df, partition_column_names))

    @staticmethod
    def get_model_name_from_df(
            df: pd.DataFrame, partition_column_names: List[str], run_type_identifier: str) -> str:
        """Get hashed model string."""
        return AutoMLPRSDriverBase.get_model_name(
            AutoMLPRSDriverBase._get_hashed_model_string_from_df(df, partition_column_names), run_type_identifier)

    @staticmethod
    def get_model_name(hashed_model_identifier: str, run_type_identifier: str) -> str:
        """Get model name."""
        return "{}{}_{}".format(AutoMLPRSDriverBase.PREFIX_MODEL_NAME, run_type_identifier, hashed_model_identifier)

    @staticmethod
    def _get_hashed_model_string_from_data_identifier(data_identifier: List[str]) -> str:
        model_string = "_".join(data_identifier)
        print("model string to encode " + model_string)
        sha = hashlib.sha256()
        sha.update(model_string.encode())
        return sha.hexdigest()

    @staticmethod
    def _get_partition_data_tag_dict(df: pd.DataFrame, partition_column_names: List[str]) -> Dict[str, str]:
        """Get the partition data tag dict based on all the contents."""
        # Here we will get all the grain contents to find the model. This is a hacky workaround only for MM
        # to solve some customers required multiple partitions in one file. This also requires both train
        # and test data have same partitions presented in the data. See bug: 2343605.
        data_dict = {}
        if partition_column_names:
            grouped_df = df.groupby(partition_column_names, as_index=False).size()
        else:
            # if no partition column names (For the root level HTS case), then return an empty dict.
            return {}
        for col in partition_column_names:
            data_dict[col] = "+".join(sorted([str(ele) for ele in grouped_df[col]]))
        return data_dict

    @staticmethod
    def _get_data_identifier(data_tags: Dict[str, Any], partition_column_names: List[str]) -> List[str]:
        model_string_items = []
        for k in partition_column_names:
            model_string_items.append(str(k))
            model_string_items.append(str(data_tags[k]))
        return model_string_items

    @staticmethod
    def _get_data_identifier_from_data(df: pd.DataFrame, partition_column_names: List[str]) -> List[str]:
        data_dict = AutoMLPRSDriverBase._get_partition_data_tag_dict(df, partition_column_names)
        return AutoMLPRSDriverBase._get_data_identifier(data_dict, partition_column_names)

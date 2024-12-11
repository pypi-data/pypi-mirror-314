# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import cast, List
import inspect

from azureml.automl.core.shared._diagnostics.contract import Contract


class RawDataInfo:
    def __init__(self, data_type: str, data_size_in_bytes: int, is_partition_needed: bool, number_of_files: int):
        self.data_type = data_type
        self.data_size_in_bytes = data_size_in_bytes
        self.is_partition_needed = is_partition_needed
        self.number_of_files = number_of_files

    @staticmethod
    def get_args_list() -> List[str]:
        """Return the list of arguments for this class."""
        return inspect.getfullargspec(RawDataInfo).args[1:]

    def __eq__(self, other: object) -> bool:
        Contract.assert_type(other, "other", RawDataInfo)
        other = cast(RawDataInfo, other)
        return self.data_type == other.data_type and\
            self.data_size_in_bytes == other.data_size_in_bytes and\
            self.is_partition_needed == other.is_partition_needed and\
            self.number_of_files == other.number_of_files

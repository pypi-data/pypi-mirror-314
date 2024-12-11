# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from datetime import datetime
import random
from typing import List, Sequence, cast, Optional, Mapping, Optional

from dask import dataframe as dd, delayed as ddelayed

from azureml.automl.runtime.featurizer.transformer.timeseries._distributed.distributed_timeseries_util import (
    convert_grain_dict_to_str)
from azureml.data import TabularDataset
from azureml.data.abstract_dataset import _PartitionKeyValueCommonPath
from azureml.data import DataType
from azureml.dataprep import FieldType

field_to_data_types = {
    FieldType.STRING: DataType.to_string(),
    FieldType.BOOLEAN: DataType.to_bool(),
    # ints are converted to floats - because when a partition has all nulls, pandas converts ints to floats
    # causing type mismatches. Converting forcefully to float avoids that issue
    FieldType.INTEGER: DataType.to_float(),
    FieldType.DECIMAL: DataType.to_float(),
    # not specifying date format - we want data runtime to auto discover the right date format
    FieldType.DATE: None,
    FieldType.UNKNOWN: None,
    FieldType.ERROR: None,
    FieldType.NULL: None,
    FieldType.DATAROW: None,
    FieldType.LIST: None,
    FieldType.STREAM: None
}


def _is_dataset_correctly_partitioned(
    dataset: Optional[TabularDataset],
    grain_column_names: Sequence[str],
) -> bool:
    if dataset is None:
        return True
    if dataset.partition_keys is None:
        return False
    return sorted(dataset.partition_keys) == sorted(grain_column_names)


def _get_partition_column_types(
    grain_keyvalues_and_paths: Sequence[_PartitionKeyValueCommonPath]
) -> Optional[Mapping[str, DataType]]:
    if len(grain_keyvalues_and_paths) == 0:
        return None
    partition_column_type = {}
    for col_name, col_value in grain_keyvalues_and_paths[0].key_values.items():
        if isinstance(col_value, int):
            partition_column_type[col_name] = DataType.to_long()
        elif isinstance(col_value, float):
            partition_column_type[col_name] = DataType.to_float()
        elif isinstance(col_value, bool):
            partition_column_type[col_name] = DataType.to_bool()
        elif isinstance(col_value, str):
            partition_column_type[col_name] = DataType.to_string()
        elif isinstance(col_value, datetime):
            partition_column_type[col_name] = DataType.to_datetime()
    return partition_column_type


def _get_sorted_partitions(partitioned_dataset: TabularDataset) -> List[_PartitionKeyValueCommonPath]:
    kvps = partitioned_dataset._get_partition_key_values_with_common_path()
    kvps.sort(key=lambda x: convert_grain_dict_to_str(x.key_values))
    return cast(List[_PartitionKeyValueCommonPath], kvps)


def _get_dataset_for_grain(grain_keyvalues_and_path: _PartitionKeyValueCommonPath,
                           partitioned_dataset: TabularDataset) -> TabularDataset:
    return partitioned_dataset._get_partition_using_partition_key_values_common_path(grain_keyvalues_and_path)


def _to_partitioned_dask_dataframe(partitioned_dataset: TabularDataset,
                                   all_grain_keyvalues_and_path: List[_PartitionKeyValueCommonPath]) \
        -> dd:  # type: ignore
    datasets_for_all_grains = [_get_dataset_for_grain(grain_keyvalues_and_path, partitioned_dataset)
                               for grain_keyvalues_and_path in all_grain_keyvalues_and_path]
    delayed_functions = [ddelayed(dataset_for_grain.to_pandas_dataframe)()
                         for dataset_for_grain in datasets_for_all_grains]
    ddf = dd.from_delayed(delayed_functions, verify_meta=False)
    return ddf


def _to_dask_dataframe_of_random_grains(partitioned_dataset: TabularDataset,
                                        all_grain_keyvalues_and_path: List[_PartitionKeyValueCommonPath],
                                        grain_count: int) -> dd:  # type: ignore
    random_grain_key_values = all_grain_keyvalues_and_path
    if grain_count < len(all_grain_keyvalues_and_path):
        random_grain_key_values = random.sample(all_grain_keyvalues_and_path, grain_count)

    datasets_for_all_grains = [_get_dataset_for_grain(grain_keyvalues_and_path, partitioned_dataset)
                               for grain_keyvalues_and_path in random_grain_key_values]
    delayed_functions = [ddelayed(dataset_for_grain.to_pandas_dataframe)()
                         for dataset_for_grain in datasets_for_all_grains]
    ddf = dd.from_delayed(delayed_functions, verify_meta=False)
    return ddf

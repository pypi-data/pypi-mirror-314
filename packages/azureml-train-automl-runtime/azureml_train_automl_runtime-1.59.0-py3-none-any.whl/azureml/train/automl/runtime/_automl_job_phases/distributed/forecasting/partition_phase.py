# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Optional, Mapping, Sequence, Callable, Any
import logging
import os
import uuid
import tempfile

from azureml.core import Dataset, Datastore
from dask.distributed import WorkerPlugin
import pandas as pd
import re

from azureml._common._error_definition import AzureMLError
from azureml._tracing._tracer_factory import get_tracer
from azureml.automl.core.shared import constants, logging_utilities
from azureml.automl.core.shared.exceptions import DataException
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.shared._diagnostics.automl_error_definitions import MissingColumnsInData
from azureml.training.tabular._diagnostics.error_definitions import (
    TimeseriesDistributedPartitionSpecialCharacters
)
from azureml.automl.core.shared.constants import MLTableDataLabel
from azureml.data import TabularDataset
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings
from azureml.train.automl.runtime._automl_job_phases.utilities import PhaseUtil
from dask.distributed import get_client, get_worker
from azureml.train.automl.runtime._worker_initiator import get_worker_variables
from azureml.automl.runtime.experiment_store import ExperimentStore
from azureml.data import DataType

logger = logging.getLogger(__name__)
tracer = get_tracer(__name__)

PARTITION_PLUGIN = 'partition_plugin'


class PartitionPlugin(WorkerPlugin):
    def __init__(
        self,
        upload_base_path: str,
        grain_column_names: Sequence[str],
        time_column_name: str,
        dataset_type: MLTableDataLabel,
        workspace_getter: Callable[..., Any],
        parent_run_id: str,
    ):
        self.upload_base_path = upload_base_path
        self.grain_column_names = grain_column_names
        self.time_column_name = time_column_name
        self.dataset_type = dataset_type
        self.workspace_getter = workspace_getter
        self.parent_run_id = parent_run_id


class ForecastingPartitionPhase:
    """AutoML job phase that partitions the data."""

    @staticmethod
    def run(
        workspace_getter: Callable[..., Any],
        parent_run_id: str,
        automl_settings: AzureAutoMLSettings,
        dataset: TabularDataset,
        dataset_type: MLTableDataLabel,
    ) -> None:
        """
        Partition the specified dataset into a partitioned TabularDataset.

        :param workspace_getter: A function to get the current workspace.
        :param parent_run_id: The run id of the parent run.
        :param automl_settings: Automl Settings for the experiment.
        :param dataset: The dataset to be partitioned.
        :param dataset_type: The type of the dataset to be partitioned.
        """

        PhaseUtil.log_with_memory(f"Beginning distributed {dataset_type.value} partitioning")
        client = get_client()
        with tracer.start_as_current_span(
            constants.TelemetryConstants.SPAN_FORMATTING.format(
                constants.TelemetryConstants.COMPONENT_NAME, constants.TelemetryConstants.DATA_PREPARATION
            ),
            user_facing_name=constants.TelemetryConstants.DATA_PREPARATION_USER_FACING
        ):
            with logging_utilities.log_activity(logger=logger, activity_name='UploadingPartitionedDataset'):
                workspace = workspace_getter()
                partitioned_data_dir = os.path.join(
                    "data",
                    parent_run_id,
                    "raw_partitioned",
                    str(dataset_type.value),
                    str(uuid.uuid4()),
                )
                partition_plugin = PartitionPlugin(
                    partitioned_data_dir,
                    automl_settings.grain_column_names,
                    automl_settings.time_column_name,
                    dataset_type,
                    workspace_getter,
                    parent_run_id,
                )
                client.register_worker_plugin(partition_plugin, PARTITION_PLUGIN)

                ddf = dataset.to_dask_dataframe()
                dtypes = ddf.dtypes
                logger.info(f"Found {ddf.npartitions} partitions in the dask dataframe")
                if ddf.npartitions > 1000:
                    # If number of partitions are more than 1000, repartition the dask dataframe
                    # to 1000 partitions to avoid creating large number of files per grain.
                    logger.info("Repartitioning the dataframe to 1000 partitions.")
                    ddf = ddf.repartition(npartitions=1000)
                ddf.map_partitions(_partition_and_upload, meta=bool).compute()

                client.unregister_worker_plugin(PARTITION_PLUGIN)

            with logging_utilities.log_activity(logger=logger, activity_name='SavingPartitionedDataset'):
                grain_column_types = _get_partition_column_types(dtypes, automl_settings.grain_column_names)
                expr_store = ExperimentStore.get_instance()
                expr_store.data.partitioned.save_raw_partitioned_dataset(
                    workspace=workspace,
                    path_to_dataset=partitioned_data_dir,
                    dataset_type=dataset_type,
                    partition_keys=automl_settings.grain_column_names,
                    set_column_types=grain_column_types
                )
        PhaseUtil.log_with_memory(f"Ending distributed {dataset_type.value} partitioning")


def _get_partition_column_types(
    dtypes: pd.Series,
    grain_column_names: Sequence[str],
) -> Optional[Mapping[str, DataType]]:
    """
    Get the column types for dataprep from datatypes from the dataframe.

    :param dtypes: The datatypes of the columns in the dataframe.
    :param grain_column_names: The grain column names.

    :return: Dictionary mapping grain column names to DataType from dataprep.
    """
    if len(grain_column_names) == 0:
        return None
    partition_column_type = {}
    for grain_column_name in grain_column_names:
        grain_dtype = dtypes[grain_column_name]
        if pd.api.types.is_integer_dtype(grain_dtype):
            partition_column_type[grain_column_name] = DataType.to_long()
        elif pd.api.types.is_float_dtype(grain_dtype):
            partition_column_type[grain_column_name] = DataType.to_float()
        elif pd.api.types.is_bool_dtype(grain_dtype):
            partition_column_type[grain_column_name] = DataType.to_bool()
        elif pd.api.types.is_string_dtype(grain_dtype):
            partition_column_type[grain_column_name] = DataType.to_string()
        elif pd.api.types.is_datetime64_any_dtype(grain_dtype):
            partition_column_type[grain_column_name] = DataType.to_datetime()
    return partition_column_type


def process_and_save_df(
    df: pd.DataFrame,
    grain_column_names: Sequence[str],
    time_column_name: str,
    remote_base_path: str,
    datastore: Datastore,
) -> None:
    """
    Process and save a partition of the dataframe.

    :param df: The partitioned dataframe containing only one grain.
    :param grain_column_names: The grain column names.
    :param time_column_name: The time column name.
    :param remote_base_path: The base path where the partitioned dataframe has to be uploaded.
    :param datastore: The datastore where the data has to be uploaded.
    """
    if df.empty:
        return
    if not pd.api.types.is_datetime64_any_dtype(df[time_column_name]):
        df[time_column_name] = pd.to_datetime(df[time_column_name])
    grain_col_values = df[grain_column_names].iloc[0].to_dict().values()
    _validate_grain_column_values(grain_col_values)
    df.reset_index(drop=True, inplace=True)
    df.drop(columns=grain_column_names, inplace=True, errors="ignore")
    with tempfile.TemporaryDirectory() as tmp_dir:
        df.to_parquet(os.path.join(tmp_dir, f"{uuid.uuid4()}.parquet"))
        target = (datastore, os.path.join(remote_base_path, *[str(val) for val in grain_col_values]))
        Dataset.File.upload_directory(tmp_dir, target, show_progress=False)


def _partition_and_upload(df: pd.DataFrame) -> bool:
    """
    Partition a dataframe and upload it to remote.

    :param df: The dataframe to be partitioned and uploaded.

    :return: Always return True because dask expects a return value.
    """
    worker = get_worker()
    partition_plugin = worker.plugins[PARTITION_PLUGIN]
    default_datastore_for_worker, _, _ = get_worker_variables(
        partition_plugin.workspace_getter, partition_plugin.parent_run_id)
    grain_column_names = partition_plugin.grain_column_names
    time_column_name = partition_plugin.time_column_name
    dataset_type = partition_plugin.dataset_type

    if time_column_name not in df.columns:
        raise DataException._with_error(
            AzureMLError.create(
                MissingColumnsInData,
                target="time_column_name",
                columns=time_column_name,
                data_object_name=dataset_type.value,
                reference_code=ReferenceCodes._TS_DIST_TIME_COLUMN_NOT_IN_UNPARTITIONED_DATASET,
            )
        )
    for grain_column in grain_column_names:
        if grain_column not in df.columns:
            raise DataException._with_error(
                AzureMLError.create(
                    MissingColumnsInData,
                    target="timeseries_identifier_column_name",
                    columns=grain_column,
                    data_object_name=dataset_type.value,
                    reference_code=ReferenceCodes._TS_DIST_GRAIN_COLUMN_NOT_IN_UNPARTITIONED_DATASET,
                )
            )

    for _, grain_df in df.groupby(grain_column_names):
        process_and_save_df(
            grain_df,
            grain_column_names,
            time_column_name,
            partition_plugin.upload_base_path,
            default_datastore_for_worker
        )
    return True


def _validate_grain_column_values(grain_col_values: Sequence[Any]) -> None:
    """
    Check if grain column values contain any special character that conflicts
    with file system path.

    :param grain_col_values: The grain column values
    """
    # Forward/backward slashes are not allowed since they create another level of directory.
    # . or .. is not allowed since they have special meaning in file system path.
    regex_string = r"(^\.+$)|[\\/]"
    if any(re.search(regex_string, str(grain_col_value)) for grain_col_value in grain_col_values):
        raise DataException._with_error(
            AzureMLError.create(
                TimeseriesDistributedPartitionSpecialCharacters,
                target="dataset_partition",
                reference_code=ReferenceCodes._TS_DIST_GRAIN_COLUMN_SPECIAL_PATH_CHARACTERS,
            )
        )

# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
import logging
import os
import uuid
from typing import Any, Callable, cast, Dict, List, Optional, Set, Tuple, Sequence

import azureml.dataprep as dprep
import dask
import gc
import numpy as np
import pandas as pd
import sklearn
from sklearn.pipeline import Pipeline
from azureml._tracing._tracer_factory import get_tracer
from azureml.automl.core.featurization import FeaturizationConfig
from azureml.automl.core.shared import constants, logging_utilities
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared.constants import TimeSeries, TimeSeriesInternal, MLTableDataLabel
from azureml.automl.core.shared.types import GrainType
from azureml.core import Run
from azureml.data import TabularDataset
from azureml.data.abstract_dataset import _PartitionKeyValueCommonPath
from azureml.train.automl import _constants_azureml
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings
from azureml.train.automl.runtime._automl_job_phases.utilities import PhaseUtil
from azureml.train.automl.runtime._automl_job_phases.distributed.experiment_state_plugin import ExperimentStatePlugin
from azureml.train.automl.runtime._worker_initiator import EXPERIMENT_STATE_PLUGIN
from azureml.train.automl.runtime._worker_initiator import get_worker_variables
from azureml.train.automl.runtime._partitioned_dataset_utils import _get_dataset_for_grain, \
    _to_partitioned_dask_dataframe, _to_dask_dataframe_of_random_grains, _get_partition_column_types
from dask.distributed import WorkerPlugin
from dask.distributed import get_client, get_worker
from joblib import Parallel, delayed, parallel_backend

from azureml.automl.runtime import _ml_engine as ml_engine, data_context
from azureml.automl.runtime._forecasting_log_transform_utilities import \
    _log_transform_column_single_series_tests, _should_apply_log_transform, LogTransformTestResults
from azureml.automl.runtime.experiment_store import ExperimentStore
from azureml.automl.runtime.featurizer.transformer import TimeSeriesPipelineType, TimeSeriesTransformer
from azureml.automl.runtime.featurizer.transformer.timeseries._distributed import \
    AutoMLAggregateTransformer, distributed_timeseries_util, AggregatedTransformerFactory
from azureml.automl.runtime.featurizer.transformer.timeseries. \
    all_rows_dropper import AllRowsDropper
import copy
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.runtime.featurizer.transformer.timeseries._distributed.distributed_timeseries_util import (
    convert_grain_dict_to_str)
from azureml.automl.runtime.featurizer.transformer.timeseries. \
    forecasting_base_estimator import _GrainBasedStatefulTransformer
from azureml.automl.runtime.featurizer.transformer.timeseries.time_index_featurizer import TimeIndexFeaturizer
from azureml.automl.runtime.featurizer.transformer.timeseries.time_series_imputer import TimeSeriesImputer
from azureml.automl.runtime._time_series_data_set import TimeSeriesDataSet
from azureml.automl.runtime.featurizer.transformer.timeseries.unique_target_grain_dropper import (
    UniqueTargetGrainDropper
)
from azureml.training.tabular.featurization.timeseries._distributed.timeseries_data_profile import \
    TimeSeriesDataProfile, AggregatedTimeSeriesDataProfile, ts_dataprofile_from_dprep_dataprofile
from azureml.dataprep import DataProfile

logger = logging.getLogger(__name__)
tracer = get_tracer(__name__)

TRANSFORM_GRAIN_PLUGIN = 'transform_grain_plugin'


class TransformGrainPlugin(WorkerPlugin):
    def __init__(self,
                 featurized_data_dir: str,
                 training_dataset: TabularDataset,
                 validation_dataset: TabularDataset,
                 ts_transformer: TimeSeriesTransformer) -> None:
        self.featurized_data_dir = featurized_data_dir
        self.training_dataset = TabularDataset._create(training_dataset._dataflow,
                                                       training_dataset._properties,
                                                       telemetry_info=training_dataset._telemetry_info)
        self.validation_dataset = TabularDataset._create(validation_dataset._dataflow,
                                                         validation_dataset._properties,
                                                         telemetry_info=validation_dataset._telemetry_info)
        self.ts_transformer = ts_transformer


class _GrainTransformResult(object):
    """The data class to store the stateful transform, last known date and y imputer."""

    def __init__(self,
                 stateful_transformers: Tuple[str, Dict[Any, _GrainBasedStatefulTransformer]],
                 latest_date: Dict[GrainType, pd.Timestamp],
                 y_imputer: Dict[GrainType, TimeSeriesImputer],
                 log_transform_results: Optional[LogTransformTestResults] = None,
                 indicator_column_data: Optional[Dict[str, bool]] = None,
                 timeseries_data_profile: Optional[TimeSeriesDataProfile] = None,
                 y_min_dict: Optional[Dict[GrainType, float]] = None,
                 y_max_dict: Optional[Dict[GrainType, float]] = None
                 ) -> None:
        """
        Constructor.

        :param stateful_transformers: The dictionary with one grain name as a key converted
                                      to string and one transform.
        :param latest_date: The dictionary with raw grain as a key name and timestamp
                            for the latest known date.
        :param y_imputer: The dictionary with raw grain as a key and corresponding y
                          imputer.
        :param log_transform_results: The data needed for log transform decision logic.
        :param indicator_column_data: The dictionary, relating column and boolean value,
                                     saying if this is an indicator column.
        :param timeseries_data_profile: The timeseries data profile for the grain.
        :param y_min_dict: The dictionary with a minimal target value for a given grain.
        :param y_max_dict: The dictionary with a maximal target value for a given grain.
        """
        # TODO: when  the support of python<3.7 will be officially removed,
        # convert this class to dataclass.
        self.stateful_transformers = stateful_transformers
        self.latest_date = latest_date
        self.y_imputer = y_imputer
        self.log_transform_results = log_transform_results
        self.indicator_column_data = indicator_column_data
        self.timeseries_data_profile = timeseries_data_profile
        self.y_min_dict = y_min_dict if y_min_dict else {}
        self.y_max_dict = y_max_dict if y_max_dict else {}


TransformOneGrainResults = Tuple[_GrainTransformResult, Optional[LogTransformTestResults]]


class ForecastingDistributedFeaturizationPhase:
    """AutoML job phase that featurizes the data."""

    @staticmethod
    def run(workspace_getter: Callable[..., Any],
            current_run: Run,
            parent_run_id: str,
            automl_settings: AzureAutoMLSettings,
            training_dataset: TabularDataset,
            validation_dataset: TabularDataset,
            original_grain_key_values: List[Dict[str, Any]],
            prepared_grain_keyvalues_and_path: List[_PartitionKeyValueCommonPath],
            prepared_grain_keyvalues_and_path_for_validation: List[_PartitionKeyValueCommonPath]) -> None:

        PhaseUtil.log_with_memory("Beginning distributed featurization")
        client = get_client()

        with tracer.start_as_current_span(
            constants.TelemetryConstants.SPAN_FORMATTING.format(
                constants.TelemetryConstants.COMPONENT_NAME, constants.TelemetryConstants.FEATURIZATION
            ),
            user_facing_name=constants.TelemetryConstants.FEATURIZATION_USER_FACING
        ):
            with logging_utilities.log_activity(logger=logger, activity_name='FindingUniqueCategories'):
                categories_by_grain_cols, categories_by_non_grain_cols = _get_categories_by_columns(
                    training_dataset,
                    original_grain_key_values,
                    prepared_grain_keyvalues_and_path,
                    automl_settings.grain_column_names)

            gc.collect()
            PhaseUtil.log_with_memory("Finished FindingUniqueCategories")

            with logging_utilities.log_activity(logger=logger, activity_name='BuildPipeline'):
                ts_transformer = _build_pipeline_for_fitting(
                    training_dataset,
                    prepared_grain_keyvalues_and_path,
                    automl_settings,
                    categories_by_grain_cols,
                    categories_by_non_grain_cols
                )

            featurized_data_dir = '{}_{}_featurized_{}'.format(current_run.experiment.name,
                                                               parent_run_id,
                                                               str(uuid.uuid4()))

            expr_store = ExperimentStore.get_instance()
            long_grain_key_values_and_path = \
                [dt for dt in prepared_grain_keyvalues_and_path
                 if convert_grain_dict_to_str(dt.key_values)
                 not in expr_store.metadata.timeseries.short_grain_names]
            long_grain_key_values_and_path_for_validation = \
                [dt for dt in prepared_grain_keyvalues_and_path_for_validation
                 if convert_grain_dict_to_str(dt.key_values)
                 not in expr_store.metadata.timeseries.short_grain_names]

            transform_grain_plugin = TransformGrainPlugin(featurized_data_dir,
                                                          training_dataset,
                                                          validation_dataset,
                                                          ts_transformer)
            client.register_worker_plugin(transform_grain_plugin, TRANSFORM_GRAIN_PLUGIN)

            with logging_utilities.log_activity(logger=logger, activity_name='DistributedTransformation'):
                with parallel_backend('dask'):
                    # This will return a list of dictionaries mapping grain_col_values to dictionaries
                    # of transformer names to transformers for all stateful transformers
                    # [{grain_id: {tr_name: tr_obj}}]
                    transform_results_list = Parallel(n_jobs=-1)(delayed(_transform_one_grain)(
                        kvp, kvp_v
                    ) for kvp, kvp_v in zip(long_grain_key_values_and_path,
                                            long_grain_key_values_and_path_for_validation))

                # We assume that at this point we have at least one long grain as otherwise
                # we are raising user error during distributed_preparation_phase.
                Contract.assert_non_empty(transform_results_list, 'TimeSeriesTransformer',
                                          reference_code=ReferenceCodes._TS_SHORT_GRAINS_ALL_SHORT_FIT_DIST_FEATUR)
                # get the log transform results
                log_transform_tests_tuple = [r.log_transform_results for r in transform_results_list]
                # Get the data onj indicator columns.
                indicator_columns_data_list = [
                    r.indicator_column_data for r in transform_results_list if r.indicator_column_data is not None]
            gc.collect()
            PhaseUtil.log_with_memory("Finished DistributedTransformation")

            with logging_utilities.log_activity(logger=logger, activity_name='BuildDistributedTransformer'):
                aggregate_timeseries_transformer = _build_transformer_for_all_grains(
                    training_dataset,
                    automl_settings.label_column_name,
                    long_grain_key_values_and_path,
                    ts_transformer,
                    transform_results_list
                )

            gc.collect()
            PhaseUtil.log_with_memory("Finished BuildDistributedTransformer")

            expr_store.transformers.set_transformers(
                {constants.Transformers.TIMESERIES_TRANSFORMER: aggregate_timeseries_transformer}
            )

            grain_column_types = _get_partition_column_types(prepared_grain_keyvalues_and_path)

            with logging_utilities.log_activity(logger=logger, activity_name='SavingFeaturizedTrainDataset'):
                expr_store.data.partitioned.save_featurized_train_dataset(
                    workspace_getter(),
                    f"{featurized_data_dir}/{MLTableDataLabel.TrainData.value}",
                    training_dataset.partition_keys,
                    grain_column_types
                )

            with logging_utilities.log_activity(logger=logger, activity_name='SavingPreparedValidationDataset'):
                expr_store.data.partitioned.save_featurized_valid_dataset(
                    workspace_getter(),
                    f"{featurized_data_dir}/{MLTableDataLabel.ValidData.value}",
                    training_dataset.partition_keys,
                    grain_column_types
                )

            time_series_info = expr_store.metadata.timeseries.series_stats.__dict__
            metadata_info = expr_store.metadata.problem_info.__dict__
            problem_info = PhaseUtil.combine_dict(a=time_series_info, b=metadata_info, override=True)

            # Add placeholder problem info. This is required today by Jasmine.
            current_run.add_properties({
                _constants_azureml.Properties.PROBLEM_INFO: json.dumps(problem_info)
            })

            with logging_utilities.log_activity(logger=logger, activity_name='SavingGlobalStatistics'):
                set_global_statistics(expr_store, [r for r in log_transform_tests_tuple if r is not None])
                expr_store.metadata.timeseries.set_indicator_columns_data(
                    distributed_timeseries_util.collate_indicator_column_data_dictionaries(
                        indicator_columns_data_list))

            with logging_utilities.log_activity(logger=logger, activity_name='BuildAggregatedTimeSeriesDataProfile'):
                column_order_in_profile = sorted(
                    list(indicator_columns_data_list[0].keys()) + [TimeSeriesInternal.DUMMY_TARGET_COLUMN]
                )
                profile_mapping = {
                    r.stateful_transformers[0]: r.timeseries_data_profile for r in transform_results_list
                }
                timeseries_data_profile = AggregatedTimeSeriesDataProfile(
                    column_order_in_timeseries_profile=column_order_in_profile,
                    columns=_get_columns_from_one_grain(expr_store, workspace_getter),
                    profile_mapping=profile_mapping
                )
                expr_store.metadata.timeseries.set_featurized_data_profile(timeseries_data_profile)

            expr_store.unload()

        PhaseUtil.log_with_memory("Ending distributed featurization")


def _get_columns_from_one_grain(
    expr_store: ExperimentStore,
    workspace_getter: Callable[..., Any]
) -> Sequence[str]:
    """
    Get the columns in the featurized dataset from one grain.

    :param expr_store: The experiment store containing the featurized TabularDataset.
    :param workspace_getter: The function to get the workspace.

    :return: The list of columns in the featurized dataset. The order of columns is maintained.
    """
    featurized_dataset = expr_store.data.partitioned.get_featurized_train_dataset(workspace_getter())
    grain = featurized_dataset._get_partition_key_values_with_common_path()[0]
    df = featurized_dataset._get_partition_using_partition_key_values_common_path(grain)\
        .take(1)\
        .to_pandas_dataframe()
    return list(df.columns)


def _clone_stateful_transformer(transform_grain_plugin: TransformGrainPlugin) -> None:
    """Clone the stateful transformer."""
    # Remove the dict latest date and _y_imputers because they keep on accumulating on each worker
    # thread which causes unnecessary duplication of data that is sent back to the scheduler.
    transform_grain_plugin.ts_transformer.dict_latest_date = {}
    transform_grain_plugin.ts_transformer._y_imputers = {}
    transform_grain_plugin.ts_transformer.pipeline = cast(Pipeline, transform_grain_plugin.ts_transformer.pipeline)
    for idx, step in enumerate(transform_grain_plugin.ts_transformer.pipeline.steps):
        if not isinstance(step[1], _GrainBasedStatefulTransformer):
            continue
        cloned_transformer = sklearn.base.clone(step[1])
        # set drop single grain to True for UniqueTargetGrainDropper as we are handling grain by grain in distributed
        # featurization
        if isinstance(cloned_transformer, UniqueTargetGrainDropper):
            cloned_transformer.drop_single_grain = True
        transform_grain_plugin.ts_transformer.pipeline.steps[idx] = (step[0], cloned_transformer)


def _fit_unique_target_grain_dropper(
        transform_grain_plugin: TransformGrainPlugin, train_X_grain: pd.DataFrame,
        train_y_grain: np.ndarray, validation_X: pd.DataFrame, validation_y: np.ndarray
) -> None:
    unique_target_grain_dropper = transform_grain_plugin.ts_transformer.unique_target_grain_dropper
    # fit unique target grain dropper first. If the data has unique target, then we won't do any other fit as all
    # rows will be dropped.
    if unique_target_grain_dropper is not None:
        tsds = TimeSeriesDataSet.create_tsds_safe(
            train_X_grain,
            y=train_y_grain,
            time_column_name=transform_grain_plugin.ts_transformer.time_column_name,
            origin_column_name=transform_grain_plugin.ts_transformer.origin_column_name,
            boolean_column_names=transform_grain_plugin.ts_transformer.boolean_columns,
            target_column_name=transform_grain_plugin.ts_transformer.target_column_name,
            grain_column_names=transform_grain_plugin.ts_transformer.grain_column_names,
        )
        tsds_val = TimeSeriesDataSet.create_tsds_safe(
            validation_X,
            y=validation_y,
            time_column_name=transform_grain_plugin.ts_transformer.time_column_name,
            origin_column_name=transform_grain_plugin.ts_transformer.origin_column_name,
            boolean_column_names=transform_grain_plugin.ts_transformer.boolean_columns,
            target_column_name=transform_grain_plugin.ts_transformer.target_column_name,
            grain_column_names=transform_grain_plugin.ts_transformer.grain_column_names,
        )
        unique_target_grain_dropper.fit(tsds)
        unique_target_grain_dropper.set_last_validation_data(tsds_val)


def _fit_transform_data(
        transform_grain_plugin: TransformGrainPlugin,
        experiment_state_plugin: ExperimentStatePlugin,
        train_X_grain: pd.DataFrame,
        train_y_grain: np.ndarray,
        validation_X_grain: pd.DataFrame,
        validation_y_grain: np.ndarray,
        grain_keyvalues_and_path: _PartitionKeyValueCommonPath,
        expr_store_for_worker: ExperimentStore
) -> Tuple[pd.DataFrame, Dict[MLTableDataLabel, str]]:
    # transform one grain
    train_transformed_data = transform_grain_plugin.ts_transformer.fit_transform(train_X_grain, train_y_grain)
    # We have to copy the latest date dictionary, because we are fitting the transform
    # multiple times. Tough distributed is using pickle mechanism for multi threading,
    # deepcopy saves us from potential mechanism change in future versions of python or
    # distributed.
    validation_transformed_data = transform_grain_plugin.ts_transformer.transform(
        validation_X_grain,
        validation_y_grain)
    target_column_name = transform_grain_plugin.ts_transformer.target_column_name
    # Target column must be in the featurized data
    Contract.assert_true(target_column_name in train_transformed_data.columns,
                         'Target column not in featurized training data.', log_safe=True)
    Contract.assert_true(target_column_name in validation_transformed_data.columns,
                         'Target column not in featurized validation data.', log_safe=True)
    featurized_file_path_dict: Dict[MLTableDataLabel, str] = {}
    for transformed_data, split in \
            zip(
                [validation_transformed_data, train_transformed_data],
                [MLTableDataLabel.ValidData, MLTableDataLabel.TrainData]
            ):
        # write one grain to local file
        # drop the grain columns since they will be part of the path and hence
        # they will be reconstructed as part of reading partitioned dataset
        transformed_data.reset_index(inplace=True)
        transformed_data.drop(columns=experiment_state_plugin.automl_settings.grain_column_names, inplace=True)
        transformed_data[TimeSeriesInternal.DUMMY_LOG_TARGET_COLUMN] = np.log1p(
            transformed_data[TimeSeriesInternal.DUMMY_TARGET_COLUMN]
        )
        featurized_file_name = '{}-{}.parquet'.format(split.value, str(uuid.uuid4()))
        featurized_file_path = '{}/{}'.format(transform_grain_plugin.featurized_data_dir, featurized_file_name)
        transformed_data.to_parquet(featurized_file_path)

        # construct the path to which data will be written to on the default blob store
        target_path_array = [transform_grain_plugin.featurized_data_dir, split.value]
        for val in grain_keyvalues_and_path.key_values.values():
            target_path_array.append(str(val))
        target_path = '/'.join(target_path_array)

        # upload data to default store
        expr_store_for_worker.data.partitioned.write_file(featurized_file_path, target_path)
        featurized_file_path_dict[split] = featurized_file_path
        logger.info("transformed one grain and uploaded data")

    return train_transformed_data, featurized_file_path_dict


def _build_grain_transform_result(
        transform_grain_plugin: TransformGrainPlugin,
        grain_keyvalues_and_path: _PartitionKeyValueCommonPath,
        is_unique_target_grain: bool,
        featurized_file_path_dict: Dict[MLTableDataLabel, str],
        train_transformed_data: pd.DataFrame
) -> _GrainTransformResult:
    # Retrieve stateful transformers to return to the primary node for aggregation
    stateful_transformers = {}
    transform_grain_plugin.ts_transformer.pipeline = cast(Pipeline, transform_grain_plugin.ts_transformer.pipeline)
    for step in transform_grain_plugin.ts_transformer.pipeline.steps:
        if not isinstance(step[1], _GrainBasedStatefulTransformer):
            continue
        else:
            stateful_transformers[step[0]] = step[1]

    dict_latest_date = copy.deepcopy(transform_grain_plugin.ts_transformer.dict_latest_date)
    y_min_dict = copy.deepcopy(transform_grain_plugin.ts_transformer.y_min_dict)
    y_max_dict = copy.deepcopy(transform_grain_plugin.ts_transformer.y_max_dict)
    y_imputer = copy.deepcopy(transform_grain_plugin.ts_transformer._y_imputers)

    # In case of unique transformer, the grain will be dropped and no log transform needed, return the results now.
    log_transform_results = None
    indicator_column_data = None
    timeseries_data_profile = None
    if not is_unique_target_grain:
        train_data_profile, val_data_profile = _get_dprep_data_profile_for_grain(featurized_file_path_dict)
        log_transform_results = get_log_transform_results(
            train_data_profile,
            train_transformed_data,
            transform_grain_plugin.ts_transformer.target_column_name,
        )
        indicator_column_data = get_indicator_columns_data_for_grain(
            train_data_profile,
            transform_grain_plugin.ts_transformer.target_column_name,
        )
        timeseries_data_profile = ts_dataprofile_from_dprep_dataprofile(
            train_data_profile,
            val_data_profile,
            transform_grain_plugin.ts_transformer.time_column_name
        )

    return _GrainTransformResult(
        stateful_transformers=(distributed_timeseries_util.convert_grain_dict_to_str(
            grain_keyvalues_and_path.key_values), stateful_transformers),
        latest_date=dict_latest_date,
        y_imputer=y_imputer,
        log_transform_results=log_transform_results,
        indicator_column_data=indicator_column_data,
        timeseries_data_profile=timeseries_data_profile,
        y_min_dict=y_min_dict,
        y_max_dict=y_max_dict
    )


def _transform_one_grain(grain_keyvalues_and_path: _PartitionKeyValueCommonPath,
                         grain_keyvalues_and_path_for_validation: _PartitionKeyValueCommonPath) \
        -> _GrainTransformResult:
    worker = get_worker()
    experiment_state_plugin = worker.plugins[EXPERIMENT_STATE_PLUGIN]
    transform_grain_plugin = worker.plugins[TRANSFORM_GRAIN_PLUGIN]

    transform_grain_plugin.ts_transformer.unique_target_grain_dropper.drop_single_grain = True

    default_datastore_for_worker, workspace_for_worker, expr_store_for_worker = get_worker_variables(
        experiment_state_plugin.workspace_getter, experiment_state_plugin.parent_run_id)

    training_dataset_for_grain = _get_dataset_for_grain(grain_keyvalues_and_path,
                                                        transform_grain_plugin.training_dataset)
    valid_dataset_for_grain = _get_dataset_for_grain(grain_keyvalues_and_path_for_validation,
                                                     transform_grain_plugin.validation_dataset)

    os.makedirs(transform_grain_plugin.featurized_data_dir, exist_ok=True)
    # load pandas dataframe for one grain
    train_X_grain = training_dataset_for_grain.to_pandas_dataframe()

    train_y_grain = train_X_grain.pop(experiment_state_plugin.automl_settings.label_column_name).values
    validation_X_grain = valid_dataset_for_grain.to_pandas_dataframe()
    validation_y_grain = validation_X_grain.pop(
        experiment_state_plugin.automl_settings.label_column_name).values

    # transform_grain_plugin contains ts_transformer object, which is shared for the same worker
    # as worker is being reused. Here we have to make sure that we have cloned all the stateful
    # transforms.
    _clone_stateful_transformer(transform_grain_plugin)
    _fit_unique_target_grain_dropper(
        transform_grain_plugin, train_X_grain, train_y_grain,
        validation_X_grain, validation_y_grain
    )
    is_unique_target = transform_grain_plugin.ts_transformer.unique_target_grain_dropper.has_unique_target_grains
    if not is_unique_target:
        train_transformed_data, featurized_file_path_dict = _fit_transform_data(
            transform_grain_plugin, experiment_state_plugin, train_X_grain, train_y_grain,
            validation_X_grain, validation_y_grain, grain_keyvalues_and_path, expr_store_for_worker
        )
    else:
        # For the unique target scenario, set those values to empty.
        train_transformed_data = pd.DataFrame()
        featurized_file_path_dict = {}

    return _build_grain_transform_result(
        transform_grain_plugin, grain_keyvalues_and_path, is_unique_target, featurized_file_path_dict,
        train_transformed_data
    )


def _get_dprep_data_profile_for_grain(
    featurized_file_path_dict: Dict[MLTableDataLabel, str]
) -> Tuple[DataProfile, DataProfile]:
    """
    Get train and val dataprep data profile for a grain.

    :param featurized_file_path_dict: A mapping of dataset type and path for its featurized data.

    :return: The dataprep data profile for train and val grains.
    """
    train_profile = dprep.read_parquet_file(featurized_file_path_dict[MLTableDataLabel.TrainData]).get_profile()
    val_profile = dprep.read_parquet_file(featurized_file_path_dict[MLTableDataLabel.ValidData]).get_profile()
    return train_profile, val_profile


def get_log_transform_results(
        train_data_profile: DataProfile,
        train_transformed_data: pd.DataFrame,
        target_column_name: str,
) -> LogTransformTestResults:
    # Do log transform tests for the target column on the training data
    # Pass the ColumnProfile for the featurized data to speed-up computations
    Contract.assert_true(target_column_name in train_data_profile.columns, 'Target column not in data profile.',
                         log_safe=True)
    target_ar = train_transformed_data[target_column_name].values
    col_profile = train_data_profile.columns[target_column_name]
    log_transform_test_results = _log_transform_column_single_series_tests(target_ar, profile=col_profile)
    return log_transform_test_results


def get_indicator_columns_data_for_grain(
        train_data_profile: DataProfile,
        target_column_name: str,
) -> Dict[str, bool]:
    """
    From the column profile detect the indicator columns.

    :param train_data_profile: DataProfile for the training grain.
    :param target_column_name: The target column.
    :return: The dictionary, relating column and boolean value, saying if this is an indicator column.
    """
    indicator_column_data = {}
    for col in train_data_profile.columns.keys():
        if col == target_column_name:
            continue
        value_counts = train_data_profile.columns[col].value_counts
        if value_counts is None or len(value_counts) > 2:
            indicator_column_data[col] = False
        else:
            indicator_column_data[col] = all(
                [val.value == 1 or val.value == 0 for val in train_data_profile.columns[col].value_counts])
    return indicator_column_data


def unique_by_partition_columns(all_grain_key_values: List[Dict[str, Any]],
                                grain_col: str) -> List[Any]:
    categories_for_grain_col = set()
    for key_val in all_grain_key_values:
        categories_for_grain_col.add(key_val[grain_col])
    unique_vals = list(categories_for_grain_col)
    logger.info("Calculated uniques for one grain column")
    return unique_vals


def _get_categories_by_columns(partitioned_dataset: TabularDataset,
                               original_grain_key_values: List[Dict[str, Any]],
                               prepared_grain_keyvalues_and_path: List[_PartitionKeyValueCommonPath],
                               grain_column_names: List[str]) -> Tuple[Dict[str, List[Any]], Dict[str, List[Any]]]:

    categories_by_grain_cols = {col: pd.Categorical(unique_by_partition_columns(original_grain_key_values,
                                                                                col)).categories
                                for col in grain_column_names}
    PhaseUtil.log_with_memory("Calculated uniques for all grain columns")

    # randomly chose about 5 grains to find types for columns
    ddf_sampled = _to_dask_dataframe_of_random_grains(partitioned_dataset, prepared_grain_keyvalues_and_path, 5)
    categorical_cols_with_grains_cols = ddf_sampled.select_dtypes(['object', 'category', 'bool']).columns
    categorical_cols = [col for col in categorical_cols_with_grains_cols if col not in grain_column_names]
    logger.info("found {} categorical columns excluding grain columns".format(len(categorical_cols)))

    categories_by_non_grain_cols = {}
    if len(categorical_cols) > 0:
        ddf = _to_partitioned_dask_dataframe(partitioned_dataset, prepared_grain_keyvalues_and_path)
        uniques_delayed = [ddf[col].unique() for col in categorical_cols]
        uniques = dask.compute(*uniques_delayed)
        categories_by_non_grain_cols = {col: pd.Categorical(uniques).categories for col, uniques
                                        in zip(categorical_cols, uniques)}
        PhaseUtil.log_with_memory("Calculated uniques for all non grain columns")

    return categories_by_grain_cols, categories_by_non_grain_cols


def _build_pipeline_for_fitting(
    training_dataset: TabularDataset,
    all_grain_keyvalues_and_path: List[_PartitionKeyValueCommonPath],
    automl_settings: AzureAutoMLSettings,
    categories_by_grain_cols: Dict[str, List[Any]],
    categories_by_non_grain_cols: Dict[str, List[Any]]
) -> TimeSeriesTransformer:

    expr_store = ExperimentStore.get_instance()

    # We currently subsample 100 grains to handle cases of large number of time series
    # To handle case of large history in addition to large number of time series we need following 2 solutions
    # 1) limit history per time series  2) Keep a tab on memory and limit total rows to fixed count at all costs
    subsampled_grains_ddf = _to_dask_dataframe_of_random_grains(training_dataset, all_grain_keyvalues_and_path, 100)
    subsampled_X = subsampled_grains_ddf.compute()
    subsampled_Y = subsampled_X.pop(automl_settings.label_column_name).values

    # Disable lags and rolling windows for FTCN
    automl_settings.window_size = None
    automl_settings.lags = None

    data_context_params = data_context.DataContextParams(automl_settings)

    pipeline_type = TimeSeriesPipelineType.FULL
    ts_params = cast(Dict[str, Any], data_context_params.control_params.timeseries_param_dict)
    featurization_config = data_context_params.control_params.featurization
    # Timeseries currently doesn't reject "off" as input and currently converts "auto"/"off" to the object
    # during the featurize_data_timeseries method. Since we bypass that call and call suggest directly, we
    # need to convert from string to object here.
    if isinstance(featurization_config, str):
        featurization_config = FeaturizationConfig()
    if featurization_config is not None and \
        isinstance(featurization_config, FeaturizationConfig) and \
            automl_settings.label_column_name is not None:
        featurization_config._convert_timeseries_target_column_name(automl_settings.label_column_name)

    tsds = TimeSeriesDataSet.create_tsds_safe(
        X=subsampled_X,
        y=subsampled_Y,
        target_column_name=data_context_params.data_params.label_column_name,
        time_column_name=ts_params[TimeSeries.TIME_COLUMN_NAME],
        origin_column_name=ts_params.get(
            TimeSeriesInternal.ORIGIN_TIME_COLUMN_NAME, TimeSeriesInternal.ORIGIN_TIME_COLNAME_DEFAULT),
        grain_column_names=ts_params.get(
            TimeSeries.GRAIN_COLUMN_NAMES, [TimeSeriesInternal.DUMMY_GRAIN_COLUMN]))

    # Force all TimeIndexFeaturizers to have the same feature list.
    tif = TimeIndexFeaturizer()
    ts_params[TimeSeriesInternal.FORCE_TIME_INDEX_FEATURES_NAME] = tif.preview_time_feature_names(tsds)

    holiday_start_time = expr_store.metadata.timeseries.global_series_start
    holiday_end_time = expr_store.metadata.timeseries.global_series_end

    featurization_config.add_transformer_params(
        "TimeIndexFeaturizer",
        [],
        {"holiday_start_time": holiday_start_time, "holiday_end_time": holiday_end_time}
    )

    (
        forecasting_pipeline,
        timeseries_param_dict,
        lookback_removed,
        time_index_non_holiday_features
    ) = ml_engine.suggest_featurizers_timeseries(
        subsampled_X,
        subsampled_Y,
        featurization_config,
        ts_params,
        pipeline_type,
        categories_by_grain_cols,
        categories_by_non_grain_cols
    )

    ts_transformer = TimeSeriesTransformer(
        forecasting_pipeline,
        pipeline_type,
        featurization_config,
        time_index_non_holiday_features,
        lookback_removed,
        **timeseries_param_dict
    )

    PhaseUtil.log_with_memory("Suggest featurization invoked and transformer pipeline is ready to be fit")
    return ts_transformer


def _build_transformer_for_all_grains(
    training_dataset: TabularDataset,
    label_column_name: str,
    all_grain_keyvalues_and_path: List[_PartitionKeyValueCommonPath],
    ts_transformer_to_merge: TimeSeriesTransformer,
    grain_transform_results: List[_GrainTransformResult]
) -> TimeSeriesTransformer:
    """
    Build a single timeseries transformer, replacing any GrainBasedStatefulTransformer with an AggregateTransformer.

    :param training_dataset: A partitioned tabular dataset used to create the TSTs for each grain.
        This is used to re-fit a single TST to capture stateless transformers.
    :param label_column_name: The label column of the dataset.
    :param grain_column_names: A list of grain column names to be used in the aggregate transformers.
    :param all_grain_key_values: A list of dictionaries mapping grain column name to grain values.
    :ts_transforer_to_merge: An unfit timeseries transformer with all transformers present.
    :param statusful_trs_list: list of dictionaries mapping grain_col_values to dictionaries
        of transformer names to transformers for all stateful transformers
        [{grain_id: {tr_name: tr_obj}}]
    """
    PhaseUtil.log_with_memory("Beginning timeseries transformer aggregation")

    # Unpack the data from the grain_transform_results.
    grain_based_trs_to_combine = {}  # type: Dict[str, Dict[str, _GrainBasedStatefulTransformer]]
    grain_set = set()  # type: Set[str]
    dict_latest_dates = {}  # type: Dict[GrainType, pd.Timestamp]
    y_imputers = {}  # type: Dict[GrainType, TimeSeriesImputer]
    y_min_dict = {}  # type: Dict[GrainType, float]
    y_max_dict = {}  # type: Dict[GrainType, float]
    for result in grain_transform_results:
        grain_id, transformers_dict = result.stateful_transformers
        y_imputers.update(result.y_imputer)
        y_min_dict.update(result.y_min_dict)
        y_max_dict.update(result.y_max_dict)
        dict_latest_dates.update(result.latest_date)
        unique_target_dropper = transformers_dict.get(TimeSeriesInternal.UNIQUE_TARGET_GRAIN_DROPPER)
        if (unique_target_dropper is not None and not unique_target_dropper.has_unique_target_grains) or \
                unique_target_dropper is None:
            # Not use the unique target grain for _fit_bootstrap_transformer
            grain_set.add(grain_id)
        for transformer_name, transformer in transformers_dict.items():
            if transformer_name in grain_based_trs_to_combine:
                grain_based_trs_to_combine[transformer_name][grain_id] = transformer
            else:
                grain_based_trs_to_combine[transformer_name] = {grain_id: transformer}

    # Grab a TST to bootstrap the aggregation (allowing re-use of non-stateful transformers)
    _fit_bootstrap_transformer(
        ts_transformer_to_merge,
        all_grain_keyvalues_and_path,
        training_dataset=training_dataset,
        label_column_name=label_column_name,
        dict_latest_dates=dict_latest_dates,
        y_imputers=y_imputers,
        grain_set=grain_set,
        y_min_dict=y_min_dict,
        y_max_dict=y_max_dict
    )

    for tr_name, tr_dict in grain_based_trs_to_combine.items():
        if tr_name == TimeSeriesInternal.SHORT_SERIES_DROPPEER:
            tr_dict[AutoMLAggregateTransformer.DEFAULT_TRANSFORM] = AllRowsDropper()
        agg_tr = AggregatedTransformerFactory.create_aggregated_transformer(tr_dict)
        for idx, step in enumerate(ts_transformer_to_merge.pipeline.steps):  # type: ignore
            if step[0] == tr_name:
                break
        ts_transformer_to_merge.pipeline.steps[idx] = (tr_name, agg_tr)  # type: ignore
    PhaseUtil.log_with_memory("Ending timeseries transformer aggregation")
    return ts_transformer_to_merge


def _fit_bootstrap_transformer(
        tst: TimeSeriesTransformer, all_grain_keyvalues_and_path: List[_PartitionKeyValueCommonPath],
        training_dataset: TabularDataset, label_column_name: str,
        dict_latest_dates: Dict[GrainType, pd.Timestamp],
        y_imputers: Dict[GrainType, TimeSeriesImputer],
        grain_set: Set[str],
        y_min_dict: Dict[GrainType, float],
        y_max_dict: Dict[GrainType, float],
) -> TimeSeriesTransformer:
    """
    Fit the time series transformer and populate the internal data structures as if it was

    fit on all grains.
    :param tst: The time series transformer to be fit.
    :param all_grain_keyvalues_and_path: The list of _PartitionKeyValueCommonPath
    :param training_dataset: The tabular dataset to fit the data.
    :param dict_latest_dates: The dictionary with the latest dates for all long grains.
    :param y_imputers: The dictionary with y imputers for all grains.
    :param label_column_name: The target column name.
    :param grain_set: the set of string grain identifiers for long grains.
    :param y_min_dict: The dictionary with a minimal target value for a given grain.
    :param y_max_dict: The dictionary with a maximal target value for a given grain.
    :return: Fitted time series transformer.
    """
    # First we will fit the transform on first long grain.
    for grain_key_values_path in all_grain_keyvalues_and_path:
        grain_str = convert_grain_dict_to_str(grain_key_values_path.key_values)
        if grain_str in grain_set:
            training_dataset_for_grain = _get_dataset_for_grain(grain_key_values_path, training_dataset)
            bootstrap_X_grain = training_dataset_for_grain.to_pandas_dataframe()
            bootstrap_y_grain = bootstrap_X_grain.pop(label_column_name).values
            tst.fit_transform(bootstrap_X_grain, bootstrap_y_grain)
            break

    # Populate the filds of TimeseriesTransformer as if we have fit it on all the long grains.
    tst.dict_latest_date = dict_latest_dates
    tst._y_imputers = y_imputers
    for imputer in tst._y_imputers.values():
        imputer.freq = tst.freq_offset
    tst.y_min_dict = y_min_dict
    tst.y_max_dict = y_max_dict

    return tst


def set_global_statistics(expr_store: ExperimentStore,
                          log_transform_tests_list: List[LogTransformTestResults]) -> None:
    """Set the approporiate metadata in the experiment store."""
    expr_store.metadata.timeseries.apply_log_transform_for_label = \
        _should_apply_log_transform(log_transform_tests_list)

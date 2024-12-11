# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, Dict, Callable, Optional, List, cast, Union
from functools import partial
import json
import logging
import math
import multiprocessing
import os
import pandas as pd
from joblib import Parallel, delayed
from azureml.automl.core.shared import logging_utilities

from azureml.core import Run
from azureml.automl.runtime._time_series_data_set import TimeSeriesDataSet
from azureml.automl.core.shared.exceptions import ClientException
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml._common._error_definition.azureml_error import AzureMLError
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.shared._diagnostics.automl_error_definitions import ExplanationsNotFound

from ....data_models.node_columns_info import NodeColumnsInfo
from ....data_models.hts_graph import Graph
from ....data_models.hts_node import Node
from ..collect_step_wrapper import CollectStepWrapper
from .hts_data_aggregation_driver_v2 import HTSDataAggregationDriverV2
from .hts_automl_train_driver_v2 import HTSAutoMLTrainDriverV2
from .hts_setup_wrapper import HTSSetupWrapper
from .hts_inference_driver_v2 import HTSInferenceDriverV2
from ....utilities.json_serializer import HTSRuntimeDecoder
from ....utilities import run_utilities as ru
from ....utilities import logging_utilities as lu
from ....constants import HTSPipelineConstants, PipelineConstants, HTSConstants
from ....utilities.events.hts_collect_events import (
    ProportionsCalculationStart,
    ProportionsCalculationEnd,
    AllocationStart,
    AllocationEnd,
    ExplainStart,
    ExplainEnd
)


logger = logging.getLogger(__name__)


class HTSCollectWrapper(CollectStepWrapper):
    """The wrapper code for proportions calculation runs."""
    FILE_EXPLANATION_INFO_JSON = "explanation_info.json"
    FILE_PROPORTIONS = "metadata.json"
    FILE_PROPORTIONS_PARQUET = "metadata.parquet"
    FILE_GRAPH = "hts_graph.json"
    FILE_HTS_PREDICTION_CSV = "automl_hts_prediction.csv"
    FILE_HTS_PREDICTION_PARQUET = "automl_hts_prediction.parquet"
    DIR_EXPLAIN_OUTPUT = "explain_output"
    COL_CROSS_TIME_SUM = "_hts_cross_time_sum"
    AVERAGE_HISTORICAL_PROPORTIONS = "average_historical_proportions"
    PROPORTIONS_OF_HISTORICAL_AVERAGE = "proportions_of_historical_average"
    METADATA_JSON_METADATA = "metadata"
    JSON_VERSION = "version"

    def __init__(self, current_step_run: Optional[Run] = None, is_train: bool = True, **kwargs: Any):
        """
        The wrapper code for proportions calculation runs.

        :param current_step_run: The current step run.
        """
        super().__init__(
            HTSPipelineConstants.STEP_COLLECT if is_train else HTSPipelineConstants.STEP_COLLECT_INF,
            current_step_run, is_train, **kwargs
        )
        self.graph = self._get_graph_from_metadata_v2(self.input_setup_metadata)
        self.forecast_parameters = ru.get_forecasting_parameters(
            self._get_automl_settings_dict_v2(self.input_setup_metadata))
        self._allocated_df = pd.DataFrame()
        self._forecast_quantiles = self.inference_configs.forecast_quantiles

    def _collect(self) -> None:
        """Run code for the collect driver."""
        super(HTSCollectWrapper, self)._collect()
        if self._is_train:
            self.all_metadata[HTSCollectWrapper.FILE_PROPORTIONS] = HTSCollectWrapper.get_proportions_metadata_json(
                self._proportions_calculation(), self.graph
            )
            self.all_metadata[HTSCollectWrapper.FILE_GRAPH] = self.graph.serialize()
            try:
                self._explain_allocation()
            except Exception as e:
                print("Model Explanation failed due to {}".format(e))
                logging_utilities.log_traceback(
                    e, logger, override_error_msg="Model explanation for HTS failed", is_critical=False)
        else:
            self._allocation()

    # region Proportions Calculation
    @lu.event_log_wrapped(ProportionsCalculationStart(), ProportionsCalculationEnd())
    def _proportions_calculation(self) -> pd.DataFrame:
        self._print("Start calculating proportions now.")
        proportion_files_list = self.all_metadata[HTSDataAggregationDriverV2.POSTFIX_PROPORTIONS_FILE]
        df_cross_time_agg = self.calculate_time_agg_sum_for_all_files(
            proportion_files_list,
            self.forecast_parameters.time_column_name,
            self.graph.label_column_name
        )
        n_points = HTSCollectWrapper.get_n_points(
            df_cross_time_agg,
            self.forecast_parameters.time_column_name,
            self.graph.label_column_name,
            self.forecast_parameters.freq)
        total_value = df_cross_time_agg[self.graph.label_column_name].sum()
        dfs = []
        for proportion_file in proportion_files_list:
            df = pd.read_parquet(proportion_file)
            df_ahp = HTSCollectWrapper.calculate_average_historical_proportions(
                n_points, df, df_cross_time_agg, self.forecast_parameters.time_column_name,
                self.graph.label_column_name, self.graph.hierarchy)
            df_pha = HTSCollectWrapper.calculate_proportions_of_historical_average(
                df, self.graph.label_column_name, self.graph.hierarchy, total_value)
            dfs.append(pd.merge(df_ahp, df_pha))

        return pd.concat(dfs)

    @staticmethod
    def calculate_average_historical_proportions(
            n_points: int,
            df: pd.DataFrame,
            df_total: pd.DataFrame,
            time_column_name: str,
            label_column_name: str,
            hierarchy: List[str]
    ) -> pd.DataFrame:
        """
        Calculate average historical proportions based on two pd.DataFrames containing values after summation.

        :param n_points: number of total points
        :param df: The pd.DataFrame which taking summation by grouping the time column and bottom hierarchy level.
        :param df_total: The pd.DataFrame which taking summation by grouping the time column.
        :param time_column_name: The time column name.
        :param label_column_name: The column that contains the summations.
        :param hierarchy: The hierarchy column names.
        :return: pd.DataFrame
        """
        # Convert the time column to same type to avoid joining error
        df[time_column_name] = df[time_column_name].astype('object')
        df_total[time_column_name] = df_total[time_column_name].astype('object')
        df_total.rename(columns={label_column_name: HTSCollectWrapper.COL_CROSS_TIME_SUM}, inplace=True)

        merged_df = pd.merge(df, df_total, how='left', on=[time_column_name])
        merged_df[HTSCollectWrapper.AVERAGE_HISTORICAL_PROPORTIONS] = (
            merged_df[label_column_name] / merged_df[HTSCollectWrapper.COL_CROSS_TIME_SUM] / n_points)
        all_final_column = [col for col in hierarchy]
        all_final_column.append(HTSCollectWrapper.AVERAGE_HISTORICAL_PROPORTIONS)
        cols_to_agg = set(all_final_column) - set(hierarchy)
        return merged_df[all_final_column]. \
            groupby(hierarchy, group_keys=False, as_index=False). \
            apply(lambda c: c[cols_to_agg].abs().sum())

    @staticmethod
    def calculate_proportions_of_historical_average(
            df: pd.DataFrame, label_column_name: str, hierarchy: List[str], total_value: Union[float, int]
    ) -> pd.DataFrame:
        """
        Calculate proportions of historical average based on hierarchical timeseries allocation.

        :param df: The input pd.DataFrame.
        :param label_column_name: The column that needs to calculate the proportions of historical average.
        :param hierarchy: The hierarchy columns list.
        :param total_value: The total value which pha will be normalized by.
        :return: pd.DataFrame
        """
        all_final_column = [col for col in hierarchy]
        all_final_column.append(label_column_name)
        aggregated_df = df[all_final_column].groupby(hierarchy, group_keys=False) \
            .apply(lambda c: c.abs().sum()).reset_index()
        aggregated_df[label_column_name] = aggregated_df[label_column_name] / total_value
        aggregated_df.rename(
            columns={label_column_name: HTSCollectWrapper.PROPORTIONS_OF_HISTORICAL_AVERAGE}, inplace=True)
        return aggregated_df

    @staticmethod
    def get_n_points(
            input_data: pd.DataFrame, time_column_name: str, label_column_name: str, freq: Optional[str] = None
    ) -> int:
        """
        Get a number of points based on a TimeSeriesDataFrame.

        :param input_data: The input data.
        :param time_column_name: The time column name.
        :param label_column_name: The label column name.
        :param freq: The user input frequency.
        :return: int
        """
        tsds = TimeSeriesDataSet(
            input_data.copy(), time_column_name=time_column_name, target_column_name=label_column_name
        )
        if freq is None:
            dataset_freq = tsds.infer_freq()
        else:
            dataset_freq = freq
        return len(pd.date_range(start=tsds.time_index.min(), end=tsds.time_index.max(), freq=dataset_freq))

    @staticmethod
    def _get_files_batches_sqrt(files_list: List[str]) -> List[List[str]]:
        """
        Covert a list of files to a list of files batches which
        contains approximately sqrt(total_files) in each batch.

        :param files_list: A list of files.
        :return: List[List[str]]
        """
        n_files = len(files_list)
        n_batch = int(math.sqrt(n_files)) + 1
        files_batches = []
        for i in range(n_batch):
            if i * n_batch < n_files:
                end_idx = n_files if (i + 1) * n_batch > n_files else (i + 1) * n_batch
                files_batches.append(files_list[i * n_batch:end_idx])
        return files_batches

    @staticmethod
    def _concat_and_sum_by_time_for_files(
            file_names: List[str], time_column_name: str, label_column_name: str
    ) -> pd.DataFrame:
        """
        Concat all the df from the datafiles and return the time column absolute summation over label_column_name.
        """
        dfs = []
        for f in file_names:
            dfs.append(pd.read_parquet(f)[[time_column_name, label_column_name]])
        return HTSDataAggregationDriverV2.abs_sum_target_by_time(pd.concat(dfs), time_column_name, label_column_name)

    @staticmethod
    def calculate_time_agg_sum_for_all_files(
            proportion_files_list: List[str], time_column_name: str, label_column_name: str) -> pd.DataFrame:
        """
        Calculate groupby time aggregation for all files using multi core processing.

        :param proportion_files_list: A list of proportion calculated csv files.
        :param time_column_name: The time column name.
        :param label_column_name: The label column name.
        :return: pd.DataFrame
        """
        files_batches = HTSCollectWrapper._get_files_batches_sqrt(proportion_files_list)

        n_cpus = multiprocessing.cpu_count()
        concat_func = partial(
            HTSCollectWrapper._concat_and_sum_by_time_for_files,
            time_column_name=time_column_name, label_column_name=label_column_name)
        with multiprocessing.Pool(n_cpus) as pool:
            df = pd.concat(pool.map(concat_func, files_batches), ignore_index=True)
        return HTSDataAggregationDriverV2.abs_sum_target_by_time(df, time_column_name, label_column_name)

    @staticmethod
    def get_proportions_metadata_json(metadata_df: pd.DataFrame, graph: Graph) -> Dict[str, Any]:
        """
        Convert a pd.DataFrame containing proportion information to a json dict.

        :param metadata_df: The input dataframe.
        :param graph: The hts graph.
        :return: Dict[str, Any]
        """
        metadata_json_dict = {HTSCollectWrapper.JSON_VERSION: "1.0"}  # type: Dict[str, Any]
        metadata = []
        for _, row in metadata_df.iterrows():
            node_metadata = {
                col: row[col] for col in [HTSCollectWrapper.PROPORTIONS_OF_HISTORICAL_AVERAGE,
                                          HTSCollectWrapper.AVERAGE_HISTORICAL_PROPORTIONS]}
            node_metadata[Node.NODE_ID] = graph.get_node_by_name_list_raise_none(
                graph.get_leaf_node_name_list(row)).node_id
            metadata.append(node_metadata)
        metadata_json_dict[HTSCollectWrapper.METADATA_JSON_METADATA] = metadata
        return metadata_json_dict
    # endregion

    # region Model Explain
    @lu.event_log_wrapped(ExplainStart(), ExplainEnd())
    def _explain_allocation(self) -> None:
        explain_level = self.arguments_dict.get(PipelineConstants.ARG_FORECAST_LEVEL)
        explain_input = self.input_prs_metadata
        print("Explain input file {} with {}.".format(explain_input, os.listdir(explain_input)))
        enable_engineered_explanations = ru.str_or_bool_to_boolean(
            self.arguments_dict[PipelineConstants.ARG_ENGINEERED_EXPLANATION])
        explain_output = self._get_explanation_output_dir()

        all_levels = self.graph.hierarchy + [HTSConstants.HTS_ROOT_NODE_LEVEL]
        desired_levels = all_levels if explain_level is None else [explain_level]
        self._explain(desired_levels, explain_input, explain_output, True)
        if enable_engineered_explanations:
            self._explain(desired_levels, explain_input, explain_output, False)

    def _get_explanation_output_dir(self) -> str:
        return os.path.join(
            self.arguments_dict[PipelineConstants.ARG_OUTPUT_METADATA], HTSCollectWrapper.DIR_EXPLAIN_OUTPUT)

    def _explain(self,
                 desired_levels: List[str],
                 input_path: str,
                 output_path: str,
                 is_raw: bool) -> None:
        """
        Aggregate and allocate the explanations on all levels.

        :param desired_levels: The levels for which the explanations are requested.
        :param input_path: The dirrectory with explanations generated by the training run.
        :param output_path: The directory to write the files to.
        :param is_raw: The file with raw or engineered featues explanations.
        """
        explain_df = self.read_all_explanations(input_path, is_raw, False)

        expl_type = (HTSAutoMLTrainDriverV2.EXPLANATIONS_RAW_FEATURES if is_raw else
                     HTSAutoMLTrainDriverV2.EXPLANATIONS_ENGINEERED_FEATURES)
        if len(explain_df) == 0:
            logger.info("No explanations for {} features found.".format(
                expl_type))
            return

        logger.info("Successfully retrieved {} explanations.".format(expl_type))
        os.makedirs(output_path, exist_ok=True)

        # Run explanations in parallel if possible.
        cpu_cnt = os.cpu_count()
        if cpu_cnt is None or cpu_cnt <= 1:
            # There is only one core, or we did non detected cores.
            for lvl in desired_levels:
                self._explain_one_level(explain_df, self.graph, output_path, lvl, is_raw)
        else:
            # Several cores were detected, run in parallel.
            Parallel(n_jobs=cpu_cnt)(delayed(self._explain_one_level)(
                explain_df, self.graph, output_path, lvl, is_raw) for lvl in desired_levels)

    @staticmethod
    def _explain_one_level(
            explain_df: pd.DataFrame,
            graph: Graph,
            out_dir: str,
            explain_level: str,
            is_raw: bool
    ) -> None:
        """
        Aggregate or allocate the explanation on one level.

        :param explain_df: The data frame with explanations from the training level.
        :param out_dir: The directory to write the files to.
        :param explain_level: The level of explanations.
        :param is_raw: The file with raw or engineered featues explanations.
        """
        # If explanation level is not in the hierarchy_to_training_level, it is below it and
        # disaggregation is needed. The edge case is HTS_ROOT_NODE_LEVEL, which is never in
        # the hierarchy and in this case disaggregation is not needed.
        disaggregation_needed = (
            explain_level not in graph.hierarchy_to_training_level
            and explain_level != HTSConstants.HTS_ROOT_NODE_LEVEL
        )

        if disaggregation_needed:
            logger.info("Explanation level below training level, disaggregating to leaf nodes.")
            res = HTSCollectWrapper.disaggregate_predictions(
                explain_df,
                graph,
                "",
                {},
                HTSCollectWrapper.disaggregate_one_node,
                explain_level
            )
        else:
            logger.info("Explanation level above training level, no disaggregation required.")

            # If the explanation level is equal to the training level, or the forecast level is the leaf node level,
            # no aggregation is required.
            aggregation_needed = explain_level != graph.training_level \
                and (
                    explain_level == HTSConstants.HTS_ROOT_NODE_LEVEL
                    or explain_level in graph.hierarchy_to_training_level)

            if aggregation_needed:
                logger.info("Explanation level is above training level, beginning aggregation.")
                # If we are explaining above the training level, we are estimating the averages of all
                # explanations, included in the groups.
                if explain_level == HTSConstants.HTS_ROOT_NODE_LEVEL:
                    # The root level is special, because it includes all groups.
                    means_series = explain_df.apply('mean', axis=0)
                    res = pd.DataFrame([means_series.values], columns=means_series.index)
                else:
                    # Calculate averages only by groups which have to be merged.
                    group_columns = graph.hierarchy[:graph.hierarchy.index(explain_level) + 1]
                    res = explain_df.groupby(group_columns, as_index=False, group_keys=False).mean()
            else:
                logger.info("Explanation level is at training level.")
                res = explain_df

        res.to_csv(
            HTSCollectWrapper._get_file_name(out_dir, explain_level, is_raw),
            index=False)

    @staticmethod
    def _get_file_name(out_dir: str, explain_level: str, is_raw: bool, separator: str = '_') -> str:
        """
        Generate the name for the explanations file.

        :param out_dir: The directory to write the files to.
        :param explain_level: The level of explanations.
        :param is_raw: The file with raw or engineered features explanations.
        :param separator: The separator to be used in the file name.
        :return: The string with the path to be used to save the file.
        """
        if is_raw:
            file_name_lst = [HTSAutoMLTrainDriverV2.EXPLANATIONS_RAW_FEATURES]
        else:
            file_name_lst = [HTSAutoMLTrainDriverV2.EXPLANATIONS_ENGINEERED_FEATURES]
        file_name_lst.append('explanations')
        file_name_lst.append(explain_level + '.csv')
        return os.path.join(out_dir, separator.join(file_name_lst))

    @staticmethod
    def disaggregate_one_node(
            df: pd.DataFrame,
            node: Node,
            graph: Graph,
            parsed_metadata: Dict[str, Any],
            allocation_method: str,
            target_level: Optional[str],
            disagg_columns: List[str] = []
    ) -> pd.DataFrame:
        """
        Add bottom level nodes to the dataframe.

        This method takes a node and dataframe, and creates duplicate copies of the dataframe with the entire
        hierarchy from node to leaf nodes included.
        :param df: The input dataframe.
        :param node: The node to be used as a template.
        :param graph: The hierarchy graph generated during training.
        :param parsed_metadata: The metadata. Not used, added for function signature.
        :param allocation_method: The mehod used for allocation. Not used, added for function signature.
        :param target_level: The target explanation level.
        :param disagg_columns: List of columns to disaggregate. This parameter is ignored for explanations.
        :return:  duplicate copies of the dataframe with the entire hierarchy.
        """
        if target_level is None:
            # This is mypy fix as we always provide target_level to this function.
            return pd.DataFrame()
        # If training index is root, well add the entire hierarchy
        # otherwise we only need to update the nodes from training to leaf.
        if graph.training_level != HTSConstants.HTS_ROOT_NODE_LEVEL:
            start_col = graph.hierarchy.index(graph.training_level) + 1
        else:
            start_col = 0
        end_col = graph.hierarchy.index(target_level)
        explanation_cols = list(filter(lambda col: col not in graph.hierarchy, df.columns))

        logger.info("retrieving children for node: {}".format(node.node_id))
        children = graph.get_children_of_level(node, target_level)

        if children:
            results = []
            for child in children:
                # Update all our predictions so all leaf nodes are represented.
                c_pred = df.copy(deep=True)
                runner = child
                for _ in range(start_col, end_col + 1):
                    # Update the hierarchy with of each leaf node with
                    # the child's relative tree path up to training level.
                    c_pred[runner.level] = runner.name
                    # order the data frame to look better.
                    runner = cast(Node, runner.parent)
                c_pred = c_pred[graph.hierarchy[:end_col + 1] + explanation_cols]
                results.append(c_pred)
            logger.info("Updated explanations for {} children.".format(len(children)))
            return pd.concat(results, sort=False, ignore_index=True)
        # If there is no children, just return the initial data frame.
        return df.copy(deep=True)

    def read_all_explanations(
            self,
            explanation_dir: str,
            raw: bool,
            except_on_no_explanation: bool) -> pd.DataFrame:
        """
        Read all the explanations and organize it to the data frame.

        :param explanation_dir: The directory with the explanations.
        :param raw: If True, raw explanations will be used, engineered
                    explanations will be used otherwise.
        :param except_on_no_explanation: Raise an exception if the explanation is absent.
        :return: The data frame with collected explanations.
        """
        node_list = self.graph.get_children_of_level(cast(Node, self.graph.root), self.graph.training_level)
        explanation_dir = os.path.join(explanation_dir, HTSAutoMLTrainDriverV2.HTS_DIR_EXPLANATIONS)
        expanation_list = []
        if os.path.isdir(explanation_dir):
            file_list = os.listdir(explanation_dir)
            for node in node_list:
                file_name = HTSAutoMLTrainDriverV2.get_explanation_artifact_name(raw, node.node_id)
                if file_name not in file_list:
                    logger.warn("The file {} was not found. The explanations may not be coherent.".format(file_name))
                    continue
                with open(os.path.join(explanation_dir, file_name)) as f:
                    artifacts_dict = json.load(f)
                current_node = node
                while current_node.name != HTSConstants.HTS_ROOT_NODE_NAME:
                    artifacts_dict[current_node.level] = current_node.name
                    current_node = cast(Node, current_node.parent)
                expanation_list.append(artifacts_dict)
        if not expanation_list:
            if except_on_no_explanation:
                expl_type = (HTSAutoMLTrainDriverV2.EXPLANATIONS_RAW_FEATURES if raw else
                             HTSAutoMLTrainDriverV2.EXPLANATIONS_ENGINEERED_FEATURES)
                raise ClientException._with_error(
                    AzureMLError.create(ExplanationsNotFound,
                                        exp_type=expl_type,
                                        target='explanations',
                                        reference_code=ReferenceCodes._HTS_NO_EXPLANATION)
                )
            else:
                return pd.DataFrame()
        return pd.DataFrame(expanation_list)
    # endregion

    # region Allocation
    @lu.event_log_wrapped(AllocationStart(), AllocationEnd())
    def _allocation(self) -> None:
        self._print("Start calculating allocation now.")
        inference_configs = HTSSetupWrapper._get_inference_configs_from_metadata_dir(self.input_setup_metadata)
        forecasting_level = cast(str, inference_configs.forecast_level)
        parsed_metadata = self.get_parsed_metadata()
        # Skip disaggregation if forecast level is above training level and not the root level
        disaggregation_needed = (
            forecasting_level not in self.graph.hierarchy_to_training_level
            and forecasting_level != HTSConstants.HTS_ROOT_NODE_LEVEL
        )

        self._allocated_df = cast(pd.DataFrame, self._predict_df).copy()
        if disaggregation_needed:
            logger.info("Forecast level below training level, disaggregating to leaf nodes.")
            self._allocated_df = HTSCollectWrapper.disaggregate_predictions(
                self._allocated_df, self.graph, cast(str, inference_configs.allocation_method),
                parsed_metadata, HTSCollectWrapper.add_children_to_df,
                forecast_quantiles=self._forecast_quantiles
            )
        else:
            logger.info("Forecast level above current allocation level, no disaggregation required.")

            # If the forecast level is equal to the training level, or the forecast level is the leaf node level,
            # no aggregation is required.
        aggregation_needed = forecasting_level != self.graph.training_level and\
            forecasting_level != self.graph.hierarchy[-1]
        gby_columns = self.graph.forecasting_group_by_levels(forecasting_level)
        if HTSInferenceDriverV2.FORECAST_ORIGIN_COLUMN in self._allocated_df.columns:
            # Add the forecast origin column to the groupby columns if its in the data
            gby_columns.append(HTSInferenceDriverV2.FORECAST_ORIGIN_COLUMN)
        if aggregation_needed:
            logger.info("Forecast level is above current allocated forecast level, beginning aggregation.")
            self._allocated_df = self._allocated_df.groupby(gby_columns).sum().reset_index()
        else:
            logger.info("Forecast level is at current allocated forecast level.")
        preds_col = [HTSConstants.PREDICTION_COLUMN]
        if self._forecast_quantiles:
            preds_col = [
                HTSInferenceDriverV2.generate_quantile_forecast_column_name(q) for q in self._forecast_quantiles]
        keep_cols_list = gby_columns + preds_col
        if HTSConstants.ACTUAL_COLUMN in self._allocated_df.columns:
            keep_cols_list.append(HTSConstants.ACTUAL_COLUMN)
        self._allocated_df = self._allocated_df[[col for col in self._allocated_df.columns if col in keep_cols_list]]

    @property
    def result_df(self) -> pd.DataFrame:
        """The dataframe that contains the final results."""
        return self._allocated_df

    def _save_metadata_prediction(self) -> None:
        super()._save_metadata_prediction()
        self._print("writing hts prediction dataframe {} with columns {}".format(
            self._allocated_df, self._allocated_df.columns))
        self._allocated_df.to_csv(
            os.path.join(self.output_metadata, HTSCollectWrapper.FILE_HTS_PREDICTION_CSV), index=False)
        self._allocated_df.to_parquet(
            os.path.join(self.output_metadata, HTSCollectWrapper.FILE_HTS_PREDICTION_PARQUET), index=False)

    def get_parsed_metadata(self) -> Dict[str, Any]:
        """
        Get the metadata parsed as a dict from artifacts.

        :return: Dict[str, Any]
        """
        raw_metadata_file = os.path.join(self.input_setup_metadata, HTSCollectWrapper.FILE_PROPORTIONS)
        with open(raw_metadata_file) as f:
            raw_metadata = json.load(f)

        parsed_metadata = {}
        for metadata_node in raw_metadata[HTSCollectWrapper.METADATA_JSON_METADATA]:
            node_id = metadata_node[Node.NODE_ID]
            parsed_metadata[node_id] = {
                HTSCollectWrapper.PROPORTIONS_OF_HISTORICAL_AVERAGE:
                    metadata_node[HTSCollectWrapper.PROPORTIONS_OF_HISTORICAL_AVERAGE],
                HTSCollectWrapper.AVERAGE_HISTORICAL_PROPORTIONS:
                    metadata_node[HTSCollectWrapper.AVERAGE_HISTORICAL_PROPORTIONS]
            }
        try:
            os.remove(raw_metadata_file)
        except Exception as e:
            self._print(f"Remove metadata file met {e}.")
        return parsed_metadata

    @staticmethod
    def add_children_to_df(
            df: pd.DataFrame,
            node: Node,
            graph: Graph,
            parsed_metadata: Dict[str, Any],
            allocation_method: str,
            target_level: str,
            disagg_columns: List[str] = [HTSAutoMLTrainDriverV2.PREFIX_MODEL_NAME]
    ) -> pd.DataFrame:
        """
        Add bottom level nodes to the dataframe.

        This method takes a node and dataframe, and creates duplicate copies of the dataframe with the entire
        hierarchy from node to leaf nodes included.
        """
        results: List[pd.DataFrame] = []
        # If training index is root, well add the entire hierarchy
        # otherwise we only need to update the nodes from training to leaf.
        cols_to_update = len(graph.hierarchy)
        if graph.training_level != HTSConstants.HTS_ROOT_NODE_LEVEL:
            cols_to_update -= graph.hierarchy.index(graph.training_level)

        logger.info("retrieving children for node: {}".format(node.node_id))
        children = graph.get_leaf_nodes_by_node(node)
        parent_allocation = sum([parsed_metadata[child.node_id][allocation_method] for child in children])

        if children:
            for child in children:
                # Update all our predictions so all leaf nodes are represented.
                c_pred = df.copy(deep=True)
                runner = child
                for _ in range(cols_to_update):
                    # Update the hierarchy with of each leaf node with
                    # the child's relative tree path up to training level.
                    c_pred[runner.level] = runner.name
                    runner = cast(Node, runner.parent)
                allocation_proportion = parsed_metadata[child.node_id][allocation_method] / parent_allocation
                # As we calculate the proportions in the training part by normalized to the root level,
                # renormalization is needed for all the child nodes of the interested nodes to ensure the
                # proportion is correct in the sub tree of the leaf nodes.
                for col in disagg_columns:
                    Contract.assert_true(col in c_pred.columns,
                                         f'Allocation expected column {col} in the raw forecasts.',
                                         log_safe=True)
                    c_pred[col] = c_pred[col] * allocation_proportion
                keep_cols_list = graph.forecasting_group_by_levels(graph.hierarchy[-1])
                if HTSInferenceDriverV2.FORECAST_ORIGIN_COLUMN in c_pred.columns:
                    keep_cols_list.append(HTSInferenceDriverV2.FORECAST_ORIGIN_COLUMN)
                keep_cols_list.extend(disagg_columns)
                results.append(c_pred[keep_cols_list])
            logger.info("Updated predictions for {} children.".format(len(children)))
        return pd.concat(results)

    # endregion

    @staticmethod
    def get_intermediate_file_postfix(filename: str) -> Optional[str]:
        if filename.endswith(HTSDataAggregationDriverV2.POSTFIX_PROPORTIONS_FILE):
            return HTSDataAggregationDriverV2.POSTFIX_PROPORTIONS_FILE
        elif filename.endswith(HTSDataAggregationDriverV2.POSTFIX_NODE_COLUMNS_INFO_JSON):
            return HTSDataAggregationDriverV2.POSTFIX_NODE_COLUMNS_INFO_JSON
        elif filename.endswith(HTSDataAggregationDriverV2.POSTFIX_ENG_COL_INFO_JSON):
            return HTSDataAggregationDriverV2.POSTFIX_ENG_COL_INFO_JSON
        elif filename.endswith(HTSAutoMLTrainDriverV2.POSTFIX_EXPLANATION_INFO_JSON):
            return HTSAutoMLTrainDriverV2.POSTFIX_EXPLANATION_INFO_JSON
        return CollectStepWrapper.get_intermediate_file_postfix(filename)

    @staticmethod
    def disaggregate_predictions(
            preds_df: pd.DataFrame,
            graph: Graph,
            allocation_method: str,
            parsed_metadata: Dict[str, Any],
            disagg_one_node_fun: Callable[..., pd.DataFrame],
            target_level: Optional[str] = None,
            forecast_quantiles: Optional[List[float]] = None
    ) -> pd.DataFrame:
        """
        Disaggregate the model predictions.

        This method takes the model predictions from the training level and disaggregates
        to the leaf nodes. It uses the allocaiton_method and parsed_metadata to determine
        what proportion of predictions to allocate towards each leaf node.

        :param preds_df: Dataframe containing predictions from the training_level.
        :param graph: Graph from the data used for training models used to create preds_df.
        :param allocation_method: Method to use for forecast allocations. Should be present in parsed_metadata.
        :param parsed_metadata: Dictionary containing disaggregation proportions. The schema is assumed to be
            node_id: {allocation_method: allocation_proportion}
        :param target_level: The level, which will be used for disaggregation.
        :param disagg_one_node_fun: The function to be used for disaggregation of a given node.
        :param forecast_quantiles: The forecast quantiles.
        :returns: The predictions allocated to the leaf node level.
        """
        # Determine which columns need disaggregation
        if forecast_quantiles:
            disagg_cols = [HTSInferenceDriverV2.generate_quantile_forecast_column_name(q) for q in forecast_quantiles]
        else:
            disagg_cols = [HTSConstants.PREDICTION_COLUMN]
        if HTSConstants.ACTUAL_COLUMN in preds_df.columns:
            disagg_cols.append(HTSConstants.ACTUAL_COLUMN)
        partial_res = []
        if graph.training_level == HTSConstants.HTS_ROOT_NODE_LEVEL:
            node = cast(Node, graph.root)
            Contract.assert_non_empty(
                node, "node", reference_code=ReferenceCodes._HTS_ALLOCATION_NOT_FOUND_NODE_TOP_LEVEL
            )
            res = disagg_one_node_fun(
                preds_df, node, graph, parsed_metadata, allocation_method, target_level,
                disagg_columns=disagg_cols)
            partial_res.append(res)
        else:
            for k, grp in preds_df.groupby(graph.hierarchy_to_training_level):
                if not isinstance(k, tuple):
                    # if k is a single value this condition is hit.
                    k = [k]
                else:
                    k = list(k)
                node = graph.get_node_by_name_list_raise_none(k)
                Contract.assert_non_empty(
                    node, "node", reference_code=ReferenceCodes._HTS_ALLOCATION_NOT_FOUND_NODE
                )
                res = disagg_one_node_fun(
                    grp, node, graph, parsed_metadata, allocation_method, target_level, disagg_columns=disagg_cols)
                partial_res.append(res)
        return pd.concat(partial_res, sort=False, ignore_index=True)

    def deserialize_metadata_file(self, full_file_path: str) -> Any:
        if full_file_path.endswith(HTSDataAggregationDriverV2.POSTFIX_NODE_COLUMNS_INFO_JSON):
            with open(full_file_path) as f:
                node_column_info = cast(NodeColumnsInfo, json.load(f, cls=HTSRuntimeDecoder))
                node = self.graph.get_node_by_id(node_column_info.node_id)
                if node is not None:
                    node.ignored_columns_types_dict = node_column_info.get_ignored_columns_dict(
                        self.graph.agg_exclude_columns)
                return node_column_info
        elif full_file_path.endswith(HTSAutoMLTrainDriverV2.POSTFIX_EXPLANATION_INFO_JSON):
            with open(full_file_path) as f:
                return json.load(f, cls=HTSRuntimeDecoder)
        elif full_file_path.endswith(HTSDataAggregationDriverV2.POSTFIX_PROPORTIONS_FILE):
            return full_file_path
        else:
            return super(HTSCollectWrapper, self).deserialize_metadata_file(full_file_path)

    def get_dump_files_dict(self) -> Dict[str, str]:
        dumps_dict_base = {k: v for k, v in super(HTSCollectWrapper, self).get_dump_files_dict().items()}
        if not self._is_train:
            return dumps_dict_base
        return dict({
            HTSDataAggregationDriverV2.POSTFIX_ENG_COL_INFO_JSON: HTSCollectWrapper.FILE_EXPLANATION_INFO_JSON,
            HTSDataAggregationDriverV2.POSTFIX_NODE_COLUMNS_INFO_JSON: HTSSetupWrapper.FILE_NODE_COLUMNS_INFO_JSON,
            HTSCollectWrapper.FILE_PROPORTIONS: HTSSetupWrapper.FILE_PROPORTIONS},
            **dumps_dict_base
        )

    def _get_copy_files(self) -> List[str]:
        copy_files = super()._get_copy_files()
        copy_files.append(HTSSetupWrapper.FILE_GRAPH)
        return copy_files

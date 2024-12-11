# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Contains data utilities for V1 Many Models and HTS runs."""
from typing import Any, Dict, Callable, Optional, List, Generator, Union, Tuple
import os
import pandas as pd

from azureml.train.automl.constants import HTSConstants

from ..data_models.hts_graph import Graph
from ..pipeline_run.steps.setup_step_wrapper import SetupStepWrapper
from ..pipeline_run.steps.hts.hts_collect_wrapper import HTSCollectWrapper
from ..pipeline_run.steps.hts.hts_data_aggregation_driver_v2 import HTSDataAggregationDriverV2


def fill_na_with_space(df: pd.Series) -> pd.Series:
    return Graph.fill_na_with_space(df)


def concat_df_with_none(df: Optional[pd.DataFrame], update_df: pd.DataFrame) -> pd.DataFrame:
    """
    Concat two dataframes. If the first one is None, then return the second one. If not, return the concat result of
    these two dataframe.

    :param df: First pd.DataFrame that can be None.
    :param update_df: Second pd.DataFrame.
    :return: The concat pd.DataFrame of these two.
    """
    return SetupStepWrapper.concat_df_with_none(df, update_df)


def abs_sum_target_by_time(
        df: pd.DataFrame,
        time_column_name: str,
        label_column_name: str,
        other_column_names: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Calculate the absolute sum value of a dataframe by the time_column_name.

    :param df: The input df.
    :param time_column_name: The time column name.
    :param label_column_name: The column name contains the values that needs to be take summation.
    :param other_column_names: Other column name that won't need group by.
    :return: pd.DataFrame
    """
    return HTSDataAggregationDriverV2.abs_sum_target_by_time(
        df, time_column_name, label_column_name, other_column_names)


def get_cross_time_df(
        df_sum: Optional[pd.DataFrame],
        df: pd.DataFrame,
        time_column_name: str,
        label_column_name: str
) -> pd.DataFrame:
    """
    Calculate the absolute summation of a pd.DataFrame with another dataframe based on time_column_name.

    :param df_sum: First pd.DataFrame which can be None.
    :param df: Second pd.DataFrame.
    :param time_column_name: The time column name.
    :param label_column_name: The column name contains the values that needs to be take summation.
    :return: pd.DataFrame
    """
    group_df_sum = abs_sum_target_by_time(df, time_column_name, label_column_name)
    if df_sum is None:
        return group_df_sum
    else:
        return abs_sum_target_by_time(
            pd.concat([df_sum, group_df_sum]), time_column_name, label_column_name)


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
    return HTSCollectWrapper.get_n_points(input_data, time_column_name, label_column_name, freq)


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
    return HTSCollectWrapper.calculate_average_historical_proportions(
        n_points, df, df_total, time_column_name, label_column_name, hierarchy
    )


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
    return HTSCollectWrapper.calculate_proportions_of_historical_average(
        df, label_column_name, hierarchy, total_value
    )


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load a csv file or a parquet file into memory as pd.DataFrame

    :param file_path: The file path.
    :return: pd.DataFrame
    """
    return SetupStepWrapper.load_data_from_file(file_path)


def get_input_data_generator(local_file_path: str) -> Generator[Tuple[pd.DataFrame, str], None, None]:
    """
    Generate pd.DataFrame from an input dataset or a local file path.

    :param local_file_path: The dir contains all the local data files.
    :return: None
    """
    for file in os.listdir(local_file_path):
        print("Processing collected {}.".format(file))
        yield pd.read_csv(os.path.join(local_file_path, file)), file


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
    :returns: The predictions allocated to the leaf node level.
    """
    return HTSCollectWrapper.disaggregate_predictions(
        preds_df, graph, allocation_method, parsed_metadata, disagg_one_node_fun, target_level, forecast_quantiles)


def generate_quantile_forecast_column_name(quantile: float) -> str:
    """Generate predict quantiles column name for sdk v1."""
    """Generate a column name for quantile forecast from the quantile value."""
    return f'{HTSConstants.PREDICTION_COLUMN}_{str(quantile)}'

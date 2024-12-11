# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import cast, Dict, Optional, Any
import logging
import numpy as np
import pandas as pd

from azureml.core import Run
from azureml._common._error_definition import AzureMLError
from azureml.automl.runtime.shared import utilities as runtime_utilities
from azureml.automl.core.shared.exceptions import DataException
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    InconsistentColumnTypeInTrainValid,
    MissingData
)
from azureml.automl.core.shared.reference_codes import ReferenceCodes

from ....data_models.arguments import Arguments
from ....data_models.hts_graph import Graph
from ....data_models.hts_node import Node
from ....data_models.node_columns_info import NodeColumnsInfo
from ....constants import HTSConstants, PipelineConstants
from ..automl_inference_driver import AutoMLPRSInferenceDriver


logger = logging.getLogger(__name__)


class HTSInferenceDriverV2(AutoMLPRSInferenceDriver):
    """Inference driver code for HTS v2."""
    def __init__(
            self,
            current_step_run: Run,
            args: Arguments,
            **kwargs: Any
    ) -> None:
        """
        This class is used for doing batch inference.

        :param current_step_run: Current step run object, parent of AutoML run.
        :param args: The arguments for the run.
        """
        super().__init__(current_step_run, args, **kwargs)
        self.graph = cast(Graph, args.hts_graph)
        self._node_columns_info = cast(Dict[str, NodeColumnsInfo], args.node_columns_info)

    def try_convert_inference_data(
            self,
            df: pd.DataFrame,
            columns_types:
            Dict[str, np.dtype]
    ) -> pd.DataFrame:
        """
        Try to check the type and convert the type of the inference data with trying data. It will raise BadData if
        the input is inconsistent.

        :param df: The input df.
        :param columns_types: The dict contains columns to types mapping.
        :return: pd.DataFrame
        """
        if not columns_types:
            logger.warn("Receive empty columns types dict. Skipping type conversion now.")
            return df

        for col in df:
            if col not in columns_types:
                self._console_writer.println("{} cannot be found in training data, skipping now...".format(col))
                logger.warn("column not found in training data, skipping now...")
            else:
                old_col_type = df[col].dtype
                if old_col_type != columns_types[col]:
                    try:
                        df[col] = df[col].astype(columns_types[col])
                        self._console_writer.println(
                            "Column {} successfully converted from type {} to {}.".format(
                                col, old_col_type, columns_types[col]))
                    except Exception as e:
                        input_dtype = runtime_utilities._get_column_data_type_as_str(df[col])
                        self._console_writer.println(
                            "Exception when trying to convert a column with inconsistent types: {}".format(e))
                        raise DataException._with_error(
                            AzureMLError.create(
                                InconsistentColumnTypeInTrainValid,
                                target="X",
                                reference_code=ReferenceCodes._HTS_FORECAST_PARALLEL_INCONSISTENT_DATA,
                                column_name=col,
                                train_dtype=columns_types[col],
                                validation_dtype=input_dtype
                            )
                        )
        return df

    def _preprocess_data_one_partition(self, df: pd.DataFrame) -> Optional[pd.DataFrame]:
        if self.graph.training_level == HTSConstants.HTS_ROOT_NODE_LEVEL:
            node = cast(Node, self.graph.root)
        else:
            node = cast(Node, self.graph.get_training_level_node_by_df_first_row(df))
        if node.node_id not in self._node_columns_info:
            raise DataException._with_error(
                AzureMLError.create(
                    MissingData,
                    target="X",
                    data_argument_name=f"node_id {node.node_id}"
                )
            )
        vocab_dict = self._node_columns_info[node.node_id].columns_vocabulary
        df = self.try_convert_inference_data(df, self._node_columns_info[node.node_id].columns_types)
        agg_df, _ = self.graph.aggregate_data_single_group(
            df,
            vocab_dict
        )
        return agg_df

    def _get_empty_df(self) -> pd.DataFrame:
        return self.graph.get_empty_df()

    def _add_training_hierarchy_columns(self, agg_df: pd.DataFrame, pred_df: pd.DataFrame) -> pd.DataFrame:
        """Add the hierarchy columns for the training level to the prediction data if necessary."""
        ret_df = pred_df
        if not all([col in pred_df.columns for col in self.graph.hierarchy_to_training_level]):
            ret_df = pred_df.assign(**agg_df[self.graph.hierarchy_to_training_level].iloc[0].to_dict())

        return ret_df

    def _post_process_predictions_rolling(
            self,
            predictions: pd.DataFrame,
            input_data: pd.DataFrame,
            rename_dict: Dict[Any, str]
    ) -> pd.DataFrame:
        return self._post_process_predictions_non_recursive(predictions, input_data, rename_dict)

    def _post_process_predictions_quantiles(
            self,
            predictions: pd.DataFrame,
            input_data: pd.DataFrame,
            rename_dict: Dict[Any, str]
    ) -> pd.DataFrame:
        return self._post_process_predictions_non_recursive(predictions, input_data, rename_dict)

    def _post_process_predictions_recursive(
            self,
            predictions: pd.DataFrame
    ) -> pd.DataFrame:
        preserve_cols = [HTSConstants.PREDICTION_COLUMN]
        return self.graph.preserve_hts_col_for_df(predictions, preserve_cols)

    def _post_process_predictions_non_recursive(
            self, predictions: pd.DataFrame,
            input_data: pd.DataFrame,
            rename_dict: Dict[str, str]
    ) -> pd.DataFrame:
        predictions = self._add_training_hierarchy_columns(input_data, predictions)
        preserve_cols = list(rename_dict.values())
        return self.graph.preserve_hts_col_for_df(predictions, preserve_cols)

    @property
    def run_type(self) -> str:
        # This run_type needs to be consistent in train and inference drivers in order to correctly
        # retrieve the model.
        return PipelineConstants.RUN_TYPE_HTS

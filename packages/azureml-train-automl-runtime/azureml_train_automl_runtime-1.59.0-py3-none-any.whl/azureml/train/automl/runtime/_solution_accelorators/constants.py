# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from azureml.train.automl.constants import HTSConstants


class ManyModelsPipelineConstants:
    STEP_SETUP = "ManyModelsSetupStep"
    STEP_AUTOML_TRAIN = "ManyModelsAutoMLTrainV2"
    STEP_COLLECT = "ManyModelsCollect"
    STEP_SETUP_INF = "ManyModelsSetupStepInf"
    STEP_INFERENCE = "ManyModelsInferenceV2"
    STEP_COLLECT_INF = "ManyModelsCollectInference"

    ALLOW_MULTI_PARTITIONS = "allow_multi_partitions"


class HTSPipelineConstants:
    STEP_SETUP = "HTSSetupStep"
    STEP_DATA_AGGREGATION = "HTSDataAggregationV2"
    STEP_AUTOML_TRAIN = "HTSAutoMLTrainV2"
    STEP_COLLECT = "HTSCollect"
    STEP_SETUP_INF = "HTSSetupInference"
    STEP_INFERENCE = "HTSInferenceV2"
    STEP_COLLECT_INF = "HTSCollectInference"


class PipelineConstants:
    ARG_ALLOW_MULIT_PARTITIONS = "--allow-multi-partitions"
    ARG_RAW_DATA = "--raw-data"
    ARG_INPUT_CONFIG = "--input-config"
    ARG_INPUT_METADATA = "--input-metadata"
    ARG_OUTPUT_AGG_DATA = "--output-agg-data"
    ARG_PROCESSED_DATA = "--processed-data"
    ARG_PRS_STEP_TIMEOUT = "--prs-step-timeout"
    ARG_ENABLE_EVENT_LOGGER = "--enable-event-logger"
    ARG_OUTPUT_METADATA = "--output-metadata"
    ARG_NODES_COUNT = "--nodes-count"
    ARG_ENGINEERED_EXPLANATION = "--enable-engineered-explanation"
    ARG_DATA_AGG_METADATA = "--data-agg-metadata"
    ARG_TRAIN_RUN_ID = "--train-run-id"
    ARG_VALIDATION_FAIL_EARLY = "--fail-early"
    ARG_EXPERIMENT_NAME = "--train-experiment-name"
    ARG_PARTITION_COLUMN_NAMES = "--partition-column-names"
    ARG_FORECAST_LEVEL = "--forecast-level"
    ARG_OUTPUT_PREDICT = "--output-prediction"
    ARG_INFERENCE_TYPE = "--inference-type"
    ARG_FORECAST_QUANTILES = "--forecast-quantiles"
    ARG_FORECAST_MODE = "--forecast-mode"
    ARG_FORECAST_STEP = "--forecast-step"
    ARG_ALLOCATION_METHOD = "--allocation-method"
    ARG_INPUT_PREDICT = "--input-prediction"
    ARG_NODE_PROCESS_COUNT = "--node-process-count"
    ARG_RETRAIN_FAILED_MODEL = "--retrain-failed-model"
    ARG_SETUP_METADATA = "--setup-metadata"
    ARG_SKIP_CONCAT_RESULTS = "--skip-concat-results"
    ARG_TRAIN_METADATA = "--optional-train-metadata"
    ARG_OUTPUT_EVALUATION_CONFIGS = "--output-evaluation-configs"
    ARG_OUTPUT_EVALUTAION_DATA = "--output-evaluation-data"
    ARG_TARGET_COLUMN_NAME = "--target-column-name"
    ARG_INTERNAL_SKIP_DATA_ACCESS = "--skip-data-access-internal"

    SDK_V1 = "SDK_V1"
    SDK_V2 = "SDK_V2"

    SCRIPTS_SCENARIO_ARG_DICT = dict(
        {
            ManyModelsPipelineConstants.STEP_SETUP: [
                ARG_OUTPUT_METADATA, ARG_RAW_DATA, ARG_PROCESSED_DATA, ARG_ENABLE_EVENT_LOGGER, ARG_INPUT_CONFIG,
                ARG_PRS_STEP_TIMEOUT, ARG_NODES_COUNT, ARG_NODE_PROCESS_COUNT, ARG_VALIDATION_FAIL_EARLY,
                ARG_INTERNAL_SKIP_DATA_ACCESS
            ],
            HTSPipelineConstants.STEP_SETUP: [
                ARG_OUTPUT_METADATA, ARG_RAW_DATA, ARG_PROCESSED_DATA, ARG_ENABLE_EVENT_LOGGER, ARG_INPUT_CONFIG,
                ARG_PRS_STEP_TIMEOUT, ARG_NODES_COUNT, ARG_NODE_PROCESS_COUNT
            ],
            HTSPipelineConstants.STEP_DATA_AGGREGATION: [
                ARG_INPUT_METADATA, ARG_OUTPUT_AGG_DATA, ARG_ENABLE_EVENT_LOGGER, ARG_OUTPUT_METADATA,
                ARG_NODES_COUNT, ARG_NODE_PROCESS_COUNT
            ],
            ManyModelsPipelineConstants.STEP_AUTOML_TRAIN: [
                ARG_INPUT_METADATA, ARG_OUTPUT_METADATA, ARG_ENABLE_EVENT_LOGGER, ARG_NODES_COUNT,
                ARG_NODE_PROCESS_COUNT, ARG_RETRAIN_FAILED_MODEL
            ],
            HTSPipelineConstants.STEP_AUTOML_TRAIN: [
                ARG_INPUT_METADATA, ARG_OUTPUT_METADATA, ARG_ENABLE_EVENT_LOGGER, ARG_NODES_COUNT,
                ARG_ENGINEERED_EXPLANATION, ARG_NODE_PROCESS_COUNT, ARG_DATA_AGG_METADATA
            ],
            ManyModelsPipelineConstants.STEP_COLLECT: [
                ARG_INPUT_METADATA, ARG_SETUP_METADATA, ARG_OUTPUT_METADATA, ARG_ENABLE_EVENT_LOGGER],
            HTSPipelineConstants.STEP_COLLECT: [
                ARG_INPUT_METADATA, ARG_SETUP_METADATA, ARG_OUTPUT_METADATA, ARG_ENABLE_EVENT_LOGGER,
                ARG_ENGINEERED_EXPLANATION
            ],
            ManyModelsPipelineConstants.STEP_SETUP_INF: [
                ARG_OUTPUT_METADATA, ARG_RAW_DATA, ARG_PROCESSED_DATA, ARG_ENABLE_EVENT_LOGGER,
                ARG_TRAIN_RUN_ID, ARG_EXPERIMENT_NAME, ARG_PARTITION_COLUMN_NAMES, ARG_FORECAST_MODE,
                ARG_FORECAST_STEP, ARG_FORECAST_QUANTILES, ARG_INFERENCE_TYPE, ARG_PRS_STEP_TIMEOUT,
                ARG_NODES_COUNT, ARG_NODE_PROCESS_COUNT, ARG_ALLOW_MULIT_PARTITIONS,
                ARG_SKIP_CONCAT_RESULTS, ARG_TRAIN_METADATA, ARG_VALIDATION_FAIL_EARLY,
                ARG_TARGET_COLUMN_NAME,
                ARG_INTERNAL_SKIP_DATA_ACCESS
            ],
            HTSPipelineConstants.STEP_SETUP_INF: [
                ARG_OUTPUT_METADATA, ARG_RAW_DATA, ARG_PROCESSED_DATA, ARG_ENABLE_EVENT_LOGGER,
                ARG_TRAIN_RUN_ID, ARG_EXPERIMENT_NAME, ARG_FORECAST_MODE, ARG_FORECAST_STEP, ARG_ALLOCATION_METHOD,
                ARG_FORECAST_LEVEL, ARG_PRS_STEP_TIMEOUT, ARG_NODES_COUNT, ARG_NODE_PROCESS_COUNT,
                ARG_TRAIN_METADATA, ARG_FORECAST_QUANTILES
            ],
            HTSPipelineConstants.STEP_INFERENCE: [
                ARG_OUTPUT_METADATA, ARG_OUTPUT_PREDICT, ARG_SETUP_METADATA, ARG_ENABLE_EVENT_LOGGER,
                ARG_NODES_COUNT, ARG_NODE_PROCESS_COUNT
            ],
            ManyModelsPipelineConstants.STEP_INFERENCE: [
                ARG_OUTPUT_METADATA, ARG_OUTPUT_PREDICT, ARG_SETUP_METADATA, ARG_ENABLE_EVENT_LOGGER,
                ARG_NODES_COUNT, ARG_NODE_PROCESS_COUNT
            ],
            HTSPipelineConstants.STEP_COLLECT_INF: [
                ARG_INPUT_METADATA, ARG_INPUT_PREDICT, ARG_SETUP_METADATA, ARG_ENABLE_EVENT_LOGGER,
                ARG_OUTPUT_METADATA, ARG_OUTPUT_EVALUATION_CONFIGS, ARG_OUTPUT_EVALUTAION_DATA
            ],
            ManyModelsPipelineConstants.STEP_COLLECT_INF: [
                ARG_INPUT_METADATA, ARG_INPUT_PREDICT, ARG_SETUP_METADATA, ARG_ENABLE_EVENT_LOGGER,
                ARG_OUTPUT_METADATA, ARG_OUTPUT_EVALUATION_CONFIGS, ARG_OUTPUT_EVALUTAION_DATA
            ]
        }
    )

    OUTPUT_ARGUMENTS_DICT = {
        ARG_RAW_DATA: "raw_data",
        ARG_PROCESSED_DATA: "processed_data",
        ARG_ENABLE_EVENT_LOGGER: "enable_event_logger",
        ARG_INPUT_CONFIG: "input_config",
        ARG_INPUT_METADATA: "input_metadata",
        ARG_OUTPUT_METADATA: "output_metadata",
        ARG_OUTPUT_AGG_DATA: "output_agg_data",
        ARG_NODES_COUNT: "nodes_count",
        ARG_ENGINEERED_EXPLANATION: "engineered_explanation",
        ARG_SETUP_METADATA: "setup_metadata",
        ARG_TRAIN_RUN_ID: "train_run_id",
        ARG_FORECAST_LEVEL: "forecast_level",
        ARG_INFERENCE_TYPE: "inference_type",
        ARG_FORECAST_MODE: "forecast_mode",
        ARG_FORECAST_STEP: "forecast_step",
        ARG_FORECAST_QUANTILES: "forecast_quantiles",
        ARG_OUTPUT_PREDICT: "output_prediction",
        ARG_INPUT_PREDICT: "input_prediction",
        ARG_EXPERIMENT_NAME: "train_experiment_name",
        ARG_PARTITION_COLUMN_NAMES: "partition_column_names",
        ARG_ALLOCATION_METHOD: "allocation_method",
        ARG_PRS_STEP_TIMEOUT: "prs_step_timeout",
        ARG_NODE_PROCESS_COUNT: "node_process_count",
        ARG_RETRAIN_FAILED_MODEL: "retrain_failed_model",
        ARG_DATA_AGG_METADATA: "data_agg_metadata",
        ARG_ALLOW_MULIT_PARTITIONS: "allow_multi_partitions",
        ARG_SKIP_CONCAT_RESULTS: "skip_concat_results",
        ARG_TRAIN_METADATA: "optional_train_metadata",
        ARG_VALIDATION_FAIL_EARLY: "fail_early",
        ARG_OUTPUT_EVALUATION_CONFIGS: "output_evaluation_configs",
        ARG_OUTPUT_EVALUTAION_DATA: "output_evaluation_data",
        ARG_TARGET_COLUMN_NAME: "target_column_name",
        ARG_INTERNAL_SKIP_DATA_ACCESS: "internal_skip_data_access"
    }

    LIST_ARGS = {ARG_PARTITION_COLUMN_NAMES, ARG_FORECAST_QUANTILES}

    PROPERTIES_RUN_TYPE = "run_type_v2"
    PROPERTIES_PIPELINE_TYPE = "pipeline_type_v2"
    PROPERTIES_STEP_NAME = "step_name_v2"
    PROPERTIES_RUN_SETTINGS = "settings_yml"
    PROPERTIES_VALUE_TRAINING = "training"
    PROPERTIES_VALUE_INFERENCE = "inference"
    PROPERTIES_DATA_TAGS = "data_tags_v2"
    PROPERTIES_INPUT_FILE = "input_file_v2"
    RUN_TYPE_HTS = "hts_v2"
    RUN_TYPE_MM = "many_models_v2"

    PREPROCESSED_DATA_INFO = "preprocessed_data_info.json"
    COLLECTED_DATA_INFO = "collected_data_info.json"
    PARTITION_COLUMN_NAMES = "partition_column_names"

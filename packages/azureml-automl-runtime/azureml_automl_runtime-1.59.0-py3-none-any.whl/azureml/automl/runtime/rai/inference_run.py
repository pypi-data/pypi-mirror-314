# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Script for computing AutoML data on remote compute."""

import json
import logging
import os
from typing import Any, Dict, List, Optional, Tuple, Union

import mlflow
import pandas as pd
from azureml.automl.core import serialization_utilities
from azureml.automl.core.constants import FeatureType
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared.exceptions import ConfigException
from azureml.automl.runtime.experiment_store import ExperimentStore
from azureml.automl.runtime.shared._parqueter import Parqueter
from azureml.core.run import Run
from azureml.train.automl.runtime._entrypoints.utils.common import init_cache_store
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)

# Constants
RANDOM_STATE = 777
NUM_SAMPLES = 5000
OUTPUTS_DIRECTORY = "outputs"
MLFLOW_MODEL_DIRECTORY = f"{OUTPUTS_DIRECTORY}/mlflow-model"
RAI_DIRECTORY = "rai"
FEATURIZATION_SUMMARY_FILENAME = "featurization_summary.json"

# Parquet file constants
PREDICTIONS_PARQUET = f"{RAI_DIRECTORY}/predictions.npy.parquet"
PREDICTIONS_TEST_PARQUET = f"{RAI_DIRECTORY}/predictions_test.npy.parquet"
PREDICTION_PROBABILITIES_PARQUET = f"{RAI_DIRECTORY}/prediction_probabilities.npy.parquet"
PREDICTION_TEST_PROBABILITIES_PARQUET = f"{RAI_DIRECTORY}/prediction_test_probabilities.npy.parquet"
TRAIN_DF_PARQUET = f"{RAI_DIRECTORY}/train.df.parquet"
TEST_DF_PARQUET = f"{RAI_DIRECTORY}/test.df.parquet"
METATADATA_JSON = f"{RAI_DIRECTORY}/metadata.json"


def generate_random_sample(
    dataset: pd.DataFrame,
    target_column: str,
    number_samples: int,
    is_classification: Optional[bool] = False,
) -> pd.DataFrame:
    """
    Pick random samples of data from dataset.
    :param dataset: Input dataset.
    :type X: pd.DataFrame
    :param target_column: The name of the column which may be used in case of
        stratified splitting.
    :type target_column: str
    :param number_samples: The number of intended samples in the sampled data
    :type number_samples: int
    :param is_classification: If this is a classification scenario and we
        should do a stratified split based on the column target_column.
    :type is_classification: bool
    :return: Sub-sample of input dataset
    :rtype: pd.DataFrame
    """
    if not isinstance(dataset, pd.DataFrame):
        raise ConfigException("Expecting a pandas dataframe for generating a dataset sample.")

    if not isinstance(target_column, str):
        raise ConfigException("Expecting a string for target_column.")

    if not isinstance(number_samples, int):
        raise ConfigException("Expecting an integer for number_samples.")

    if not isinstance(is_classification, bool):
        raise ConfigException("Expecting a boolean for is_classification.")

    if target_column not in dataset.columns.tolist():
        raise ConfigException("The column {0} is not present in dataset".format(target_column))

    if number_samples <= 0:
        raise ConfigException("The number_samples should be greater than zero.")

    n_samples = len(dataset)
    if n_samples <= number_samples:
        logger.info(
            f"Length of the dataset ({n_samples}) is less than the requested number of samples ({number_samples}), "
            f"returning original datsaset."
        )
        return dataset

    target = dataset[target_column].values
    try:
        stratified_split = target if is_classification else None
        (
            dataset_sampled,
            _,
        ) = train_test_split(
            dataset,
            train_size=number_samples,
            random_state=RANDOM_STATE,
            stratify=stratified_split,
        )
    except BaseException as ex:
        logging_utilities.log_traceback(ex, logger, is_critical=False)
        # in case stratification fails, fall back to non-stratify train/test split
        (
            dataset_sampled,
            _,
        ) = train_test_split(dataset, random_state=RANDOM_STATE, train_size=number_samples)

    return dataset_sampled


def _get_raw_data_from_exp_store(parent_run: Run) -> Tuple[Any, Any, Any, Any]:
    cache_store = init_cache_store(parent_run)
    expr_store = ExperimentStore(cache_store, read_only=True)
    expr_store.load()
    logger.info("Successfully loaded the experiment store object.")
    X_raw, y, X_raw_valid, y_valid = expr_store.data.materialized.get_raw()
    ExperimentStore.reset()
    return X_raw, y, X_raw_valid, y_valid


def automl_download_raw_data(parent_run_or_id: Union[str, Run]) -> Tuple[Any, Any, Any, Any]:
    parent_run = _hydrate_run_from_context(parent_run_or_id)

    X_raw, y, X_raw_valid, y_valid = _get_raw_data_from_exp_store(parent_run)

    if X_raw_valid is None:
        logger.info("No validation data is set, generating one.")
        target_column, task_type = get_automl_task_type_and_target_column_name(parent_run)
        train = X_raw.copy()
        train[target_column] = y

        test = generate_random_sample(
            train,
            target_column=target_column,
            number_samples=NUM_SAMPLES,
            is_classification=(task_type == "classification"),
        )

        X_raw_valid = test.drop(columns=[target_column])
        y_valid = test[target_column]
    elif len(X_raw_valid) > NUM_SAMPLES:
        logger.info("Validation set greater than NUM_SAMPLES")
        target_column, task_type = get_automl_task_type_and_target_column_name(parent_run)
        test = X_raw_valid.copy()
        test[target_column] = y_valid

        test_sampled = generate_random_sample(
            test,
            target_column=target_column,
            number_samples=NUM_SAMPLES,
            is_classification=(task_type == "classification"),
        )

        X_raw_valid = test_sampled.drop(columns=[target_column])
        y_valid = test_sampled[target_column]

    return X_raw, y, X_raw_valid, y_valid


def _hydrate_run_from_context(run_or_id: Union[str, Run]) -> Run:
    if isinstance(run_or_id, Run):
        return run_or_id
    # `run_or_id` is a run identifier
    curr_run = Run.get_context()
    if curr_run.id == run_or_id:
        return curr_run
    workspace_run = curr_run.experiment.workspace.get_run(run_or_id)
    return workspace_run


def get_automl_task_type_and_target_column_name(parent_run_or_id: Union[str, Run]) -> Tuple[str, str]:
    parent_run = _hydrate_run_from_context(parent_run_or_id)
    automl_settings = json.loads(parent_run.properties["AMLSettingsJsonString"])
    target_column = automl_settings["label_column_name"]
    task_type = automl_settings["task_type"]
    return target_column, task_type


def get_feature_summary_and_dropped_feature_types(
        child_run_or_id: Union[str, Run]) -> Tuple[Dict[str, Any], List[str]]:
    child_run = _hydrate_run_from_context(child_run_or_id)
    child_run.download_file(
        f"{OUTPUTS_DIRECTORY}/{FEATURIZATION_SUMMARY_FILENAME}",
        FEATURIZATION_SUMMARY_FILENAME,
    )

    f = open(FEATURIZATION_SUMMARY_FILENAME, "r")
    file_content = f.read()
    file_content = file_content.replace("NaN", "null")
    summaries = json.loads(file_content)
    f.close()

    feature_type_to_feature_name_dict: Dict[str, Any] = {}
    for feature in FeatureType.FULL_SET:
        feature_type_to_feature_name_dict[feature] = []

    for summary in summaries:
        feature_type_to_feature_name_dict[summary["TypeDetected"]].append(summary["RawFeatureName"])

    return feature_type_to_feature_name_dict, list(FeatureType.DROP_SET)


def get_inference_results(
    parent_run_or_id: Union[str, Run],
    child_run_or_id: Union[str, Run],
    X_raw: pd.DataFrame,
    X_raw_valid: pd.DataFrame,
) -> Tuple[Any, Any, Any, Any, Any]:
    child_run = _hydrate_run_from_context(child_run_or_id)
    parent_run = _hydrate_run_from_context(parent_run_or_id)

    child_run.download_files(MLFLOW_MODEL_DIRECTORY, ".")
    logger.info("Loading the MLFLow model locally...")
    model = mlflow.sklearn.load_model(f"./{MLFLOW_MODEL_DIRECTORY}")
    logger.info("Successfully loaded the model.")
    preds = model.predict(X_raw)
    preds_valid = model.predict(X_raw_valid)

    _, task_type = get_automl_task_type_and_target_column_name(parent_run)
    if task_type == "classification":
        preds_proba = model.predict_proba(X_raw)
        preds_valid_proba = model.predict_proba(X_raw_valid)
        if isinstance(preds_proba, (pd.DataFrame, pd.Series)):
            preds_proba = preds_proba.values
        if isinstance(preds_valid_proba, (pd.DataFrame, pd.Series)):
            preds_valid_proba = preds_valid_proba.values
    else:
        preds_proba = None
        preds_valid_proba = None

    # get model classes
    classes = None
    if hasattr(model, "classes_"):
        classes = serialization_utilities.serialize_json_safe(list(model.classes_))
    return preds, preds_valid, preds_proba, preds_valid_proba, classes


def upload_rai_artifacts_to_automl_child_run(parent_run_id: Union[str, Run], child_run_id: Union[str, Run]) -> None:
    try:
        parent_run = _hydrate_run_from_context(parent_run_id)
        child_run = _hydrate_run_from_context(child_run_id)

        logger.info("Downloading dataset locally...")
        X_raw, y, X_raw_valid, y_valid = automl_download_raw_data(parent_run)
        target_column, task_type = get_automl_task_type_and_target_column_name(parent_run)
        (
            feature_type_to_feature_name_dict,
            feature_types_dropped,
        ) = get_feature_summary_and_dropped_feature_types(child_run)

        logger.info("Getting inference results...")
        preds, preds_valid, preds_proba, preds_valid_proba, classes = get_inference_results(
            parent_run, child_run, X_raw, X_raw_valid
        )

        os.makedirs(RAI_DIRECTORY, exist_ok=True)

        Parqueter.dump(preds, PREDICTIONS_PARQUET)
        Parqueter.dump(preds_valid, PREDICTIONS_TEST_PARQUET)

        if task_type == "classification":
            Parqueter.dump(preds_proba, PREDICTION_PROBABILITIES_PARQUET)
            Parqueter.dump(preds_valid_proba, PREDICTION_TEST_PROBABILITIES_PARQUET)

        train = X_raw.copy()
        train[target_column] = y

        test = X_raw_valid.copy()
        test[target_column] = y_valid

        Parqueter.dump(train, TRAIN_DF_PARQUET)
        Parqueter.dump(test, TEST_DF_PARQUET)

        metadata = {
            "feature_type_summary": feature_type_to_feature_name_dict,
            "feature_type_dropped": feature_types_dropped,
            "target_column": target_column,
            "task_type": task_type,
            "classes": classes,
        }

        with open(METATADATA_JSON, "w") as fp:
            json.dump(metadata, fp)

        logger.info("Uploading RAI outputs on the child run...")
        child_run.upload_folder(f"{OUTPUTS_DIRECTORY}/{RAI_DIRECTORY}", RAI_DIRECTORY)
    except Exception as ex:
        logger.error("Failed to upload RAI outputs on the run.")
        logging_utilities.log_traceback(ex, logger)
        raise

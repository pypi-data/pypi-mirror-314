# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""The set of helper functions for data frames."""
from typing import Any, List, Optional, cast, Dict, Sequence

import gc

import numpy as np
import pandas as pd

from azureml.automl.core.automl_base_settings import AutoMLBaseSettings
from azureml.automl.core.shared import constants
from azureml.automl.core.shared._diagnostics.automl_error_definitions import TimeseriesDfWrongTypeOfValueColumn
from azureml.automl.core.shared.forecasting_exception import ForecastingDataException
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.runtime._data_definition.raw_experiment_data import RawExperimentData
from azureml.automl.runtime._ml_engine.validation import common_data_validations
from azureml.automl.runtime.column_purpose_detection._time_series_column_helper import convert_check_grain_value_types
from azureml.automl.runtime.faults_verifier import VerifierManager
from azureml.automl.runtime import short_grain_padding, _timeseries_id_detection_utilities,\
    _data_transformation_utilities
from azureml.automl.runtime.featurizer.transformer.timeseries._validation import (
    TimeseriesAutoParamValidationWorker,
    TimeseriesColumnNameValidationWorker,
    TimeseriesCVValidationWorker,
    TimeseriesDataFrameValidationWorker,
    TimeseriesFrequencyValidationWorker,
    TimeseriesInputValidationWorker,
    TimeseriesParametersValidationWorker,
    TimeseriesValidationParameter,
    TimeseriesValidationParamName,
    TimeseriesValidationWorkerBase,
    TimeseriesValidator,
)
from azureml._common._error_definition.azureml_error import AzureMLError
from azureml._restclient.models.featurization_config import FeaturizationConfig
from azureml.automl.runtime.featurizer.transformer.timeseries._validation._timeseries_validation_common \
    import check_memory_limit
from azureml.automl.runtime.frequency_fixer import fix_data_set_regularity_may_be
from azureml.automl.runtime.shared.types import DataInputType
from azureml.automl.runtime.shared.utilities import _get_num_unique
from azureml.automl.runtime.experiment_store import ExperimentStore
from azureml.automl.runtime.shared.score._metric_base import NonScalarMetric
from azureml.automl.core.shared.constants import TimeSeriesInternal
from azureml.automl.runtime.shared.score._regression import NormRMSE
from azureml.automl.runtime import _time_series_training_utilities
from azureml.automl.runtime.shared.model_wrappers import RegressionPipeline
import copy
import logging
_logger = logging.getLogger(__name__)


def validate_timeseries_training_data(
    automl_settings: AutoMLBaseSettings,
    X: DataInputType,
    y: DataInputType,
    X_valid: Optional[DataInputType] = None,
    y_valid: Optional[DataInputType] = None,
    sample_weight: Optional[np.ndarray] = None,
    sample_weight_valid: Optional[np.ndarray] = None,
    cv_splits_indices: Optional[List[List[Any]]] = None,
    x_raw_column_names: Optional[np.ndarray] = None,
) -> None:
    """
    Quick check of the timeseries input values, no tsdf is required here.

    :param automl_settings: automl settings
    :param X: Training data.
    :param y: target/label data.
    :param X_valid: Validation data.
    :param y_valid: Validation target/label data.
    :param sample_weight: Sample weights for the training set.
    :param sample_weight_valid: Sample weights for the validation set.
    :param cv_splits_indices: Indices for the cross validation.
    :param x_raw_column_names: The column names for the features in train and valid set.
    """
    ts_val_param = TimeseriesValidationParameter(
        automl_settings=automl_settings,
        X=X,
        y=y,
        X_valid=X_valid,
        y_valid=y_valid,
        sample_weight=sample_weight,
        sample_weight_valid=sample_weight_valid,
        cv_splits_indices=cv_splits_indices,
        x_raw_column_names=x_raw_column_names,
    )
    validation_workers = [
        TimeseriesParametersValidationWorker(),
        TimeseriesFrequencyValidationWorker(),
        TimeseriesColumnNameValidationWorker(),
        TimeseriesCVValidationWorker(),
        TimeseriesInputValidationWorker(
            x_param_name=TimeseriesValidationParamName.X, y_param_name=TimeseriesValidationParamName.Y
        ),
        TimeseriesInputValidationWorker(
            x_param_name=TimeseriesValidationParamName.X_VALID, y_param_name=TimeseriesValidationParamName.Y_VALID
        ),
        TimeseriesAutoParamValidationWorker(),
        TimeseriesDataFrameValidationWorker(),
    ]  # type: List[TimeseriesValidationWorkerBase]

    ts_validator = TimeseriesValidator(validation_workers=validation_workers)
    ts_validator.validate(param=ts_val_param)


def _add_freq_fixer_guard_rails(verifier: Optional[VerifierManager],
                                failed: bool, corrected: bool,
                                automl_settings: AutoMLBaseSettings) -> None:
    """
    Add the correct guard rail to the verifier.

    :param verifier: The verifier to be used to write guard rails to.
    :param failed: True if frequency fixer has failed.
    :param corrected: True if the dimensions of the data frame was corrected.
    :param automl_settings: The automl_settings used to run frequency fixer.
    :param effective_freq_str: The forecasting frequency used.
    """
    if verifier is None:
        return
    if automl_settings.target_aggregation_function is None or automl_settings.freq is None:
        verifier.update_data_verifier_frequency_inference(failed, corrected)
    elif not failed:
        # Aggregation does not fail, so in this case we ignore this value.
        verifier.update_data_verifier_aggregation(
            corrected,
            automl_settings.target_aggregation_function,
            automl_settings.freq)


def _is_df_unique_target_value(
        df: pd.DataFrame,
        target_column_name: str = constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN) -> bool:
    n_unique = _get_num_unique(df[target_column_name], ignore_na=True, ignore_inf=True)
    return n_unique == 1


def _check_uniqueness_and_perturb_maybe(raw_data_context: RawExperimentData,
                                        automl_settings_obj: AutoMLBaseSettings,
                                        validation_set: bool,
                                        verifier: Optional[VerifierManager] = None) -> pd.DataFrame:
    """
    Check for unique values. If only one unique value is present, add noise from a N(0, sigma) where
    sigma = mu*cv, mu is the unique value, and cv is the coefficient of variation.
    :param raw_data_context: The raw data context to be used as a data source.
    :param automl_settings_obj: The automl settngs.
    :param validation_set: Is this a validation set.
    :return: The data frame with corrected target.
    """
    X = _concat_features_and_target(raw_data_context, validation_set=validation_set)
    # check if target is non-numeric
    target_column_name = constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN
    if not all(isinstance(v, (int, float, np.number)) for v in X[target_column_name]):
        raise ForecastingDataException._with_error(
            AzureMLError.create(
                TimeseriesDfWrongTypeOfValueColumn,
                target='target_column',
                reference_code=ReferenceCodes._TSDF_NON_NUMERIC_TGT_COL)
        )

    is_all_grains_unique_target = _is_df_unique_target_value(X)
    if automl_settings_obj.grain_column_names is None:
        X = _check_uniqueness_and_perturb_maybe_one_grain(X)
    elif _is_all_grains_unique_target(
            X, automl_settings_obj.grain_column_names, constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN):
        # We will save the link to the X_valid, before we will perturb it.
        # We will only perturb if all grains has unique target value.
        is_all_grains_unique_target = True
        X_before_perturb = X
        X = X.groupby(automl_settings_obj.grain_column_names,
                      as_index=False, group_keys=False).apply(_check_uniqueness_and_perturb_maybe_one_grain)
        # We have implicitly copied X_valid above and now we have to drop the target from the link.
        X_before_perturb.drop(constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN, axis=1, inplace=True)

    if verifier is not None:
        verifier.update_data_verifier_for_unique_target_grains(
            is_all_grains_unique_target=is_all_grains_unique_target)
    return X


def _is_all_grains_unique_target(X: pd.DataFrame, grain_col_names: List[str], target_col: str) -> bool:
    """Check if all grains has unique target values."""
    return all(
        _get_num_unique(
            df[target_col], ignore_na=True, ignore_inf=True) == 1 for _, df in X.groupby(grain_col_names))


def _check_uniqueness_and_perturb_maybe_one_grain(
        X: pd.DataFrame,
        target_column_name: str = constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN
) -> pd.DataFrame:
    """
    Check for unique values. If only one unique value is present, add noise from a N(0, sigma) where
    sigma = mu*cv, mu is the unique value, and cv is the coefficient of variation.
    :param X: The data frame to be corrected.
    :return: The data frame with corrected target.
    """
    if _is_df_unique_target_value(X, target_column_name):
        series = X[target_column_name].values
        mean = series[np.isfinite(series)].mean()
        cv = constants.TimeSeriesInternal.PERTURBATION_NOISE_CV
        sd = abs(mean) * cv if mean != 0 else cv
        X[target_column_name] = X[target_column_name] + np.random.normal(loc=0, scale=sd, size=len(X))
    return X


def _concat_features_and_target(raw_experiment_data: RawExperimentData,
                                validation_set: bool = False) -> pd.DataFrame:
    df = cast(pd.DataFrame, raw_experiment_data.X_valid if validation_set else raw_experiment_data.X)
    target = raw_experiment_data.y_valid if validation_set else raw_experiment_data.y
    if isinstance(df, np.ndarray) and raw_experiment_data.feature_column_names is not None:
        df = pd.DataFrame(df, columns=raw_experiment_data.feature_column_names)
    df[constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN] = cast(np.ndarray, target)
    return df


def validate_timeseries_data_for_auto_time_series_id_detection(x_raw_column_names: Optional[np.ndarray],
                                                               time_column_name: str,
                                                               time_series_id_column_names: List[str] = []) -> bool:

    if (time_column_name is None or x_raw_column_names is None):
        return False
    # time_column_name can be set for an index and it throws an keyError while checking duplicates.
    elif time_column_name not in x_raw_column_names:
        return False
    elif time_series_id_column_names is not None:
        if not (time_column_name not in time_series_id_column_names
                and all(item in x_raw_column_names for item in time_series_id_column_names)):
            return False
    return True


def _check_insufficient_data_for_tcn(
        verifier: VerifierManager,
        number_of_data_points: int,
        number_of_data_points_after_preprocessing: int,
        automl_settings: AutoMLBaseSettings) -> None:
    is_multi_grain = automl_settings.grain_column_names is not None
    verifier.update_data_verifier_insufficient_data_forecast_tcn(
        number_of_data_points, number_of_data_points_after_preprocessing, is_multi_grain, automl_settings.enable_dnn)


def preprocess_timeseries_data(
        raw_experiment_data: RawExperimentData,
        automl_settings_obj: AutoMLBaseSettings,
        is_remote: bool,
        verifier: Optional[VerifierManager] = None) -> RawExperimentData:
    """
    Preprocess timeseries data and apply rule based validation.

    :param raw_experiment_data: The data to be analyzed and preprocessed.
    :param automl_settings_obj: The AutoML settings.
    :param is_remote: True if it is a remote run.
    :param verifier: The VerifierManager object used to output the guard rails.
    :return: The same RawExperimentData with modified data.
    """
    # We should not check dimensions on remote and non
    # forecasting runs because of streaming scenario.
    if not is_remote or automl_settings_obj.is_timeseries:
        common_data_validations.check_dimensions(
            X=raw_experiment_data.X,
            y=raw_experiment_data.y,
            X_valid=raw_experiment_data.X_valid,
            y_valid=raw_experiment_data.y_valid,
            sample_weight=raw_experiment_data.weights,
            sample_weight_valid=raw_experiment_data.weights_valid
        )
    if automl_settings_obj.is_timeseries:
        # Reconstruct the pandas data frames if possible.
        if not isinstance(raw_experiment_data.X, pd.DataFrame) and \
                raw_experiment_data.feature_column_names is not None:
            raw_experiment_data.X = pd.DataFrame(
                raw_experiment_data.X, columns=raw_experiment_data.feature_column_names
            )
        if raw_experiment_data.X_valid is not None and not isinstance(raw_experiment_data.X_valid, pd.DataFrame) \
                and raw_experiment_data.feature_column_names is not None:
            raw_experiment_data.X_valid = pd.DataFrame(
                raw_experiment_data.X_valid, columns=raw_experiment_data.feature_column_names
            )

        # Validate before triggering auto time series id detection feature.
        is_valid = validate_timeseries_data_for_auto_time_series_id_detection(
            raw_experiment_data.feature_column_names,
            automl_settings_obj.time_column_name,
            cast(List[str], automl_settings_obj.grain_column_names)
        )

        if is_valid:
            # Detect time series id column names if needed.
            _timeseries_id_detection_utilities.detect_time_series_id_if_exists(raw_experiment_data.X,
                                                                               automl_settings_obj,
                                                                               verifier)

        # Check that each grain column contains exactly one data type.
        raw_experiment_data.X, raw_experiment_data.X_valid = convert_check_grain_value_types(
            raw_experiment_data.X, raw_experiment_data.X_valid, automl_settings_obj.grain_column_names,
            automl_settings_obj.featurization,
            ReferenceCodes._TS_VALIDATION_GRAIN_TYPE_REMOTE if
            is_remote else ReferenceCodes._TS_VALIDATION_GRAIN_TYPE_LOCAL)

        # The time series data may undergo aggregation, which will change the column
        # names. We need to save the data snapshot before it will happen.
        raw_experiment_data.data_snapshot_str = _data_transformation_utilities.get_data_snapshot(
            raw_experiment_data.X)
        raw_experiment_data.data_snapshot_str_with_quantiles = \
            _data_transformation_utilities._get_data_snapshot_with_quantiles(
                raw_experiment_data.X, is_forecasting=True, is_raw=True)
        output_index_columns = []
        if automl_settings_obj.grain_column_names is not None:
            output_index_columns = [
                c for c in automl_settings_obj.grain_column_names if c in raw_experiment_data.X.columns]
        output_index_columns.append(automl_settings_obj.time_column_name)
        raw_experiment_data.output_data_snapshot_str_with_quantiles = \
            _data_transformation_utilities._get_data_snapshot_with_quantiles(
                raw_experiment_data.X, is_forecasting=True, is_raw=False, include_cols=output_index_columns)

        # Check for uniqueness and add noise here.
        if is_valid:
            X = _check_uniqueness_and_perturb_maybe(raw_experiment_data, automl_settings_obj, False, verifier)
            # Update object with corrected data
            raw_experiment_data.y = X.pop(constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN).values.copy()
            raw_experiment_data.X = X
        else:
            # When user provides grain column names that do not exist, we pass the data as is and
            # user error will be raised at the data validation stage.
            X = _concat_features_and_target(raw_experiment_data, False)

        number_of_data_points = raw_experiment_data.X.shape[0]
        # When data were read try to fix the frequency.
        if raw_experiment_data.X_valid is None:
            # This check is for the scenario when user provided grain column names that do not exist.
            # We pass the data as is and user error will be raised at the data validation stage.
            fixed_freq_obj = fix_data_set_regularity_may_be(
                X,
                raw_experiment_data.y,
                automl_settings_obj,
                ReferenceCodes._REMOTE_SCRIPT_WRONG_FREQ
                if is_remote else ReferenceCodes._TRAINING_UTILITIES_CHECK_FREQ_FIX)
            X = fixed_freq_obj.data_x
            raw_experiment_data.y = cast(np.ndarray, fixed_freq_obj.data_y)
            failed = fixed_freq_obj.is_failed
            corrected = fixed_freq_obj.is_modified
            freq = fixed_freq_obj.freq
            # Do our best to clean up memory.
            raw_experiment_data.X = None
            gc.collect()
            # If we do not have enough memory, raise the exception.
            check_memory_limit(X, raw_experiment_data.y)
            # Pad the short grains if needed (the short_series_handing_config_value is
            # checked by pad_short_grains_or_raise).
            X, raw_experiment_data.y = short_grain_padding.pad_short_grains_or_raise(
                X, raw_experiment_data.y, freq, automl_settings_obj,
                ReferenceCodes._TS_ONE_VALUE_PER_GRAIN_RSCRIPT if
                is_remote else ReferenceCodes._TS_ONE_VALUE_PER_GRAIN_TSUTIL,
                verifier)
            # We may have reordered data frame X remember the new column order.
            raw_experiment_data.feature_column_names = X.columns.values
            # and then copy the data to new location.
            raw_experiment_data.X = X
            if verifier:
                _add_freq_fixer_guard_rails(
                    verifier, failed, corrected,
                    automl_settings_obj)
        else:
            # Check for uniqueness and add noise here.
            if is_valid:
                X_valid = _check_uniqueness_and_perturb_maybe(raw_experiment_data, automl_settings_obj, True)
                # Update object with corrected data
                raw_experiment_data.y_valid = X_valid.pop(constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN).values
                raw_experiment_data.X_valid = X_valid

        # Check whether sufficient data points are available for ForecastTCN to be suggested
        if verifier and is_remote:
            number_of_data_points_after_preprocessing = raw_experiment_data.X.shape[0]
            _check_insufficient_data_for_tcn(
                verifier,
                number_of_data_points,
                number_of_data_points_after_preprocessing,
                automl_settings_obj)

    return raw_experiment_data


def _compute_forecast_adjustment(
        forecast_CV_data: Dict[str, Any],
        fitted_pipeline: RegressionPipeline,
        target_column_name: str,
        predicted_column_name: str,
        time_column_name: str) -> Dict[str, List[Any]]:
    """
    Identify the grains that should be adjusted and the corresponding adjustment

    :param forecast_CV_data: Stores the metrics from the latest CV fold
    :param fitted_pipeline: Will be used for generating the insample fit of the data
    :param target_column_name: str,
    :param predicted_column_name: str,
    :param time_column_name: str
    :return: A dictionary containing the grains with their corresponding adjustment. Default value is 0 adjustment.
    """

    if NonScalarMetric.DATA in forecast_CV_data:
        forecast_CV_data = forecast_CV_data[NonScalarMetric.DATA]
    if TimeSeriesInternal.GAP_CV_METRIC in forecast_CV_data:
        gap_cv_metrics = forecast_CV_data[TimeSeriesInternal.GAP_CV_METRIC]
        X_train = pd.DataFrame()
        insample_df_test = pd.DataFrame()
        expr_store = ExperimentStore.get_instance()
        if TimeSeriesInternal.GRAIN_COL_NAME in gap_cv_metrics:
            for idx, split in enumerate(expr_store.data.materialized.get_CV_splits()):
                if idx == forecast_CV_data[TimeSeriesInternal.LAST_CV_NUM]:
                    X_train = split._X_train_transformed
                    y_train = split._y_train
                    X_train.reset_index(inplace=True)
                    X_train[target_column_name] = y_train

                    X_test = split._X_test_transformed
                    X_test = X_test.reset_index()

                    insample_df_test = pd.DataFrame(X_test[gap_cv_metrics[TimeSeriesInternal.GRAIN_COL_NAME]])
                    insample_df_test[time_column_name] = X_test[time_column_name]
                    insample_df_test[target_column_name] = split._y_test
                    # data is already transformed so we don't need to transform it again
                    fitted_pipeline_trimmed = copy.deepcopy(fitted_pipeline)
                    if len(fitted_pipeline.steps) > 0 and fitted_pipeline.steps[0][0] == 'timeseriestransformer':
                        fitted_pipeline_trimmed.steps = fitted_pipeline.steps[1:]
                    insample_df_test[predicted_column_name] = fitted_pipeline_trimmed.predict(
                        split._X_test_transformed)
                    insample_df_test[TimeSeriesInternal.GAP] = insample_df_test[predicted_column_name] \
                        - insample_df_test[target_column_name]
            return _calculate_adjustment_grain_level(X_train, insample_df_test,
                                                     gap_cv_metrics[TimeSeriesInternal.GRAIN_DATA],
                                                     gap_cv_metrics[TimeSeriesInternal.GRAIN_COL_NAME],
                                                     target_column_name, predicted_column_name)
    return dict()


def _calculate_adjustment_grain_level(
        X_train: pd.DataFrame,
        insample_df_test: pd.DataFrame,
        grain_list: list,
        grain_column_names: list,
        target_column_name: str,
        predicted_column_name: str) -> Dict[str, List[Any]]:
    """
    Identify the grains that needs to be adjusted and the corresponding adjustment based on the rule. Store the
    adjustment in a dictionary.

    :param X_train: Training data for insample nrmse calculation
    :param insample_df_test: Training data for insample nrmse calculation
    :param grain_list: List of grains
    :param grain_column_names: List of grain column names
    :param target_column_name: The name of the target column,
    :param predicted_column_name: The name of the column containing the predicted values,
    :return: Dictionary with adjustment levels per grain.
    """

    adjustment_dict = {TimeSeriesInternal.GRAIN_NAME: grain_column_names,
                       TimeSeriesInternal.GRAIN_VALUE_LIST: [],
                       TimeSeriesInternal.ADJUSTMENT: []}
    # if train and insample data is presnet then calculate the adjustment
    if X_train.empty or insample_df_test.empty:
        return adjustment_dict
    # Converting the grains to str so it will match the grains in adjustment list of string dtypes
    insample_df_test[grain_column_names] = insample_df_test[grain_column_names].astype(str)
    X_train[grain_column_names] = X_train[grain_column_names].astype(str)

    groupby_test = insample_df_test.groupby(grain_column_names)  # Insample test data
    groupby_train = X_train.groupby(grain_column_names)  # Insample train data

    # Loop to iterate over individual grains and calculate the required adjustment
    error_grains = []

    for grain in grain_list:
        adjustment = 0.0
        try:
            grain_val = grain[TimeSeriesInternal.GRAIN_VALUE]
            df_one_insample_test = groupby_test.get_group(tuple(grain_val) if len(grain_val) > 1 else grain_val[0])
            insample_nrmse = _compute_insample_nrmse_adj(grain, groupby_train,
                                                         df_one_insample_test,
                                                         target_column_name,
                                                         predicted_column_name)
            adjustment = _get_adjustment(grain, insample_nrmse, df_one_insample_test)
        except Exception:
            error_grains.append(grain)
        adjustment_dict[TimeSeriesInternal.GRAIN_VALUE_LIST].append(grain[TimeSeriesInternal.GRAIN_VALUE])
        adjustment_dict[TimeSeriesInternal.ADJUSTMENT].append(adjustment)

    _logger.info("Adjusted grains/Total grains/Error grains={0}/{1}/{2}".
                 format(np.count_nonzero(adjustment_dict['adjustment']),
                        len(adjustment_dict['adjustment']),
                        len(error_grains)))
    return adjustment_dict


def _get_adjustment(
        grain: dict,
        insample_nrmse: float,
        df_one_insample_test: pd.DataFrame) -> float:
    """
    If Insample NRMSE and Last CV NRMSE is higher than the defined thresholds
    then we return the adjustment value else default is zero
    :param grain: It is a dictionary containing the grain properties
    :param insample_nrmse: NRMSE of the insample fit
    :param df_one_insample_test: Dataframe of insample fit of test data
    :return: float adjustment value
    """
    if TimeSeriesInternal.GAP_CV_BIAS in grain and TimeSeriesInternal.GAP_CV_NRMSE in grain:
        # If cv_nrmse, insample_nrmse and cv_bias_percent are there,then adjust
        if grain[TimeSeriesInternal.GAP_CV_BIAS] >= TimeSeriesInternal.GAP_CV_BIAS_CUTOFF and \
                (insample_nrmse >= TimeSeriesInternal.GAP_INSAMPLE_NRMSE_CUTOFF
                 or grain[TimeSeriesInternal.GAP_CV_NRMSE] >= TimeSeriesInternal.GAP_CV_NRMSE_CUTOFF):
            return float(round(df_one_insample_test[TimeSeriesInternal.GAP].mean(), 5))
    return float(0)


def _compute_insample_nrmse_adj(
        grain: dict,
        groupby_train: pd.core.groupby.DataFrameGroupBy,
        df_one_insample_test: pd.DataFrame,
        target_column_name: str,
        predicted_column_name: str) -> float:
    """
    Calculate NRMSE
    :param grain: It is a dictionary containing the grain properties
    :param groupby_train: Train dataframe to be used for insample NRMSE calculation
    :param df_one_insample_test: Dataframe of insample fit of test data
    :param target_column_name:  The column name we want to predict in train data
    :param predicted_column_name: The column name with the predicted value
    :return: float Insample NRMSE
    """
    grain_val = grain[TimeSeriesInternal.GRAIN_VALUE]
    train_min, train_max = list(groupby_train.get_group(tuple(grain_val) if len(grain_val) > 1 else grain_val[0])
                                [target_column_name].agg([constants.AggregationFunctions.MIN,
                                                          constants.AggregationFunctions.MAX]))
    return float(round(NormRMSE(
                       df_one_insample_test[target_column_name],
                       df_one_insample_test[predicted_column_name],
                       train_max,
                       train_min).compute(), 5))


def _get_metadata_dict(model_name: str, is_distributed: bool, run_id: str) -> Dict[str, Any]:
    """
    Generate metadata dictionary to log forecasting run.

    :param model_name: The name of a model i.e. TCNForecaster.
    :param is_distributed: If true, the run is distributed.
    :param run_id: The run ID.
    :return: The dictionary to be logged.
    """
    return {
        constants.MLFlowMetaLiterals.BASE_MODEL_NAME: model_name,
        constants.MLFlowMetaLiterals.FINETUNING_TASK: constants.Subtasks.FORECASTING,
        constants.MLFlowMetaLiterals.IS_AUTOML_MODEL: True,
        constants.MLFlowMetaLiterals.IS_DISTRIBUTED: is_distributed,
        constants.MLFlowMetaLiterals.TRAINING_RUN_ID: run_id
    }

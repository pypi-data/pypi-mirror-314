# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Holding the featurization functions."""
import json
import logging
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import azureml.automl.runtime._ml_engine as ml_engine
import numpy as np
import pandas as pd

from azureml._common._error_definition import AzureMLError
from azureml._tracing._tracer_factory import get_tracer
from azureml.automl.core._experiment_observer import (ExperimentObserver,
                                                      NullExperimentObserver)
from azureml.automl.core.constants import PredictionTransformTypes
from azureml.automl.core.featurization import FeaturizationConfig
from azureml.automl.core.shared import constants, logging_utilities, utilities
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    AutoMLInternal, InvalidValuesInData)
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared._diagnostics.validation import Validation
from azureml.automl.core.shared.constants import (AutoMLDefaultTimeouts,
                                                  TimeSeries)
from azureml.automl.core.shared.exceptions import (ClientException,
                                                   DataException,
                                                   ValidationException)
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.shared.types import GrainType
from azureml.automl.runtime._data_transformation_utilities import _log_data_info
from azureml.automl.runtime._time_series_data_set import TimeSeriesDataSet
from azureml.automl.runtime.column_purpose_detection import StatsAndColumnPurposeType
from azureml.automl.runtime.column_purpose_detection._time_series_column_helper import get_drop_columns
from azureml.automl.runtime.featurization import data_transformer_utils
from azureml.automl.runtime.featurizer.transformer.featurization_utilities import (
    get_prediction_transform_type,
    skip_featurization)
from azureml.automl.runtime.featurizer.transformer.timeseries import timeseries_transformer
from azureml.automl.runtime.shared import utilities as runtime_utilities
from azureml.automl.runtime.shared.cache_store import CacheStore
from azureml.automl.runtime.shared.stationarity_check_utils import unit_root_test_wrapper
from azureml.automl.runtime.shared.types import (DataInputType,
                                                 DataSingleColumnInputType)
from azureml.dataprep import Dataflow
from azureml.training.tabular.models.differencing_y_transformer import DifferencingYTransformer
from azureml.training.tabular.models.target_type_transformer import TargetTypeTransformer
from azureml.training.tabular.models.y_pipeline_transformer import YPipelineTransformer
from scipy import sparse
from sklearn import preprocessing
from sklearn.pipeline import Pipeline
from sklearn.utils.class_weight import compute_class_weight

from . import _data_transformation_utilities
from ._feature_sweeped_state_container import FeatureSweepedStateContainer
from .data_context import RawDataContext, TransformedDataContext
from .faults_verifier import VerifierManager, VerifierResults
from .featurization import DataTransformer
from .featurization._featurizer_container import FeaturizerContainer

_logger = logging.getLogger(__name__)
tracer = get_tracer(__name__)


# TODO: Remove defaults.
def _suggest_featurizers_and_create_datatransformer(
        task: str,
        X: pd.DataFrame,
        y: Optional[DataSingleColumnInputType] = None,
        featurization_config: Optional[FeaturizationConfig] = None,
        is_onnx_compatible: bool = False,
        observer: ExperimentObserver = NullExperimentObserver(),
        enable_feature_sweeping: bool = True,
        feature_sweeping_timeout_seconds: int = AutoMLDefaultTimeouts.DEFAULT_FEATSWEEP_TIMEOUT_SECONDS,
        is_cross_validation: bool = True,
        enable_dnn: bool = False,
        force_text_dnn: bool = False,
        feature_sweeping_config: Dict[str, Any] = {},
        working_dir: Optional[str] = None,
        _test_transforms: Optional[List[Any]] = None,
        _feature_sweeper: Optional[Any] = None,
        enable_categorical_indicators: bool = False,
        for_distributed_featurization: bool = False) -> DataTransformer:
    """
    Identify the transformations for all the columns in the dataframe.

    :param task: Experiment task.
    :param X: Input training data.
    :param y: Optional label data.
    :param featurization_config: Featurization configuration if provided by the user.
    :param is_onnx_compatible: If the model needs to be ONNX compatible.
    :param observer: Experiment observer.
    :param enable_feature_sweeping: If feature sweeping is enabled.
    :param feature_sweeping_timeout_seconds: Specific timeout for feature sweeping in case it is enabled.
    :param is_cross_validation: If the current experiment is cross validation based.
    :param enable_dnn: If DNN is enabled.
    :param force_text_dnn: If DNN should be forced.
    :param feature_sweeping_config: Feature sweeping configuration.
    :param working_dir: Working directory
    :param _test_transforms: (Internal only)Any test transforms that need to be added.
    :param _feature_sweeper: (Internal only)Custom feature sweeper for testing.
    :param enable_categorical_indicators: If enable_categorical_indicators needs to be enabled.
    :param for_distributed_featurization: True if the featurizer needs to be distributed.
    :return: A DataTransformer
    """
    with tracer.start_as_current_span(
            constants.TelemetryConstants.SPAN_FORMATTING.format(
                constants.TelemetryConstants.COMPONENT_NAME, constants.TelemetryConstants.FEATURIZATION_STRATEGY
            ),
            user_facing_name=constants.TelemetryConstants.FEATURIZATION_STRATEGY_USER_FACING
    ):
        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X)
        (
            raw_feature_names,
            pre_processing_stats,
            stats_and_column_purposes,
            engg_featname_gen_holder,
            transformer_and_mapper_list,
        ) = ml_engine.suggest_featurizers(
            task=task,
            X=X,
            y=y,
            featurization_config=featurization_config,
            is_onnx_compatible=is_onnx_compatible,
            observer=observer,
            enable_feature_sweeping=enable_feature_sweeping,
            feature_sweeping_timeout_seconds=feature_sweeping_timeout_seconds,
            is_cross_validation=is_cross_validation,
            enable_dnn=enable_dnn,
            force_text_dnn=force_text_dnn,
            feature_sweeping_config=feature_sweeping_config,
            working_dir=working_dir,
            _test_transforms=_test_transforms,
            _feature_sweeper=_feature_sweeper,
            enable_categorical_indicators=enable_categorical_indicators,
            for_distributed_featurization=for_distributed_featurization
        )

        dt = DataTransformer(task=task,
                             is_onnx_compatible=is_onnx_compatible,
                             enable_feature_sweeping=enable_feature_sweeping,
                             enable_dnn=enable_dnn,
                             force_text_dnn=force_text_dnn,
                             observer=observer,
                             featurization_config=featurization_config,
                             is_cross_validation=is_cross_validation,
                             feature_sweeping_config=feature_sweeping_config,
                             working_dir=working_dir,
                             enable_categorical_indicators=enable_categorical_indicators
                             )

        dt._columns_types_mapping = data_transformer_utils.get_pandas_columns_types_mapping(X)
        dt._raw_feature_names = raw_feature_names
        dt._pre_processing_stats = pre_processing_stats
        dt.stats_and_column_purposes = stats_and_column_purposes
        dt._engineered_feature_names_class = engg_featname_gen_holder
        dt.transformer_and_mapper_list = transformer_and_mapper_list
        dt._is_text_dnn = any(dt._set_is_text_dnn_if_available(t) for t in transformer_and_mapper_list)
        dt._feature_sweeped = enable_feature_sweeping
        return dt


def build_feature_sweeped_state_container(
        raw_data_context: RawDataContext,
        cache_store: CacheStore,
        is_onnx_compatible: bool,
        experiment_observer: ExperimentObserver,
        enable_feature_sweeping: bool,
        feature_sweeping_config: Dict[str, Any],
        enable_dnn: bool,
        force_text_dnn: bool,
        featurizer_container: FeaturizerContainer,
        enable_categorical_indicators: bool = False
) -> FeatureSweepedStateContainer:
    """
    Builds a feature sweeped state container.

    :param raw_data_context: The raw input data.
    :param cache_store: The object that should be used to cache featurized data.
    :param is_onnx_compatible: If works in onnx compatible mode.
    :param experiment_observer: The experiment observer.
    :param enable_feature_sweeping: Enable or disable feature sweeping.
    :param feature_sweeping_config: Config used for feature sweeping.
    :param enable_dnn: Flag to enable neural networks for forecasting and natural language processing.
    :param force_text_dnn: Flag to force add neural networks for natural language processing in feature sweeping.
    :param featurizer_container: The featurizer container.
    :return: The feature sweeped state container to use for featurization.
    """
    transformed_data_context, y_transformer, X, y = create_transformed_data_context_no_streaming(
        raw_data_context,
        cache_store,
        enable_dnn=enable_dnn)
    transformed_data_context.X = _data_transformation_utilities._add_raw_column_names_to_X(
        transformed_data_context.X,
        raw_data_context.x_raw_column_names)

    featurization_config = raw_data_context.featurization if isinstance(raw_data_context.featurization,
                                                                        FeaturizationConfig) else None
    data_transformer = DataTransformer(
        task=raw_data_context.task_type,
        is_onnx_compatible=is_onnx_compatible,
        enable_feature_sweeping=enable_feature_sweeping,
        enable_dnn=enable_dnn,
        force_text_dnn=force_text_dnn,
        observer=experiment_observer,
        featurization_config=featurization_config,
        is_cross_validation=transformed_data_context._is_cross_validation_scenario(),
        feature_sweeping_config=feature_sweeping_config,
        enable_categorical_indicators=enable_categorical_indicators
    )
    # This is a separate featurization run, so we need to restore the data_transformer.
    _data_transformation_utilities.load_and_update_from_sweeping(data_transformer, transformed_data_context.X)
    data_transformer.set_cached_featurizers(
        _data_transformation_utilities.pull_fitted_featurizers_from_cache(cache_store, featurizer_container))

    data_transformer._featurizer_container = featurizer_container

    return FeatureSweepedStateContainer(
        data_transformer, transformed_data_context, y_transformer, X, y)


def create_transformed_data_context_no_streaming(raw_data_context: RawDataContext,
                                                 cache_store: CacheStore,
                                                 verifier: Optional[VerifierManager] = None,
                                                 enable_dnn: bool = False) \
        -> Tuple[TransformedDataContext, Optional[preprocessing.LabelEncoder], DataInputType, np.ndarray]:
    """
    Helper function for transforming input raw data from JOS to a transformed data context for further processing.
    We have already checked to ensure that streaming is not turned on.

    :param raw_data_context: The raw input data.
    :param cache_store: The object that should be used to cache featurized data.
    :param verifier: The verifier to check input data quality.
    :param enable_dnn: If DNN is enabled.
    :return: Transformed data context.
    """
    _logger.info("Pre-processing user data")
    _logger.info("The size of the raw data is: " + str(raw_data_context._get_memory_size()))
    X = raw_data_context.X
    y = raw_data_context.y
    sample_weight = raw_data_context.sample_weight
    X_valid = raw_data_context.X_valid
    y_valid = raw_data_context.y_valid
    sample_weight_valid = raw_data_context.sample_weight_valid

    # if featurization is turned off (which means AutoML is not handling missing value)
    # and data is sparse (data contains 50 percent or more NaNs),
    # we need to convert it to sparse.spmatrix so that Miro can suggest pipelines that are sparse-compatible.
    if skip_featurization(raw_data_context.featurization, raw_data_context.timeseries):
        count_nans = _data_transformation_utilities.count_nans_in_data(X)
        if count_nans > 0:
            if _data_transformation_utilities.should_convert_data_to_sparse(X, count_nans):
                _logger.info("Data detected as sparse with more than 50 percent NaNs, "
                             "but featurization is turned off and is omitting imputation. "
                             "Converting the data into sparse matrix.")
                X = _data_transformation_utilities.convert_data_to_sparse(X)
                X_valid = _data_transformation_utilities.convert_data_to_sparse(X_valid)
            else:
                _logger.info("Data contains NaN but is detected as dense since it contains less than 50 percent NaNs. "
                             "Featurization is turned off and is omitting imputation. "
                             "If NaNs are not expected, consider turning on featurization or cleaning up data.")
            if verifier is not None:
                verifier.update_data_verifier_for_missing_values(verifier_result=VerifierResults.ALERTED)

    prediction_transform_type = get_prediction_transform_type(raw_data_context.featurization)

    does_contain_exog_cols = True   # type bool
    freq = None  # type Optional[pd.DateOffset]
    grain_column_names = []
    time_column_name = None   # type Optional[str]
    if raw_data_context.timeseries:    # Only for forecasting task.
        Contract.assert_value(raw_data_context.timeseries_param_dict,
                              "raw_data_context.timeseries_param_dict",
                              reference_code=ReferenceCodes._DATA_TRANSFORMATION_INVALID_PARAM_DICT)

        freq = raw_data_context.timeseries_param_dict.get(TimeSeries.FREQUENCY)

        if raw_data_context.timeseries_param_dict.get(constants.TimeSeries.GRAIN_COLUMN_NAMES):
            grain_column_names = raw_data_context.timeseries_param_dict.get(constants.TimeSeries.GRAIN_COLUMN_NAMES)

        time_column_name = raw_data_context.timeseries_param_dict.get(constants.TimeSeries.TIME_COLUMN_NAME)
        Contract.assert_value(time_column_name,
                              "time_column_name",
                              reference_code=ReferenceCodes._DATA_TRANSFORMATION_INVALID_TIME_COL_NAME)

        raw_columns = get_raw_columns(
            X,
            raw_data_context.timeseries_param_dict,
            raw_data_context.featurization
        )
        # Check if data has any exogenous columns.
        does_contain_exog_cols = does_data_have_exogenous_cols(raw_columns, grain_column_names, time_column_name)

    y_transformer, y, y_valid = _y_transform(y, y_valid, raw_data_context.task_type,
                                             prediction_transform_type,
                                             raw_data_context.timeseries,
                                             raw_data_context.featurization,
                                             grain_column_names,
                                             time_column_name,
                                             freq,
                                             does_contain_exog_cols,
                                             X, X_valid,
                                             enable_dnn)

    # Here, if there is any exogenous column/s, we disable stationary featurizer fault verifier
    # independent of the data is stationary or not.
    if raw_data_context.timeseries and verifier is not None and not does_contain_exog_cols:
        if isinstance(y_transformer, YPipelineTransformer) and \
                DifferencingYTransformer.get_differencing_y_transformer(y_transformer):
            verifier.update_data_verifier_data_non_stationary(True)
        else:
            verifier.update_data_verifier_data_non_stationary(False)

    enable_class_balancing = False
    class_balancing_fixed = False
    if raw_data_context.task_type == constants.Tasks.CLASSIFICATION and raw_data_context.sample_weight is None and\
       verifier is not None:
        enable_class_balancing, size_of_smallest_class, name_of_smallest_class = \
            _class_balancing_check(y, y_transformer)
        verifier.update_data_verifier_for_class_balancing_validation(enable_class_balancing,
                                                                     class_balancing_fixed,
                                                                     size_of_smallest_class,
                                                                     name_of_smallest_class, y.shape[0])

    transformed_data_context = TransformedDataContext(
        X=X,
        y=y,
        X_valid=X_valid,
        y_valid=y_valid,
        sample_weight=sample_weight,
        sample_weight_valid=sample_weight_valid,
        x_raw_column_names=raw_data_context.x_raw_column_names,
        cv_splits_indices=raw_data_context.cv_splits_indices,
        num_cv_folds=raw_data_context.num_cv_folds,
        n_step=raw_data_context.n_step,
        validation_size=raw_data_context.validation_size,
        timeseries=raw_data_context.timeseries,
        timeseries_param_dict=raw_data_context.timeseries_param_dict,
        cache_store=cache_store,
        task_type=raw_data_context.task_type,
        X_raw_cleaned=raw_data_context.X,
        y_raw_cleaned=raw_data_context.y,
        X_valid_raw_cleaned=raw_data_context.X_valid,
        y_valid_raw_cleaned=raw_data_context.y_valid,
        data_snapshot_str=raw_data_context.data_snapshot_str,
        data_snapshot_str_with_quantiles=raw_data_context.data_snapshot_str_with_quantiles,
        output_data_snapshot_str_with_quantiles=raw_data_context.output_data_snapshot_str_with_quantiles
    )

    _log_data_info('X', transformed_data_context.X)
    _log_data_info('X_valid', transformed_data_context.X_valid)
    _log_data_info('y', transformed_data_context.y)
    _log_data_info('y_valid', transformed_data_context.y_valid)

    return transformed_data_context, y_transformer, X, y


def get_transformers_for_full_featurization(
        raw_data_context: RawDataContext,
        cache_store: CacheStore,
        is_onnx_compatible: bool = False,
        experiment_observer: Optional[ExperimentObserver] = None,
        enable_feature_sweeping: bool = False,
        verifier: Optional[VerifierManager] = None,
        enable_streaming: bool = False,
        feature_sweeping_config: Dict[str, Any] = {},
        enable_dnn: bool = False,
        force_text_dnn: bool = False,
        working_dir: Optional[str] = None,
        feature_sweeping_timeout_seconds: int = AutoMLDefaultTimeouts.DEFAULT_FEATSWEEP_TIMEOUT_SECONDS,
        enable_categorical_indicators: bool = False) \
        -> Optional[FeatureSweepedStateContainer]:
    """
    Performs the feature sweeping part of data transformation for all standard code paths.

    :param raw_data_context: The raw input data.
    :param cache_store: The object that should be used to cache featurized data.
    :param is_onnx_compatible: If works in onnx compatible mode.
    :param experiment_observer: The experiment observer.
    :param enable_feature_sweeping: Enable or disable feature sweeping.
    :param verifier: The verifier to check input data quality.
    :param enable_streaming: Enable or disable streaming.
    :param feature_sweeping_config: Config used for feature sweeping.
    :param enable_dnn: Flag to enable neural networks for forecasting and natural language processing.
    :param force_text_dnn: Flag to force add neural networks for natural language processing in feature sweeping.
    :param working_dir: Working directory to use for featurization/training.
    :param feature_sweeping_timeout_seconds: Feature sweeping timeout in seconds.
    :return: Container for objects generated by feature sweeping that will be needed in full featurization.
    """
    if raw_data_context.timeseries or \
            skip_featurization(raw_data_context.featurization, raw_data_context.timeseries):
        scenario_types_for_logging = []
        if raw_data_context.timeseries:
            scenario_types_for_logging.append("timeseries")
        if skip_featurization(raw_data_context.featurization, raw_data_context.timeseries):
            scenario_types_for_logging.append("skip featurization")
        _logger.info("Skipping mainstream sweeping logic. Detected {} scenario.".format(
            " + ".join(scenario_types_for_logging)))
        return None

    transformed_data_context, y_transformer, X, y = \
        create_transformed_data_context_no_streaming(raw_data_context,
                                                     cache_store,
                                                     verifier,
                                                     enable_dnn)
    if not sparse.issparse(transformed_data_context.X):
        transformed_data_context.X = _data_transformation_utilities._add_raw_column_names_to_X(
            transformed_data_context.X, raw_data_context.x_raw_column_names)

        featurization_config = None
        if isinstance(raw_data_context.featurization, FeaturizationConfig):
            featurization_config = raw_data_context.featurization

        is_cross_validation = transformed_data_context._is_cross_validation_scenario()
        with logging_utilities.log_activity(logger=_logger, activity_name="Beginning feature sweeping."):
            data_transformer = _suggest_featurizers_and_create_datatransformer(
                task=raw_data_context.task_type,
                X=transformed_data_context.X,
                y=transformed_data_context.y,
                featurization_config=featurization_config,
                observer=experiment_observer or NullExperimentObserver(),
                enable_feature_sweeping=enable_feature_sweeping,
                is_onnx_compatible=is_onnx_compatible,
                enable_dnn=enable_dnn,
                force_text_dnn=force_text_dnn,
                feature_sweeping_config=feature_sweeping_config,
                is_cross_validation=is_cross_validation,
                working_dir=working_dir,
                feature_sweeping_timeout_seconds=feature_sweeping_timeout_seconds,
                enable_categorical_indicators=enable_categorical_indicators)

        if verifier is not None:
            verifier.update_data_verifier_for_missing_values(data_transformer)
            verifier.update_data_verifier_for_high_cardinal_features(data_transformer.stats_and_column_purposes)

        return FeatureSweepedStateContainer(data_transformer=data_transformer,
                                            transformed_data_context=transformed_data_context,
                                            y_transformer=y_transformer,
                                            x=X,
                                            y=y)
    return None


def _get_data_snapshot(data: DataInputType, column_names_and_types: Optional[Dict[str, np.dtype]] = None,
                       column_purposes: Optional[List[StatsAndColumnPurposeType]] = None,
                       is_forecasting: bool = False) -> Any:
    Contract.assert_value(data, "data")
    try:
        if isinstance(data, Dataflow) and not column_names_and_types:
            # We need some data to figure out pandas dtypes.
            data = data.take(1000).to_pandas_dataframe()

        Validation.validate_type(data, "data", (np.ndarray, pd.DataFrame, sparse.spmatrix))

        if isinstance(data, pd.DataFrame) or isinstance(data, Dataflow):
            first_row = data.head(1)
            if not column_names_and_types:
                column_names_and_types = data.dtypes.to_dict()
            df_str = _data_transformation_utilities._get_data_snapshot_helper(
                first_row,
                column_names_and_types=column_names_and_types,
                column_purposes=column_purposes)
            sample_df_str = 'pd.DataFrame(' + df_str + ')'
            return sample_df_str
        elif isinstance(data, np.ndarray):
            np_array_str = _data_transformation_utilities._get_data_snapshot_helper(
                pd.Series(data[0]), column_purposes=column_purposes)
            sample_numpy_array_str = 'np.array([' + np_array_str + '])'
            return sample_numpy_array_str
        elif sparse.issparse(data):
            # Assuming that sparse matrix will be inferenced as a numpy array
            # TODO: Test sparse matrices with inference scenario
            np_array_str = _data_transformation_utilities._get_data_snapshot_helper(
                pd.Series(data[0, :].toarray().ravel()),
                column_purposes=column_purposes)
            sample_sparse_array_str = 'np.array([' + np_array_str + '])'
            return sample_sparse_array_str
    except (DataException, ValidationException):
        raise
    except Exception as e:
        exception_error_msg = "Raw data snapshot failed with exception of type: {}".format(type(e))
        _logger.error(exception_error_msg)
        error = AzureMLError.create(AutoMLInternal, error_details=exception_error_msg)
        raise ClientException(azureml_error=error, inner_exception=e) from e


def _get_output_snapshot(y: Union[np.ndarray, Dataflow]) -> str:
    """
    Get the snapshot representing the sample output.

    :param y: y data
    :return:
    """
    Contract.assert_value(y, "y")
    if isinstance(y, Dataflow):
        y = y.take(1000).to_pandas_dataframe().values
    y_type, _ = _data_transformation_utilities._get_dummy_value_by_purpose_or_dtype(npdtype=y.dtype)
    col_val = json.dumps([y_type]) if isinstance(y_type, str) else [y_type]
    output_snapshot_str = "np.array({0})".format(col_val)
    return output_snapshot_str


def get_raw_columns(
    X: pd.DataFrame,
    timeseries_param_dict: Optional[Dict[str, Any]],
    featurization_config: Optional[FeaturizationConfig] = None
) -> Set[Any]:
    """
    Get raw/unprocessed columns of data.
    :param X: Input training data.
    :param timeseries_param_dict: The parameters specific to time series.
    :param featurization_config: Featurization configuration if provided by the user.
    return: Set of raw columns.
    """
    drop_column_names = get_drop_columns(X, timeseries_param_dict, featurization_config)
    raw_columns = set(X.columns.values).difference(drop_column_names) if hasattr(X, 'columns') else set()

    return raw_columns


def does_data_have_exogenous_cols(
    raw_columns: Set[Any],
    grain_column_names: Optional[List[str]] = None,
    time_column_name: Optional[str] = None
) -> bool:

    """
    Check if the dataset has any exogenous columns or not.
    :param columns: set of raw/unprocessed column names that exists in data.
    :param grain_column_names: A list of grain_column_names.
    :param time_column_name: The name of the time column.
    return: bool of exogenous data.
    """

    # If the data is univariate, we enable stationary featurizer.
    # If the data has any exogenous columns, we disable stationary featurizer.
    exogenous_colnames = raw_columns - {time_column_name}
    if grain_column_names:
        exogenous_colnames -= set(grain_column_names)
    return bool(exogenous_colnames)


def get_time_series_data_non_stationary_ids(
    X: pd.DataFrame,
    y: np.ndarray,
    X_valid: pd.DataFrame = None,
    y_valid: Optional[np.ndarray] = None,
    featurization_config: Optional[FeaturizationConfig] = None,
    grain_column_names: List[str] = None,
    time_column_name: Optional[str] = None,
    freq: Optional[pd.DateOffset] = None
) -> List[GrainType]:

    """
    Check if the given time series is non-stationary.
    :param X: Input training data.
    :param y: y data.
    :param X_valid: Validation data.
    :param y_valid: Validation y data.
    :param featurization_config: Featurization configuration if provided by the user.
    :param grain_column_names: A list of grain_column_names.
    :param time_column_name: The name of the time column.
    :return: List of non-stationary columns.
    """

    with logging_utilities.log_activity(
            _logger,
            activity_name=constants.TelemetryConstants.RUN_STATIONARY_CHECK_NAME):

        non_stationary_time_series_ids = []   # type: List[GrainType]
        stationary_time_series_ids = []   # type: List[GrainType]

        # This check is done for legacy unittests which set X as np.ndarray.
        if isinstance(X, pd.DataFrame):
            if y_valid is None or len(y_valid) == 0:
                X_valid = pd.DataFrame()
                y_valid = np.array([])

            X_all = pd.concat([X, X_valid], axis=0)
            y_all = np.concatenate([y, y_valid])
            X_all[constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN] = y_all

            if grain_column_names is None or len(grain_column_names) == 0 or \
                    (grain_column_names == [constants.TimeSeriesInternal.DUMMY_GRAIN_COLUMN]
                     and grain_column_names[0] not in X.columns):
                X_all[constants.TimeSeriesInternal.DUMMY_GRAIN_COLUMN] =\
                    constants.TimeSeriesInternal.DUMMY_GRAIN_COLUMN
                grain_column_names = constants.TimeSeriesInternal.DUMMY_GRAIN_COLUMN

            tsds = TimeSeriesDataSet(X_all,
                                     time_column_name=time_column_name,
                                     time_series_id_column_names=grain_column_names,
                                     target_column_name=constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN
                                     )
            freq = freq if freq is not None else tsds.infer_freq()
            imputer = timeseries_transformer._get_target_imputer(
                constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN,
                freq,
                featurization_config
            )
            xtrans = imputer.fit_transform(tsds)
            X_all = xtrans.data
            X_all.dropna(subset=[constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN], inplace=True)
            X_all.reset_index(inplace=True, drop=False)

            for grain, df_grain in X_all.groupby(grain_column_names):
                stationary_test = unit_root_test_wrapper(
                    df_grain[constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN]
                )
                if (not stationary_test):
                    # adding non-stationary grains.
                    non_stationary_time_series_ids.append(grain)
                else:
                    # adding stationary grains.
                    stationary_time_series_ids.append(grain)
            stationary_ratio_to_total = len(stationary_time_series_ids) / (
                len(stationary_time_series_ids) + len(non_stationary_time_series_ids)
            )
            _logger.info("Ratio of stationary_time_series_ids to total_time_series_ids: "
                         + str(stationary_ratio_to_total))
            _logger.info("Number of non_stationary_time_series_ids before processing with threshold: "
                         + str(len(non_stationary_time_series_ids)))
            _logger.info("Number of stationary_time_series_ids before processing with threshold: "
                         + str(X_all.groupby(grain_column_names).ngroups - len(non_stationary_time_series_ids)))
            # Here, we check the stationary ratio to all is less than given threshold.
            # If stationary ratio is less than threshold, we assume all grains are non-stationary and
            # we start processing all grains to make them stationary.
            # Otherwise, we assume there is no non-stationary grains.
            if stationary_ratio_to_total < constants.TimeSeriesInternal.STATIONARY_THRESHOLD:
                non_stationary_time_series_ids.extend(stationary_time_series_ids)
                stationary_time_series_ids = []
            else:
                non_stationary_time_series_ids = []
            _logger.info("Number of non_stationary_time_series_ids after processing with threshold: "
                         + str(len(non_stationary_time_series_ids)))
            _logger.info("Number of stationary_time_series_ids after processing with threshold: "
                         + str(len(stationary_time_series_ids)))

        return non_stationary_time_series_ids


def _y_transform(
        y: np.ndarray,
        y_valid: Optional[np.ndarray],
        task_type: str,
        prediction_transform_type: Optional[str] = None,
        is_forecasting: bool = False,
        featurization_config: Optional[FeaturizationConfig] = None,
        grain_column_names: Optional[List[str]] = None,
        time_column_name: Optional[str] = None,
        freq: Optional[pd.DateOffset] = None,
        does_contain_exog_cols: bool = True,
        X: pd.DataFrame = None,
        X_valid: pd.DataFrame = None,
        enable_dnn: bool = False
) -> Tuple[Optional[preprocessing.LabelEncoder], np.ndarray, Optional[np.ndarray]]:
    """
    Apply label encoder for string, float and negative int type y data for classification and
    Apply post processing of y data for forecasting and regression tasks.

    :param y: y data
    :param y_valid: Validation y data
    :param task_type: CLASSIFICATION/REGRESSION
    :param prediction_transform_type: target column type
    :param is_forecasting: forecasting task type
    :param featurization_config: Featurization configuration if provided by the user.
    :param grain_column_names: A list of grain_column_names.
    :param time_column_name: The name of the time column.
    :param freq: frequency of data.
    :param does_contain_exog_cols: Flag to present if data has any exogenous column/s or not.
    :param X: Input training data.
    :param X_valid: Validation data.
    :param enable_dnn: If DNN is enabled.
    :return: tuple (y_transformer, y, y_valid)
    """
    y_transformer = None
    if task_type == constants.Tasks.CLASSIFICATION:
        y_type = runtime_utilities._get_column_data_type_as_str(y)
        y_valid_type = None if y_valid is None else runtime_utilities._get_column_data_type_as_str(y_valid)
        if runtime_utilities._is_y_transform_needed(y, y_type) or \
                runtime_utilities._is_y_transform_needed(y_valid, y_valid_type):
            # Currently y_transformer only support the label encoder for negative, float and categorical data.
            y_is_numeric = utilities._check_if_column_data_type_is_numerical(y_type)
            if y_valid is None:
                if runtime_utilities._is_y_mixed_type(y_type) and not y_is_numeric:
                    y = pd.Series(y).apply(str).values
            else:
                y_valid_type = str(y_valid_type)
                y_valid_is_numeric = utilities._check_if_column_data_type_is_numerical(y_valid_type)
                if runtime_utilities._is_y_conversion_needed(y_type, y_is_numeric, y_valid_type, y_valid_is_numeric):
                    y = pd.Series(y).apply(str).values
                if runtime_utilities._is_y_conversion_needed(y_valid_type, y_valid_is_numeric, y_type, y_is_numeric):
                    y_valid = pd.Series(y_valid).apply(str).values

            _logger.info("Start doing label encoding on y data.")
            y_transformer = preprocessing.LabelEncoder()
            try:
                if y_valid is None:
                    le = y_transformer.fit(y)
                    y = le.transform(y)
                else:
                    le = y_transformer.fit(np.vstack([y.reshape(-1, 1), y_valid.reshape(-1, 1)]))
                    y = le.transform(y)
                    y_valid = le.transform(y_valid)
                _logger.info("End doing label encoding on y data.")
            except Exception as e:
                _logger.error("Label encoding on y data failed with exception of type: {}".format(type(e)))
                raise DataException._with_error(
                    AzureMLError.create(InvalidValuesInData, target="target_column_data"), inner_exception=e
                ) from e
    # Forecasting or Regression Tasks
    else:

        # Disabling non-stationary detection and handling featurizer due to backward incompabilities.
        # The feature will be enabled with version 1.49.0 (WorkItem-2101125).
        # TODO: Please uncomment following checks for forecasting and
        # replace old target-type-transformer codes with the commented ones.

        # Current y-transformer supports post-processing of target column for forecasting and regression tasks.
        # steps = []
        # if is_forecasting:
        #     # TODO: enable_dnn will be removed after recalculating the statistics for data normalization
        #     # which will be solved with https://msdata.visualstudio.com/Vienna/_workitems/edit/2069308/.
        #     if does_contain_exog_cols or enable_dnn:
        #         _logger.info("Stationary Featurizer is not triggered.")
        #     else:
        #         # Start checking if data has any non stationary grains or not.
        #         _logger.info("Starting data stationarity check.")
        #         non_stationary_time_series_ids = get_time_series_data_non_stationary_ids(
        #             X, y,
        #             X_valid,
        #             y_valid,
        #             featurization_config,
        #             grain_column_names,
        #             time_column_name,
        #             freq
        #         )
        #         _logger.info("End checking data if it is stationary or not.")
        #         if len(non_stationary_time_series_ids) == 0:
        #             _logger.info("Stationary featurizer is not triggered because all grains are stationary.")
        #         else:
        #             # Current y-transformer supports differencing of target column
        #             # when the time series data is univariate and stationary_ratio to all < STATIONARY_THRESHOLD.
        #             _logger.info("Stationary featurizer is triggered.")
        #             y_transformer = DifferencingYTransformer(non_stationary_time_series_ids)
        #             steps.append((constants.TimeSeriesInternal.DIFFERENCING_Y_TRANSFORMER_NAME, y_transformer))

        _logger.info("Start doing y_transformation for target type transformer on y data.")
        if(prediction_transform_type == PredictionTransformTypes.INTEGER):
            y_transformer = TargetTypeTransformer(prediction_transform_type)
            if y_valid is None:
                y = y_transformer.fit_transform(y)
            else:
                y_transformer = y_transformer.fit(np.vstack([y.reshape(-1, 1), y_valid.reshape(-1, 1)]))
                y = y_transformer.transform(y)
                y_valid = y_transformer.transform(y_valid)
        _logger.info("End doing y_transformation for target type transformer on y data.")

        # if prediction_transform_type == PredictionTransformTypes.INTEGER:
        #     # Current y-transformer supports post-processing of target column for forecasting and regression tasks.
        #     _logger.info("y_transformation for TargetTypeTransformer is added.")
        #     y_transformer = TargetTypeTransformer(prediction_transform_type)
        #     steps.append((constants.TimeSeriesInternal.TARGET_TYPE_TRANSFORMER_NAME, y_transformer))
        # if steps:
        #     pipeline = Pipeline(steps)
        #     y_transformer = YPipelineTransformer(pipeline)
        #     y = y_transformer.fit_transform(y)
        #     y_valid = y_transformer.transform(y_valid)

    return y_transformer, y, y_valid


def _class_balancing_check(y, y_transformer):
    """
    Class balancing check based on y distribution.
    Imbalance would be detected if the Size of the minority class/Size of the majority class <= 20%.
    Comparison between minority & majority class, as opposed to minority class & overall training samples,
    makes more sense as demonstrated with this example:

    For a four class problem with data distributed among labels like this:{'a': 20, 'b': 20, 'c': 20, 'd': 200},
    the fraction of minority to majority is 10%, while minority to overall is 7.7%.

    For a four class problem with data distributed among labels like this:{'a': 20, 'b': 200, 'c': 200, 'd': 200},
    the fraction of minority to majority is 10%, while minority to overall is 3.2%.

    The first fraction is consistent, regardless of other classes and hence gives a more stable estimate of what
    clearly is an imbalance.

    :param y: Training y data
    :param y_transformer: Label-Encoder/Transformer used to encode target/label values
    :return: is class imbalanced, size of smallest class in y, name of smallest class in y
    """
    _logger.info("Start checking class balancing on y data.")
    if y_transformer is not None:
        y = y_transformer.inverse_transform(y)
    labels, counts = np.unique(y, return_counts=True)
    _logger.info("Num of classes: {}, Minority class size: {}, Majority class size: {}".format(len(counts),
                                                                                               min(counts),
                                                                                               max(counts)))
    is_class_imbalanced = False
    if float(min(counts)) <= constants.CheckImbalance.MINORITY_TO_MAJORITY_THRESHOLD_RATIO * float(max(counts)):
        is_class_imbalanced = True
    if is_class_imbalanced:
        _logger.info("Classes are imbalanced in training data.")

    size_of_smallest_class = min(counts)
    name_of_smallest_class = labels[np.argwhere(counts == size_of_smallest_class)]
    name_of_smallest_class = ', '.join(map(str, name_of_smallest_class.flatten()))
    return is_class_imbalanced, size_of_smallest_class, name_of_smallest_class


def _compute_sample_weight(y: DataSingleColumnInputType) -> np.ndarray:
    """
    Compute sample weight based on class weight.

    :param y: Input labels.
    :return: sample weights.
    """

    unique_vals = np.unique(y)

    class_weight = compute_class_weight(class_weight='balanced', classes=unique_vals, y=y)
    weights = {uniq: weight for uniq, weight in zip(unique_vals, class_weight)}
    sample_class_weight = [weights[label] for label in y]

    return np.array(sample_class_weight)

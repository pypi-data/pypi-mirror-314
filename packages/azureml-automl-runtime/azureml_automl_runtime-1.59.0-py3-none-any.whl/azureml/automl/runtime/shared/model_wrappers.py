# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module to wrap models that don't accept parameters such as 'fraction of the dataset'."""
import copy
import importlib
import logging
import math
import os
import pickle
import warnings
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union, cast
from typing import TYPE_CHECKING
import lightgbm as lgb
import numpy as np
import pandas as pd
import scipy
import sklearn
import sklearn.decomposition
import sklearn.naive_bayes
import sklearn.pipeline
from azureml._common._error_definition import AzureMLError
from azureml.automl.core import _codegen_utilities
from azureml.automl.core.automl_base_settings import AutoMLBaseSettings
from azureml.automl.core.forecasting_parameters import ForecastingParameters
from azureml.automl.core.shared import constants
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    AutoMLInternalLogSafe,
    DataShapeMismatch,
    ForecastPredictNotSupported,
    GenericTransformError,
    InsufficientMemory,
    InvalidArgumentType,
    PowerTransformerInverseTransform,
    QuantileRange,
    TimeseriesDfInvalidArgFcPipeYOnly,
    TimeseriesDfInvalidArgOnlyOneArgRequired,
    TimeseriesInsufficientDataForecast,
    TimeseriesNonContiguousTargetColumn,
    TransformerYMinGreater)
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared.constants import TimeSeries, TimeSeriesInternal
from azureml.automl.core.shared.exceptions import (AutoMLException,
                                                   DataException,
                                                   FitException,
                                                   PredictionException,
                                                   TransformException,
                                                   UntrainedModelException,
                                                   UserException,
                                                   ValidationException,
                                                   ResourceException)
from azureml.automl.core.shared.forecasting_exception import (
    ForecastingDataException, ForecastingConfigException
)
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.shared.types import GrainType
from azureml.automl.core.shared.utilities import get_min_points
from azureml.automl.runtime.column_purpose_detection._time_series_column_helper import convert_check_grain_value_types
from azureml.automl.runtime.frequency_fixer import fix_data_set_regularity_may_be
from azureml.automl.runtime.shared import forecasting_utils
from azureml.automl.runtime.shared._multi_grain_forecast_base import _MultiGrainForecastBase
from azureml.automl.runtime.shared.forecast_model_wrapper_base import ForecastModelWrapperBase
from azureml.automl.runtime.shared.score import _scoring_utilities
from azureml.automl.runtime.shared.types import DataInputType
from azureml.automl.core.constants import PredictionTransformTypes as _PredictionTransformTypes
import azureml.dataprep as dprep
from azureml.training.tabular.models import (
    _AbstractModelWrapper,
    CalibratedModel,
    RegressionPipeline,
    ForecastingPipelineWrapper,
    PipelineWithYTransformations,
    SparseScaleZeroOne,
    StackEnsembleBase,
    StackEnsembleClassifier,
    StackEnsembleRegressor,
    TargetTypeTransformer,
    DifferencingYTransformer,
    # The feature will be enabled with version 1.49.0 (WorkItem-2101125).
    # YPipelineTransformer,
    PreFittedSoftVotingRegressor,
    PreFittedSoftVotingClassifier
)

from packaging import version
from pandas.tseries.frequencies import to_offset
from scipy.special import inv_boxcox
from scipy.stats import boxcox
from sklearn import preprocessing
from sklearn.base import (BaseEstimator, ClassifierMixin, RegressorMixin,
                          TransformerMixin, clone)
from sklearn.calibration import CalibratedClassifierCV
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer


try:
    import xgboost as xgb

    xgboost_present = True
except ImportError:
    xgboost_present = False

try:
    import catboost as catb

    catboost_present = True
except ImportError:
    catboost_present = False


try:
    import torch
    from azureml.automl.runtime.shared._tabularnetworks import trainer as tabnet

    tabnet_present = True
except ImportError:
    tabnet_present = False

# NOTE:
# Here we import type checking only for type checking time.
# during runtime TYPE_CHECKING is set to False.
if TYPE_CHECKING:
    from azureml._common._error_definition.error_definition import ErrorDefinition
    from azureml.automl.runtime.featurizer.transformer.timeseries.time_series_imputer import TimeSeriesImputer
    from azureml.automl.runtime.featurizer.transformer.timeseries.timeseries_transformer import TimeSeriesTransformer

logger = logging.getLogger(__name__)

_generic_fit_error_message = 'Failed to fit the input data using {}'
_generic_transform_error_message = 'Failed to transform the input data using {}'
_generic_prediction_error_message = 'Failed to predict the test data using {}'


class LightGBMClassifier(BaseEstimator, ClassifierMixin, _AbstractModelWrapper):
    """
    LightGBM Classifier class.

    :param random_state:
        RandomState instance or None, optional (default=None)
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`.
    :type random_state: int or np.random.RandomState
    :param n_jobs: Number of parallel threads.
    :type n_jobs: int
    :param kwargs: Other parameters
        Check http://lightgbm.readthedocs.io/en/latest/Parameters.html
        for more parameters.
    """

    DEFAULT_MIN_DATA_IN_LEAF = 20

    def __init__(self, random_state=None, n_jobs=1, problem_info=None, **kwargs):
        """
        Initialize LightGBM Classifier class.

        :param random_state:
            RandomState instance or None, optional (default=None)
            If int, random_state is the seed used by the random number
            generator.
            If RandomState instance, random_state is the random number
            generator.
            If None, the random number generator is the RandomState instance
            used by `np.random`.
        :type random_state: int or np.random.RandomState
        :param n_jobs: Number of parallel threads.
        :type n_jobs: int
        :param problem_info: Problem metadata.
        :type problem_info: ProblemInfo
        :param kwargs: Other parameters
            Check http://lightgbm.readthedocs.io/en/latest/Parameters.html
            for more parameters.
        """
        self._kwargs = kwargs.copy()
        self.params = kwargs
        self.params['random_state'] = random_state
        self.params['n_jobs'] = n_jobs
        self.params = GPUHelper.lightgbm_add_gpu_support(problem_info, self.params)
        self.model = None  # type: Optional[sklearn.base.BaseEstimator]
        self._min_data_str = "min_data_in_leaf"
        self._min_child_samples = "min_child_samples"
        self._problem_info = problem_info.clean_attrs(['gpu_training_param_dict',
                                                       'dataset_categoricals']) if problem_info is not None else None

        # Both 'min_data_in_leaf' and 'min_child_samples' are required
        Contract.assert_true(
            self._min_data_str in kwargs or self._min_child_samples in kwargs,
            message="Failed to initialize LightGBMClassifier. Neither min_data_in_leaf nor min_child_samples passed",
            target="LightGBMClassifier", log_safe=True
        )

    def get_model(self):
        """
        Return LightGBM Classifier model.

        :return: Returns the fitted model if fit method has been called.
        Else returns None.
        """
        return self.model

    def fit(self, X: np.ndarray, y: np.ndarray, **kwargs: Any) -> "LightGBMClassifier":
        """
        Fit function for LightGBM Classifier model.

        :param X: Input data.
        :param y: Input target values.
        :param kwargs: other parameters
            Check http://lightgbm.readthedocs.io/en/latest/Parameters.html
            for more parameters.
        :return: Self after fitting the model.
        """
        N = X.shape[0]
        args = dict(self.params)
        if (self._min_data_str in args):
            if (self.params[self._min_data_str]
                    == LightGBMClassifier.DEFAULT_MIN_DATA_IN_LEAF):
                args[self._min_child_samples] = self.params[
                    self._min_data_str]
            else:
                args[self._min_child_samples] = int(
                    self.params[self._min_data_str] * N) + 1
            del args[self._min_data_str]
        else:
            min_child_samples = self.params[self._min_child_samples]
            if min_child_samples > 0 and min_child_samples < 1:
                # we'll convert from fraction to int as that's what LightGBM expects
                args[self._min_child_samples] = int(
                    self.params[self._min_child_samples] * N) + 1
            else:
                args[self._min_child_samples] = min_child_samples

        verbose_str = "verbose"
        if verbose_str not in args:
            args[verbose_str] = -10

        if self._problem_info is not None and self._problem_info.dataset_categoricals is not None:
            n_categorical = len(np.where(self._problem_info.dataset_categoricals)[0])
            kwargs['categorical_feature'] = [i for i in range(n_categorical)]

        self.model = lgb.LGBMClassifier(**args)
        try:
            self.model.fit(X, y, **kwargs)
        except Exception as e:
            # std::bad_alloc shows up as the error message if memory allocation fails. Unfortunately there is no
            # better way to check for this due to how LightGBM raises exceptions
            if 'std::bad_alloc' in str(e):
                raise ResourceException._with_error(
                    AzureMLError.create(InsufficientMemory, target='LightGbm'), inner_exception=e) from e
            raise FitException.from_exception(e, has_pii=True, target="LightGbm"). \
                with_generic_msg(_generic_fit_error_message.format(self.__class__.__name__))

        self.classes_ = np.unique(y)

        return self

    def __setstate__(self, state):
        if "_kwargs" not in state:
            state["_kwargs"] = {}
        if "_problem_info" in state:
            state["_problem_info"] = state["_problem_info"].clean_attrs(
                ['gpu_training_param_dict',
                 'dataset_categoricals']) if state["_problem_info"] is not None else None

        super().__setstate__(state)

    def __getstate__(self):
        state = self.__dict__

        # Backwards compatibility to handle inferencing on old SDK
        # pipeline_categoricals in ProblemInfo will always be None since we cleaned it, so we can inject it as part
        # of model init instead of fit
        if self._problem_info is not None and self._problem_info.dataset_categoricals is not None:
            n_categorical = len(np.where(self._problem_info.dataset_categoricals)[0])
            state["params"]["categorical_feature"] = [i for i in range(n_categorical)]

        return state

    def get_params(self, deep: bool = True) -> Dict[str, Any]:
        """
        Return parameters for LightGBM Regressor model.

        :param deep:
            If True, will return the parameters for this estimator
            and contained subobjects that are estimators.
        :type deep: bool
        :return: Parameters for LightGBM Regressor model.
        """
        params = self._kwargs.copy()
        params["random_state"] = self.params["random_state"]
        params["n_jobs"] = self.params["n_jobs"]
        params["problem_info"] = self._problem_info

        return params

    def __repr__(self) -> str:
        params = self.get_params(deep=False)
        return _codegen_utilities.generate_repr_str(self.__class__, params)

    def _get_imports(self) -> List[Tuple[str, str, Any]]:
        if self._problem_info:
            return [
                _codegen_utilities.get_import(self._problem_info)
            ]
        else:
            return []

    def predict(self, X):
        """
        Prediction function for LightGBM Classifier model.

        :param X: Input data.
        :type X: numpy.ndarray
        :return: Prediction values from LightGBM Classifier model.
        """
        try:
            return self.model.predict(X)
        except Exception as e:
            raise PredictionException.from_exception(e, target='LightGbm', has_pii=True). \
                with_generic_msg(_generic_prediction_error_message.format(self.__class__.__name__))

    def predict_proba(self, X):
        """
        Prediction class probabilities for X for LightGBM Classifier model.

        :param X: Input data.
        :type X: numpy.ndarray
        :return: Prediction probability values from LightGBM Classifier model.
        """
        try:
            predict_probas = self.model.predict_proba(X)
            if self.classes_ is not None and len(self.classes_) == 1:
                # Select only the first class since a dummy class is added when the train has only 1 class.
                return predict_probas[:, [0]]

            return predict_probas
        except Exception as e:
            raise PredictionException.from_exception(e, target='LightGbm', has_pii=True). \
                with_generic_msg(_generic_prediction_error_message.format(self.__class__.__name__))


class DaskLightGBMClassifier(BaseEstimator, ClassifierMixin, _AbstractModelWrapper):
    """
        Wrapper class for invoking Distributed lightgbm using DASK and TabularDataset
    """

    def __init__(self, random_state=None, problem_info=None, **kwargs):

        self._kwargs = kwargs.copy()
        self.params = kwargs
        self.params['random_state'] = random_state
        self._problem_info = problem_info
        self.model = None  # type: Optional[sklearn.base.BaseEstimator]
        self.params = GPUHelper.lightgbm_add_gpu_support(problem_info, self.params)

    def get_model(self):
        return self.model

    def fit(self, X, y, **kwargs):
        try:
            init_args = dict(self.params)
            LightGbmHelper.set_dask_lightgbm_advanced_params(init_args, self._problem_info)

            self.model = lgb.dask.DaskLGBMClassifier(**init_args)

            if self._problem_info.label_encoded_column_indexes:
                if self.params.get('device') != 'gpu':
                    logger.info("categorical col indexes {}".format(self._problem_info.label_encoded_column_indexes))
                    kwargs['categorical_feature'] = self._problem_info.label_encoded_column_indexes
                else:
                    # see https://github.com/microsoft/LightGBM/issues/4082
                    logger.info("not feeding categorical features since lightgbm max_bin param isn't compatible")

            self.model.fit(X, y, **kwargs)
            self.model = self.model.to_local()
        except Exception as e:
            raise FitException.from_exception(e, has_pii=True, target="DaskLightGbmClassifier"). \
                with_generic_msg(_generic_fit_error_message.format(self.__class__.__name__))

        return self

    def get_params(self, deep: bool = True) -> Dict[str, Any]:
        params = self._kwargs.copy()
        params["random_state"] = self.params["random_state"]
        params["problem_info"] = self._problem_info

        return params

    def predict(self, X):
        """
            This function is invoked
                - using dataflow during metric calculation phase during training sweeping loop.
                - using pandas dataframe during inference phase
        """
        try:
            if isinstance(X, dprep.Dataflow):
                X = X.to_pandas_dataframe()
            return self.model.predict(X)
        except Exception as e:
            raise PredictionException.from_exception(e, target='DaskLightGbmClassifier', has_pii=True). \
                with_generic_msg(_generic_prediction_error_message.format(self.__class__.__name__))

    def predict_proba(self, X):
        """
            This function is invoked
                - using dataflow during metric calculation phase during training sweeping loop.
                - using pandas dataframe during inference phase
        """
        try:
            if isinstance(X, dprep.Dataflow):
                X = X.to_pandas_dataframe()
            predict_probas = self.model.predict_proba(X)
            if self.classes_ is not None and len(self.classes_) == 1:
                # Select only the first class since a dummy class is added when the train has only 1 class.
                return predict_probas[:, [0]]

            return predict_probas
        except Exception as e:
            raise PredictionException.from_exception(e, target='LightGbm', has_pii=True). \
                with_generic_msg(_generic_prediction_error_message.format(self.__class__.__name__))

    @property
    def classes_(self):
        return self.model.classes_


class XGBoostClassifier(BaseEstimator, ClassifierMixin, _AbstractModelWrapper):
    """
    XGBoost Classifier class.

    :param random_state:
        RandomState instance or None, optional (default=None)
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`.
    :type random_state: int or np.random.RandomState
    :param n_jobs: Number of parallel threads.
    :type n_jobs: int
    :param kwargs: Other parameters
        Check https://xgboost.readthedocs.io/en/latest/parameter.html
        for more parameters.
    """

    def __init__(self, random_state=0, n_jobs=1, problem_info=None, **kwargs):
        """
        Initialize XGBoost Classifier class.

        :param random_state:
            RandomState instance or None, optional (default=None)
            If int, random_state is the seed used by the random number
            generator.
            If RandomState instance, random_state is the random number
            generator.
            If None, the random number generator is the RandomState instance
            used by `np.random`.
        :type random_state: int or np.random.RandomState
        :param n_jobs: Number of parallel threads.
        :type n_jobs: int
        :param kwargs: Other parameters
            Check https://xgboost.readthedocs.io/en/latest/parameter.html
            for more parameters.
        """
        self.params = kwargs.copy()
        self.params['random_state'] = random_state if random_state is not None else 0
        self.params['n_jobs'] = n_jobs if n_jobs != -1 else 0
        self.params['verbosity'] = 0
        self.params = GPUHelper.xgboost_add_gpu_support(problem_info, self.params)
        self._kwargs = kwargs
        self._problem_info = problem_info.clean_attrs(['gpu_training_param_dict']) \
            if problem_info is not None else None
        self.model = None
        self.classes_ = None

        Contract.assert_true(
            xgboost_present, message="Failed to initialize XGBoostClassifier. xgboost is not installed, "
                                     "please install xgboost for including xgboost based models.",
            target='XGBoostClassifier', log_safe=True
        )

    def __setstate__(self, state):
        if "_kwargs" not in state:
            state["_kwargs"] = {}
        if "_problem_info" not in state:
            state["_problem_info"] = None
        state["_problem_info"] = state["_problem_info"].clean_attrs(
            ['gpu_training_param_dict']) if state["_problem_info"] is not None else None
        super().__setstate__(state)

    def __repr__(self) -> str:
        params = self.get_params(deep=False)
        params.update(self._kwargs)
        return _codegen_utilities.generate_repr_str(self.__class__, params)

    def _get_imports(self) -> List[Tuple[str, str, Any]]:
        if self._problem_info:
            return [
                _codegen_utilities.get_import(self._problem_info)
            ]
        else:
            return []

    def get_model(self):
        """
        Return XGBoost Classifier model.

        :return: Returns the fitted model if fit method has been called.
        Else returns None.
        """
        return self.model

    def fit(self, X, y, **kwargs):
        """
        Fit function for XGBoost Classifier model.

        :param X: Input data.
        :type X: numpy.ndarray
        :param y: Input target values.
        :type y: numpy.ndarray
        :param kwargs: other parameters
            Check https://xgboost.readthedocs.io/en/latest/parameter.html
            for more parameters.
        :return: Self after fitting the model.
        """
        args = dict(self.params)
        verbose_str = "verbose"
        if verbose_str not in args:
            args[verbose_str] = -10

        self.model = xgb.XGBClassifier(**args)
        try:
            self.model.fit(X, y, **kwargs)
        except Exception as e:
            raise FitException.from_exception(e, has_pii=True, target="Xgboost"). \
                with_generic_msg(_generic_fit_error_message.format(self.__class__.__name__))

        self.classes_ = np.unique(y)

        return self

    def get_params(self, deep=True):
        """
        Return parameters for XGBoost Classifier model.

        :param deep: If True, will return the parameters for this estimator and contained subobjects that are
            estimators.
        :type deep: bool
        :return: Parameters for the XGBoost classifier model.
        """
        if deep:
            if self.model:
                return self.model.get_params(deep)
            else:
                return self.params
        else:
            params = {
                "random_state": self.params["random_state"],
                "n_jobs": self.params["n_jobs"],
                "problem_info": self._problem_info
            }
            params.update(self._kwargs)
            return params

    def predict(self, X):
        """
        Prediction function for XGBoost Classifier model.

        :param X: Input data.
        :type X: numpy.ndarray
        :return: Prediction values from XGBoost Classifier model.
        """
        if self.model is None:
            raise UntrainedModelException(target="Xgboost", has_pii=False)

        try:
            return self.model.predict(X)
        except Exception as e:
            raise PredictionException.from_exception(e, target="Xgboost", has_pii=True). \
                with_generic_msg(_generic_prediction_error_message.format(self.__class__.__name__))

    def predict_proba(self, X):
        """
        Prediction class probabilities for X for XGBoost Classifier model.

        :param X: Input data.
        :type X: numpy.ndarray
        :return: Prediction probability values from XGBoost Classifier model.
        """
        if self.model is None:
            raise UntrainedModelException(target="Xgboost", has_pii=False)
        try:
            predict_probas = self.model.predict_proba(X)
            if self.classes_ is not None and len(self.classes_) == 1:
                # Select only the first class since a dummy class is added when the train has only 1 class.
                return predict_probas[:, [0]]

            return predict_probas
        except Exception as e:
            raise PredictionException.from_exception(e, target="Xgboost", has_pii=True). \
                with_generic_msg(_generic_prediction_error_message.format(self.__class__.__name__))


class CatBoostClassifier(ClassifierMixin, _AbstractModelWrapper):
    """Model wrapper for the CatBoost Classifier."""

    def __init__(self, random_state=0, thread_count=1, **kwargs):
        """
        Construct a CatBoostClassifier.

        :param random_state:
            RandomState instance or None, optional (default=None)
            If int, random_state is the seed used by the random number
            generator.
            If RandomState instance, random_state is the random number
            generator.
            If None, the random number generator is the RandomState instance
            used by `np.random`.
        :type random_state: int or np.random.RandomState
        :param n_jobs: Number of parallel threads.
        :type n_jobs: int
        :param kwargs: Other parameters
            Check https://catboost.ai/docs/concepts/python-reference_parameters-list.html
            for more parameters.
        """
        self.params = kwargs
        self.params['random_state'] = random_state if random_state is not None else 0
        self.params['thread_count'] = thread_count
        self.model = None

        Contract.assert_true(
            catboost_present, message="Failed to initialize CatBoostClassifier. CatBoost is not installed, "
                                      "please install CatBoost for including CatBoost based models.",
            target='CatBoostClassifier', log_safe=True
        )

    def __repr__(self):
        return _codegen_utilities.generate_repr_str(self.__class__, self.get_params(deep=False))

    def get_model(self):
        """
        Return CatBoostClassifier model.

        :return: Returns the fitted model if fit method has been called.
        Else returns None.
        """
        return self.model

    def fit(self, X, y, **kwargs):
        """
        Fit function for CatBoostClassifier model.

        :param X: Input data.
        :param y: Input target values.
        :param kwargs: Other parameters
            Check https://catboost.ai/docs/concepts/python-reference_parameters-list.html
            for more parameters.
        :return: Self after fitting the model.
        """
        args = dict(self.params)
        verbose_str = "verbose"
        if verbose_str not in args:
            args[verbose_str] = False

        self.model = catb.CatBoostClassifier(**args)

        try:
            self.model.fit(X, y, **kwargs)
        except Exception as e:
            raise FitException.from_exception(e, has_pii=True, target="CatBoostClassifier"). \
                with_generic_msg(_generic_fit_error_message.format(self.__class__.__name__))

        return self

    def get_params(self, deep=True):
        """
        Return parameters for the CatBoostClassifier model.

        :param deep: If True, returns the model parameters for sub-estimators as well.
        :return: Parameters for the CatBoostClassifier model.
        """
        if self.model and deep:
            return self.model.get_params(deep)
        else:
            return self.params

    def predict(self, X):
        """
        Predict the target based on the dataset features.

        :param X: Input data.
        :return: Model predictions.
        """
        if self.model is None:
            raise UntrainedModelException(target="CatBoostClassifier", has_pii=False)
        try:
            return self.model.predict(X)
        except Exception as e:
            raise PredictionException.from_exception(e, target="CatBoostClassifier", has_pii=True). \
                with_generic_msg(_generic_prediction_error_message.format(self.__class__.__name__))

    def predict_proba(self, X):
        """
        Predict the probability of each class based on the dataset features.

        :param X: Input data.
        :return: Model predicted probabilities per class.
        """
        if self.model is None:
            raise UntrainedModelException(target="CatBoostClassifier", has_pii=False)
        try:
            return self.model.predict_proba(X)
        except Exception as e:
            raise PredictionException.from_exception(e, target="CatBoostClassifier", has_pii=True). \
                with_generic_msg(_generic_prediction_error_message.format(self.__class__.__name__))


class TabnetClassifier(ClassifierMixin, _AbstractModelWrapper):
    """Model wrapper for the Tabnet Classifier."""

    def __init__(self, num_steps=3, hidden_features=16, epochs=10, learning_rate=0.03, problem_info=None, **kwargs):
        """
        Construct a TabnetClassifier.

        :param kwargs: Other parameters
        """
        self.params = kwargs
        self.params['num_steps'] = num_steps if num_steps is not None else 3
        self.params['hidden_features'] = hidden_features if hidden_features is not None else 16
        self.params['epochs'] = epochs if epochs is not None else 10
        self.params['learning_rate'] = learning_rate if learning_rate is not None else 0.03
        self.params['problem_info'] = problem_info
        self.model = None
        self.classes_ = None
        Contract.assert_true(
            tabnet_present, message="Failed to initialize TabnetClassifier. Tabnet is not installed, "
                                    "please install pytorch and Tabnet for including Tabnet based models.",
            target=self.__class__.__name__, log_safe=True
        )

    def __repr__(self):
        return _codegen_utilities.generate_repr_str(self.__class__, self.get_params(deep=False))

    def get_model(self):
        """
        Return TabnetClassifier model.

        :return: Returns the fitted model if fit method has been called.
        Else returns None.
        """
        return self.model

    def fit(self, X, y, **kwargs):
        """
        Fit function for TabnetClassifier model.

        :param X: Input data.
        :param y: Input target values.
        :param kwargs: Other parameters
        :return: Self after fitting the model.
        """
        args = dict(self.params)
        self.model = tabnet.TabnetClassifier(**args)

        try:
            self.model.fit(X, y, **kwargs)
        except Exception as e:
            raise FitException.from_exception(e, has_pii=True, target=self.__class__.__name__). \
                with_generic_msg(_generic_fit_error_message.format(self.__class__.__name__))

        self.classes_ = np.unique(y)

        return self

    def get_params(self, deep=True):
        """
        Return parameters for the TabnetClassifier model.

        :param deep: If True, returns the model parameters for sub-estimators as well.
        :return: Parameters for the TabnetClassifier model.
        """
        if self.model and deep:
            return self.model.get_params(deep)
        else:
            return self.params

    def predict(self, X):
        """
        Predict the target based on the dataset features.

        :param X: Input data.
        :return: Model predictions.
        """
        if self.model is None:
            raise UntrainedModelException(target=self.__class__.__name__, has_pii=False)
        try:
            return self.model.predict(X)
        except Exception as e:
            raise PredictionException.from_exception(e, target=self.__class__.__name__, has_pii=True). \
                with_generic_msg(_generic_prediction_error_message.format(self.__class__.__name__))

    def predict_proba(self, X):
        """
        Predict the probability of each class based on the dataset features.

        :param X: Input data.
        :return: Model predicted probabilities per class.
        """
        if self.model is None:
            raise UntrainedModelException(target=self.__class__.__name__, has_pii=False)
        try:
            return self.model.predict_proba(X)
        except Exception as e:
            raise PredictionException.from_exception(e, target=self.__class__.__name__, has_pii=True). \
                with_generic_msg(_generic_prediction_error_message.format(self.__class__.__name__))


class SparseNormalizer(TransformerMixin, _AbstractModelWrapper):
    """
    Normalizes rows of an input matrix. Supports sparse matrices.

    :param norm:
        Type of normalization to perform - l1’, ‘l2’, or ‘max’,
        optional (‘l2’ by default).
    :type norm: str
    """

    def __init__(self, norm="l2", copy=True):
        """
        Initialize function for Sparse Normalizer transformer.

        :param norm:
            Type of normalization to perform - l1’, ‘l2’, or ‘max’,
            optional (‘l2’ by default).
        :type norm: str
        """
        self.norm = norm
        self.norm_str = "norm"
        self.model = Normalizer(norm, copy=True)

    def __repr__(self):
        return repr(self.model)

    def _get_imports(self) -> List[Tuple[str, str, Any]]:
        return [_codegen_utilities.get_import(self.model)]

    def get_model(self):
        """
        Return Sparse Normalizer model.

        :return: Sparse Normalizer model.
        """
        return self.model

    def fit(self, X, y=None):
        """
        Fit function for Sparse Normalizer model.

        :param X: Input data.
        :type X: numpy.ndarray
        :param y: Input target values.
        :type y: numpy.ndarray
        :return: Returns self.
        """
        return self

    def get_params(self, deep=True):
        """
        Return parameters for Sparse Normalizer model.

        :param deep:
            If True, will return the parameters for this estimator
            and contained subobjects that are estimators.
        :return: Parameters for Sparse Normalizer model.
        """
        params = {self.norm_str: self.norm}
        if self.model:
            params.update(self.model.get_params(deep))

        return params

    def transform(self, X):
        """
        Transform function for Sparse Normalizer model.

        :param X: Input data.
        :type X: numpy.ndarray
        :return: Transformed output of Sparse Normalizer.
        """
        try:
            return self.model.transform(X)
        except Exception as e:
            raise TransformException.from_exception(
                e, has_pii=True, target="SparseNormalizer",
                reference_code='model_wrappers.SparseNormalizer.transform'). \
                with_generic_msg(_generic_transform_error_message.format(self.__class__.__name__))


class PreprocWrapper(TransformerMixin, _AbstractModelWrapper):
    """Normalizes rows of an input matrix. Supports sparse matrices."""

    def __init__(self, cls, module_name=None, class_name=None, **kwargs):
        """
        Initialize PreprocWrapper class.

        :param cls:
        :param kwargs:
        """
        self.cls = cls
        if cls is not None:
            self.module_name = cls.__module__
            self.class_name = cls.__name__
        else:
            self.module_name = module_name
            self.class_name = class_name

        self.args = kwargs
        self.model = None

    def __repr__(self):
        params = self.get_params(deep=False)

        for param in ["module_name", "class_name"]:
            params.pop(param, None)

        return _codegen_utilities.generate_repr_str(self.__class__, params)

    def get_model(self):
        """
        Return wrapper model.

        :return: wrapper model
        """
        return self.model

    def fit(self, X, y=None):
        """
        Fit function for PreprocWrapper.

        :param X: Input data.
        :type X: numpy.ndarray or scipy.sparse.spmatrix
        :param y: Ignored.
        :type y: numpy.ndarray
        :return: Returns an instance of self.
        """
        args = dict(self.args)
        if self.cls is not None:
            self.model = self.cls(**args)
        else:
            assert self.module_name is not None
            assert self.class_name is not None
            mod = importlib.import_module(self.module_name)
            self.cls = getattr(mod, self.class_name)
        try:
            self.model.fit(X)
        except Exception as e:
            raise FitException.from_exception(e, has_pii=True, target="PreprocWrapper"). \
                with_generic_msg(_generic_fit_error_message.format(self.__class__.__name__))
        return self

    def get_params(self, deep=True):
        """
        Return parameters for PreprocWrapper.

        :param deep:
            If True, will return the parameters for this estimator
            and contained subobjects that are estimators.
        :type deep: bool
        :return: Parameters for PreprocWrapper.
        """
        # using the cls field instead of class_name & class_name because these fields might not be set
        # when this instance is created through unpickling
        params = {'module_name': self.cls.__module__, 'class_name': self.cls.__name__}
        if self.model:
            params.update(self.model.get_params(deep))
        else:
            params.update(self.args)

        return params

    def transform(self, X):
        """
        Transform function for PreprocWrapper.

        :param X: Input data.
        :type X: numpy.ndarray or scipy.sparse.spmatrix
        :return: Transformed output of inner model.
        """
        try:
            return self.model.transform(X)
        except Exception as e:
            raise TransformException.from_exception(
                e, has_pii=True, target="PreprocWrapper",
                reference_code='model_wrappers.PreprocWrapper.transform'). \
                with_generic_msg(_generic_transform_error_message.format(self.__class__.__name__))

    def inverse_transform(self, X):
        """
        Inverse transform function for PreprocWrapper.

        :param X: New data.
        :type X: numpy.ndarray or scipy.sparse.spmatrix
        :return: Inverse transformed data.
        """
        try:
            return self.model.inverse_transform(X)
        except Exception as e:
            raise TransformException.from_exception(
                e, has_pii=True, target="PreprocWrapper_Inverse",
                reference_code='model_wrappers.PreprocWrapper_Inverse.inverse_transform'). \
                with_generic_msg(_generic_transform_error_message.format(self.__class__.__name__))


class StandardScalerWrapper(PreprocWrapper):
    """Standard Scaler Wrapper around StandardScaler transformation."""

    def __init__(self, **kwargs):
        """Initialize Standard Scaler Wrapper class."""
        super().__init__(sklearn.preprocessing.StandardScaler,
                         **kwargs)


class NBWrapper(BaseEstimator, ClassifierMixin, _AbstractModelWrapper):
    """Naive Bayes Wrapper for conditional probabilities using either Bernoulli or Multinomial models."""

    def __init__(self, model, **kwargs):
        """
        Initialize Naive Bayes Wrapper class with either Bernoulli or Multinomial models.

        :param model: The actual model name.
        :type model: str
        """
        assert model in ['Bernoulli', 'Multinomial']
        self.model_name = model
        self.args = kwargs
        self.model = None

    def __repr__(self) -> str:
        params = self.get_params(deep=False)
        return _codegen_utilities.generate_repr_str(self.__class__, params)

    def get_model(self):
        """
        Return Naive Bayes model.

        :return: Naive Bayes model.
        """
        return self.model

    def fit(self, X, y, **kwargs):
        """
        Fit function for Naive Bayes model.

        :param X: Input data.
        :type X: numpy.ndarray or scipy.sparse.spmatrix
        :param y: Input target values.
        :type y: numpy.ndarray
        :param kwargs: Other arguments.
        """
        if self.model_name == 'Bernoulli':
            base_clf = sklearn.naive_bayes.BernoulliNB(**self.args)
        elif self.model_name == 'Multinomial':
            base_clf = sklearn.naive_bayes.MultinomialNB(**self.args)
        model = base_clf
        is_sparse = scipy.sparse.issparse(X)
        # sparse matrix with negative cells
        if is_sparse and np.any(X < 0).max():
            clf = sklearn.pipeline.Pipeline(
                [('MinMax scaler', SparseScaleZeroOne()),
                 (self.model_name + 'NB', base_clf)])
            model = clf
        # regular matrix with negative cells
        elif not is_sparse and np.any(X < 0):
            clf = sklearn.pipeline.Pipeline(
                [('MinMax scaler',
                  sklearn.preprocessing.MinMaxScaler(
                      feature_range=(0, X.max()))),
                 (self.model_name + 'NB', base_clf)])
            model = clf

        self.model = model
        try:
            self.model.fit(X, y, **kwargs)
        except MemoryError as me:
            raise ResourceException._with_error(
                AzureMLError.create(InsufficientMemory, target='NBWrapper'), inner_exception=me) from me
        except Exception as e:
            raise FitException.from_exception(e, has_pii=True, target="NBWrapper"). \
                with_generic_msg(_generic_fit_error_message.format(self.__class__.__name__))
        if hasattr(self.model, "classes_"):
            self.classes_ = self.model.classes_
        else:
            self.classes_ = np.unique(y)

    def get_params(self, deep=True):
        """
        Return parameters for Naive Bayes model.

        :param deep:
            If True, will return the parameters for this estimator
            and contained subobjects that are estimators.
        :type deep: bool
        :return: Parameters for Naive Bayes model.
        """
        params = {'model': self.model_name}
        if self.model:
            if isinstance(self.model, sklearn.pipeline.Pipeline):
                # we just want to get the parameters of the final estimator, excluding the preprocessors
                params.update(self.model._final_estimator.get_params(deep))
            else:
                params.update(self.model.get_params(deep))
        else:
            params.update(self.args)

        return params

    def predict(self, X):
        """
        Prediction function for Naive Bayes Wrapper Model.

        :param X: Input samples.
        :type X: numpy.ndarray or scipy.sparse.spmatrix
        :return: Prediction values from actual Naive Bayes model.
        """
        if self.model is None:
            raise UntrainedModelException(target="NBWrapper", has_pii=False)

        try:
            return self.model.predict(X)
        except Exception as e:
            raise PredictionException.from_exception(e, has_pii=True, target='NBWrapper'). \
                with_generic_msg(_generic_prediction_error_message.format(self.__class__.__name__))

    def predict_proba(self, X):
        """
        Prediction class probabilities for X for Naive Bayes Wrapper model.

        :param X: Input samples.
        :type X: numpy.ndarray or scipy.sparse.spmatrix
        :return: Prediction probability values from actual Naive Bayes model.
        """
        if self.model is None:
            raise UntrainedModelException(target="NBWrapper", has_pii=False)

        try:
            return self.model.predict_proba(X)
        except Exception as e:
            raise PredictionException.from_exception(e, has_pii=True, target='NBWrapper'). \
                with_generic_msg(_generic_prediction_error_message.format(self.__class__.__name__))


class TruncatedSVDWrapper(BaseEstimator, TransformerMixin, _AbstractModelWrapper):
    """
    Wrapper around Truncated SVD so that we only have to pass a fraction of dimensions.

    Read more at http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html

    :param min_components: Min number of desired dimensionality of output data.
    :type min_components: int
    :param max_components: Max number of desired dimensionality of output data.
    :type max_components: int
    :param random_state: RandomState instance or None, optional, default = None
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by np.random.
    :type random_state: int or np.random.RandomState
    :param kwargs: Other args taken by sklearn TruncatedSVD.
    """

    def __init__(
            self,
            min_components=2,
            max_components=200,
            random_state=None,
            **kwargs):
        """
        Initialize Truncated SVD Wrapper Model.

        :param min_components:
            Min number of desired dimensionality of output data.
        :type min_components: int
        :param max_components:
            Max number of desired dimensionality of output data.
        :type max_components: int
        :param random_state:
            RandomState instance or None, optional, default = None
            If int, random_state is the seed used by the random number
            generator;
            If RandomState instance, random_state is the random number
            generator;
            If None, the random number generator is the RandomState instance
            used by np.random.
        :type random_state: int or np.random.RandomState
        :param kwargs: Other args taken by sklearn TruncatedSVD.
        :return:
        """
        self._min_components = min_components
        self._max_components = max_components
        self.args = kwargs
        self.args['random_state'] = random_state

        self.n_components_str = "n_components"
        self.model = None

        Contract.assert_value(self.args.get(self.n_components_str), self.n_components_str,
                              reference_code=ReferenceCodes._TRUNCATED_SVD_WRAPPER_INIT)

    def get_model(self):
        """
        Return sklearn Truncated SVD Model.

        :return: Truncated SVD Model.
        """
        return self.model

    def fit(self, X, y=None):
        """
        Fit function for Truncated SVD Wrapper Model.

        :param X: Input data.
        :type X: numpy.ndarray or scipy.sparse.spmatrix
        :param y: Ignored.
        :return: Returns an instance of self.
        :rtype: azureml.automl.runtime.shared.model_wrappers.TruncatedSVDWrapper
        """
        args = dict(self.args)
        args[self.n_components_str] = min(
            self._max_components,
            max(self._min_components,
                int(self.args[self.n_components_str] * X.shape[1])))
        self.model = TruncatedSVD(**args)
        try:
            self.model.fit(X)
        except Exception as e:
            raise FitException.from_exception(e, has_pii=True, target="TruncatedSVDWrapper"). \
                with_generic_msg(_generic_fit_error_message.format(self.__class__.__name__))

        return self

    def get_params(self, deep=True):
        """
        Return parameters for Truncated SVD Wrapper Model.

        :param deep:
            If True, will return the parameters for this estimator
            and contained subobjects that are estimators.
        :type deep: bool
        :return: Parameters for Truncated SVD Wrapper Model.
        """
        params = {}
        params['min_components'] = self._min_components
        params['max_components'] = self._max_components
        params['random_state'] = self.args['random_state']
        if self.model:
            params.update(self.model.get_params(deep=deep))
        else:
            params.update(self.args)

        return self.args

    def transform(self, X):
        """
        Transform function for Truncated SVD Wrapper Model.

        :param X: Input data.
        :type X: numpy.ndarray or scipy.sparse.spmatrix
        :return: Transformed data of reduced version of X.
        :rtype: array
        """
        try:
            return self.model.transform(X)
        except Exception as e:
            raise TransformException.from_exception(
                e, has_pii=True, target="TruncatedSVDWrapper",
                reference_code='model_wrappers.TruncatedSVDWrapper.transform'). \
                with_generic_msg(_generic_transform_error_message.format(self.__class__.__name__))

    def inverse_transform(self, X):
        """
        Inverse Transform function for Truncated SVD Wrapper Model.

        :param X: New data.
        :type X: numpy.ndarray
        :return: Inverse transformed data. Always a dense array.
        :rtype: array
        """
        try:
            return self.model.inverse_transform(X)
        except Exception as e:
            raise TransformException.from_exception(
                e, has_pii=True, target="TruncatedSVDWrapper_Inverse",
                reference_code='model_wrappers.TruncatedSVDWrapper_Inverse.inverse_transform'). \
                with_generic_msg(_generic_transform_error_message.format(self.__class__.__name__))


class SVCWrapper(BaseEstimator, ClassifierMixin, _AbstractModelWrapper):
    """
    Wrapper around svm.SVC that always sets probability to True.

    Read more at:
    http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html.

    :param random_state: RandomState instance or None, optional, default = None
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by np.random.
    :type random_state: int or np.random.RandomState
    :param: kwargs: Other args taken by sklearn SVC.
    """

    def __init__(self, random_state=None, **kwargs):
        """
        Initialize svm.SVC Wrapper Model.

        :param random_state:
            RandomState instance or None, optional, default = None
            If int, random_state is the seed used by the random number
            generator;
            If RandomState instance, random_state is the random number
            generator;
            If None, the random number generator is the RandomState instance
            used by np.random.
        :type random_state: int or np.random.RandomState
        :param: kwargs: Other args taken by sklearn SVC.
        """
        kwargs["probability"] = True
        self.args = kwargs
        self.args['random_state'] = random_state
        self.model = sklearn.svm.SVC(**self.args)

    def __repr__(self) -> str:
        params = self.get_params(deep=False)
        return _codegen_utilities.generate_repr_str(self.__class__, params)

    def get_model(self):
        """
        Return sklearn.svm.SVC Model.

        :return: The svm.SVC Model.
        """
        return self.model

    def fit(self, X, y, **kwargs):
        """
        Fit function for svm.SVC Wrapper Model.

        :param X: Input data.
        :type X: numpy.ndarray or scipy.sparse.spmatrix
        :param y: Input target values.
        :type y: numpy.ndarray
        """
        try:
            self.model.fit(X, y, **kwargs)
        except Exception as e:
            raise FitException.from_exception(e, has_pii=True, target="SVCWrapper"). \
                with_generic_msg(_generic_fit_error_message.format(self.__class__.__name__))
        if hasattr(self.model, "classes_"):
            self.classes_ = self.model.classes_
        else:
            self.classes_ = np.unique(y)

    def get_params(self, deep=True):
        """
        Return parameters for svm.SVC Wrapper Model.

        :param deep:
            If True, will return the parameters for this estimator
            and contained subobjects that are estimators.
        :type deep: bool
        :return: parameters for svm.SVC Wrapper Model.
        """
        params = {'random_state': self.args['random_state']}
        params.update(self.model.get_params(deep=deep))

        return params

    def predict(self, X):
        """
        Prediction function for svm.SVC Wrapper Model. Perform classification on samples in X.

        :param X: Input samples.
        :type X: numpy.ndarray or scipy.sparse.spmatrix
        :return: Prediction values from svm.SVC model.
        :rtype: array
        """
        if self.model is None:
            raise UntrainedModelException(target='SVCWrapper', has_pii=False)

        try:
            return self.model.predict(X)
        except Exception as e:
            raise PredictionException.from_exception(e, has_pii=True, target='SVCWrapper'). \
                with_generic_msg(_generic_prediction_error_message.format(self.__class__.__name__))

    def predict_proba(self, X):
        """
        Prediction class probabilities for X for svm.SVC Wrapper model.

        :param X: Input samples.
        :type X: numpy.ndarray
        :return: Prediction probabilities values from svm.SVC model.
        :rtype: array
        """
        if self.model is None:
            raise UntrainedModelException(target='SVCWrapper', has_pii=False)

        try:
            return self.model.predict_proba(X)
        except Exception as e:
            raise PredictionException.from_exception(e, has_pii=True, target='SVCWrapper'). \
                with_generic_msg(_generic_prediction_error_message.format(self.__class__.__name__))


class NuSVCWrapper(BaseEstimator, ClassifierMixin, _AbstractModelWrapper):
    """
    Wrapper around svm.NuSVC that always sets probability to True.

    Read more at:
    http://scikit-learn.org/stable/modules/generated/sklearn.svm.NuSVC.html.

    :param random_state: RandomState instance or None, optional, default = None
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by np.random.
    :type random_state: int or np.random.RandomState
    :param: kwargs: Other args taken by sklearn NuSVC.
    """

    def __init__(self, random_state=None, **kwargs):
        """
        Initialize svm.NuSVC Wrapper Model.

        :param random_state: RandomState instance or None, optional,
        default = None
            If int, random_state is the seed used by the random number
            generator;
            If RandomState instance, random_state is the random number
            generator;
            If None, the random number generator is the RandomState instance
            used by np.random.
        :type random_state: int or np.random.RandomState
        :param: kwargs: Other args taken by sklearn NuSVC.
        """
        kwargs["probability"] = True
        self.args = kwargs
        self.args['random_state'] = random_state
        self.model = sklearn.svm.NuSVC(**self.args)

    def __repr__(self) -> str:
        params = self.get_params(deep=False)
        return _codegen_utilities.generate_repr_str(self.__class__, params)

    def get_model(self):
        """
        Return sklearn svm.NuSVC Model.

        :return: The svm.NuSVC Model.
        """
        return self.model

    def fit(self, X, y, **kwargs):
        """
        Fit function for svm.NuSVC Wrapper Model.

        :param X: Input data.
        :type X: numpy.ndarray or scipy.sparse.spmatrix
        :param y: Input target values.
        :type y: numpy.ndarray
        """
        try:
            self.model.fit(X, y, **kwargs)
        except Exception as e:
            raise FitException.from_exception(e, has_pii=True, target="NuSVCWrapper"). \
                with_generic_msg(_generic_fit_error_message.format(self.__class__.__name__))
        if hasattr(self.model, "classes_"):
            self.classes_ = self.model.classes_
        else:
            self.classes_ = np.unique(y)

    def get_params(self, deep=True):
        """
        Return parameters for svm.NuSVC Wrapper Model.

        :param deep:
            If True, will return the parameters for this estimator
            and contained subobjects that are estimators.
        :type deep: bool
        :return: Parameters for svm.NuSVC Wrapper Model.
        """
        params = {'random_state': self.args['random_state']}
        params.update(self.model.get_params(deep=deep))
        return params

    def predict(self, X):
        """
        Prediction function for svm.NuSVC Wrapper Model. Perform classification on samples in X.

        :param X: Input samples.
        :type X: numpy.ndarray or scipy.sparse.spmatrix
        :return: Prediction values from svm.NuSVC model.
        :rtype: array
        """
        if self.model is None:
            raise UntrainedModelException(target='NuSVCWrapper', has_pii=False)

        try:
            return self.model.predict(X)
        except Exception as e:
            raise PredictionException.from_exception(e, has_pii=True, target='NuSVCWrapper'). \
                with_generic_msg(_generic_prediction_error_message.format(self.__class__.__name__))

    def predict_proba(self, X):
        """
        Prediction class probabilities for X for svm.NuSVC Wrapper model.

        :param X: Input samples.
        :type X: numpy.ndarray
        :return: Prediction probabilities values from svm.NuSVC model.
        :rtype: array
        """
        if self.model is None:
            raise UntrainedModelException(target='NuSVCWrapper', has_pii=False)

        try:
            return self.model.predict_proba(X)
        except Exception as e:
            raise PredictionException.from_exception(e, has_pii=True, target='NuSVCWrapper'). \
                with_generic_msg(_generic_prediction_error_message.format(self.__class__.__name__))


class SGDClassifierWrapper(BaseEstimator, ClassifierMixin, _AbstractModelWrapper):
    """
    SGD Classifier Wrapper Class.

    Wrapper around SGD Classifier to support predict probabilities on loss
    functions other than log loss and modified huber loss. This breaks
    partial_fit on loss functions other than log and modified_huber since the
    calibrated model does not support partial_fit.

    Read more at:
    http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html.
    """

    def __init__(self, random_state=None, n_jobs=1, **kwargs):
        """
        Initialize SGD Classifier Wrapper Model.

        :param random_state:
            RandomState instance or None, optional (default=None)
            If int, random_state is the seed used by the random number
            generator;
            If RandomState instance, random_state is the random number
            generator;
            If None, the random number generator is the RandomState
            instance used
            by `np.random`.
        :type random_state: int or np.random.RandomState
        :param n_jobs: Number of parallel threads.
        :type n_jobs: int
        :param kwargs: Other parameters.
        """
        self.loss = "loss"
        self.model = None
        self._calibrated = False

        self.args = kwargs.copy()
        self.args['random_state'] = random_state
        self.args['n_jobs'] = n_jobs
        loss_arg = kwargs.get(self.loss, None)
        if loss_arg == "log":
            self.args[self.loss] = "log_loss"
        if loss_arg in ["log_loss", "modified_huber"]:
            self.model = sklearn.linear_model.SGDClassifier(**self.args)
        else:
            self.model = CalibratedModel(
                sklearn.linear_model.SGDClassifier(**self.args), random_state)
            self._calibrated = True

    def __repr__(self) -> str:
        params = self.get_params(deep=False)
        return _codegen_utilities.generate_repr_str(self.__class__, params)

    def get_model(self):
        """
        Return SGD Classifier Wrapper Model.

        :return: Returns the fitted model if fit method has been called.
        Else returns None
        """
        return self.model

    def fit(self, X, y, **kwargs):
        """
        Fit function for SGD Classifier Wrapper Model.

        :param X: Input data.
        :type X: numpy.ndarray
        :param y: Input target values.
        :type y: numpy.ndarray
        :param kwargs: Other parameters.
        :return: Returns an instance of inner SGDClassifier model.
        """
        try:
            model = self.model.fit(X, y, **kwargs)
        except Exception as e:
            raise FitException.from_exception(e, has_pii=True, target="SGDClassifierWrapper"). \
                with_generic_msg(_generic_fit_error_message.format(self.__class__.__name__))
        if hasattr(model, "classes_"):
            self.classes_ = model.classes_
        else:
            self.classes_ = np.unique(y)

        return model

    def get_params(self, deep=True):
        """
        Return parameters for SGD Classifier Wrapper Model.

        :param deep:
            If True, will return the parameters for this estimator
            and contained subobjects that are estimators.
        :type deep: bool
        :return: parameters for SGD Classifier Wrapper Model.
        """
        params = {}
        params['random_state'] = self.args['random_state']
        params['n_jobs'] = self.args['n_jobs']
        params.update(self.model.get_params(deep=deep))
        return self.args

    def predict(self, X):
        """
        Prediction function for SGD Classifier Wrapper Model.

        :param X: Input data.
        :type X: numpy.ndarray
        :return: Prediction values from SGD Classifier Wrapper model.
        """
        if self.model is None:
            raise UntrainedModelException(target='SGDClassifierWrapper', has_pii=False)

        try:
            return self.model.predict(X)
        except Exception as e:
            raise PredictionException.from_exception(e, has_pii=True, target='SGDClassifierWrapper'). \
                with_generic_msg(_generic_prediction_error_message.format(self.__class__.__name__))

    def predict_proba(self, X):
        """
        Prediction class probabilities for X for SGD Classifier Wrapper model.

        :param X: Input data.
        :type X: numpy.ndarray
        :return:
            Prediction probability values from SGD Classifier Wrapper model.
        """
        if self.model is None:
            raise UntrainedModelException(target='SGDClassifierWrapper', has_pii=False)

        try:
            return self.model.predict_proba(X)
        except Exception as e:
            raise PredictionException.from_exception(e, has_pii=True, target='SGDClassifierWrapper'). \
                with_generic_msg(_generic_prediction_error_message.format(self.__class__.__name__))

    def partial_fit(self, X, y, **kwargs):
        """
        Return partial fit result.

        :param X: Input data.
        :type X: numpy.ndarray
        :param y: Input target values.
        :type y: numpy.ndarray
        :param kwargs: Other parameters.
        :return: Returns an instance of inner SGDClassifier model.
        """
        Contract.assert_true(
            not self._calibrated, message="Failed to partially fit SGDClassifier. Calibrated model used.",
            target='SGDClassifierWrapper', log_safe=True
        )

        try:
            return self.model.partial_fit(X, y, **kwargs)
        except Exception as e:
            raise FitException.from_exception(e, has_pii=True, target="SGDClassifierWrapper"). \
                with_generic_msg(_generic_fit_error_message.format(self.__class__.__name__))


class EnsembleWrapper(BaseEstimator, ClassifierMixin):
    """Wrapper around multiple pipelines that combine predictions."""

    def __init__(self, models=None, clf=None, weights=None, task=constants.Tasks.CLASSIFICATION,
                 **kwargs):
        """
        Initialize EnsembleWrapper model.

        :param models: List of models to use in ensembling.
        :type models: list
        :param clf:
        """
        self.models = models
        self.clf = clf
        self.classes_ = None
        if self.clf:
            if hasattr(self.clf, 'classes_'):
                self.classes_ = self.clf.classes_
        self.weights = weights
        self.task = task

    def _get_imports(self) -> List[Tuple[str, str, Any]]:
        imports = []
        if self.models:
            imports.extend([
                _codegen_utilities.get_import(model[1]) for model in self.models
            ])
        if self.clf:
            imports.append(_codegen_utilities.get_import(self.clf))
        return imports

    def fit(self, X, y):
        """
        Fit function for EnsembleWrapper.

        :param X: Input data.
        :type X: numpy.ndarray
        :param y: Input target values.
        :type y: numpy.ndarray
        :return:
        """
        try:
            for m in self.models:
                m.fit(X, y)
        except Exception as e:
            # models in an ensemble could be from multiple frameworks
            raise FitException.from_exception(e, has_pii=True, target='EnsembleWrapper'). \
                with_generic_msg(_generic_fit_error_message.format(self.__class__.__name__))
        return self

    def get_params(self, deep=True):
        """
        Return parameters for Ensemble Wrapper Model.

        :param deep:
            If True, will return the parameters for this estimator
            and contained subobjects that are estimators.
        :type deep: bool
        :return: parameters for Ensemble Wrapper Model.
        """
        params = {
            "models": self.models,
            "clf": self.clf,
            "weights": self.weights,
            "task": self.task
        }

        return params

    def __repr__(self) -> str:
        params = self.get_params(deep=False)
        return _codegen_utilities.generate_repr_str(self.__class__, params)

    @staticmethod
    def get_ensemble_predictions(preds, weights=None,
                                 task=constants.Tasks.CLASSIFICATION):
        """
        Combine an array of probilities from compute_valid_predictions.

        Probabilities are combined into a single array of shape [num_samples, num_classes].
        """
        preds = np.average(preds, axis=2, weights=weights)
        if task == constants.Tasks.CLASSIFICATION:
            preds /= preds.sum(1)[:, None]
            assert np.all(preds >= 0) and np.all(preds <= 1)

        return preds

    @staticmethod
    def compute_valid_predictions(models, X, model_file_name_format=None, num_scores=None, splits=None):
        """Return an array of probabilities of shape [num_samples, num_classes, num_models]."""
        found_model = False
        if model_file_name_format:
            for i in range(num_scores):
                model_file_name = model_file_name_format.format(i)
                if os.path.exists(model_file_name):
                    with open(model_file_name, 'rb') as f:
                        m = pickle.load(f)
                    found_model = True
                    break
        else:
            for m in models:
                if m is not None:
                    found_model = True
                    break
        if not found_model:
            raise PredictionException.create_without_pii('Failed to generate predictions, no models found.',
                                                         target='EnsembleWrapper')
        if isinstance(m, list):
            m = m[0]
        preds0 = EnsembleWrapper._predict_proba_if_possible(m, X)
        num_classes = preds0.shape[1]

        preds = np.zeros((X.shape[0], num_classes, num_scores if num_scores else len(models)))
        if model_file_name_format:
            for i in range(num_scores):
                model_file_name = model_file_name_format.format(i)
                if os.path.exists(model_file_name):
                    with open(model_file_name, 'rb') as f:
                        m = pickle.load(f)
                    if isinstance(m, list):
                        for cv_fold, split in enumerate(splits):
                            preds[split, :, i] = EnsembleWrapper._predict_proba_if_possible(m[cv_fold], X[split])
                    else:
                        preds[:, :, i] = EnsembleWrapper._predict_proba_if_possible(m, X)
        else:
            for i, m in enumerate(models):
                if m is None:
                    continue
                if isinstance(m, list):
                    for cv_fold, split in enumerate(splits):
                        preds[split, :, i] = EnsembleWrapper._predict_proba_if_possible(m[cv_fold], X[split])
                else:
                    preds[:, :, i] = EnsembleWrapper._predict_proba_if_possible(m, X)
        return preds

    @staticmethod
    def _predict_proba_if_possible(model, X):
        try:
            if hasattr(model, 'predict_proba'):
                preds = model.predict_proba(X)
            else:
                preds = model.predict(X)
                preds = preds.reshape(-1, 1)
            return preds
        except Exception as e:
            raise PredictionException.from_exception(e, has_pii=True, target='EnsembleWrapper'). \
                with_generic_msg(_generic_prediction_error_message.format('EnsembleWrapper'))

    def predict(self, X):
        """
        Prediction function for EnsembleWrapper model.

        :param X: Input data.
        :type X: numpy.ndarray
        :return: Prediction values from EnsembleWrapper model.
        """
        try:
            if self.task == constants.Tasks.CLASSIFICATION:
                probs = self.predict_proba(X)
                return np.argmax(probs, axis=1)
            else:
                return self.predict_regression(X)
        except Exception as e:
            raise PredictionException.from_exception(e, has_pii=True, target='EnsembleWrapper'). \
                with_generic_msg(_generic_prediction_error_message.format(self.__class__.__name__))

    def predict_regression(self, X):
        """
        Predict regression results for X for EnsembleWrapper model.

        :param X: Input data.
        :type X: numpy.ndarray
        :return:
            Prediction probability values from EnsembleWrapper model.
        """
        valid_predictions = EnsembleWrapper.compute_valid_predictions(
            self.models, X)
        if self.clf is None:
            return EnsembleWrapper.get_ensemble_predictions(
                valid_predictions, self.weights, task=self.task)
        else:
            try:
                return self.clf.predict(valid_predictions.reshape(
                    valid_predictions.shape[0],
                    valid_predictions.shape[1] * valid_predictions.shape[2]))
            except Exception as e:
                raise PredictionException.from_exception(e, has_pii=True, target='EnsembleWrapper'). \
                    with_generic_msg(_generic_prediction_error_message.format(self.__class__.__name__))

    def predict_proba(self, X):
        """
        Prediction class probabilities for X for EnsembleWrapper model.

        :param X: Input data.
        :type X: numpy.ndarray
        :return:
            Prediction probability values from EnsembleWrapper model.
        """
        valid_predictions = EnsembleWrapper.compute_valid_predictions(
            self.models, X)
        if self.clf is None:
            return EnsembleWrapper.get_ensemble_predictions(
                valid_predictions, self.weights)
        else:
            try:
                # TODO make sure the order is same as during training\
                # ignore the first column due to collinearity
                valid_predictions = valid_predictions[:, 1:, :]
                return self.clf.predict_proba(valid_predictions.reshape(
                    valid_predictions.shape[0],
                    valid_predictions.shape[1] * valid_predictions.shape[2]))
            except Exception as e:
                raise PredictionException.from_exception(e, has_pii=True, target='EnsembleWrapper'). \
                    with_generic_msg(_generic_prediction_error_message.format(self.__class__.__name__))


class LinearSVMWrapper(BaseEstimator, ClassifierMixin, _AbstractModelWrapper):
    """
    Wrapper around linear svm to support predict_proba on sklearn's liblinear wrapper.

    :param random_state:
        RandomState instance or None, optional (default=None)
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`.
    :type random_state: int or np.random.RandomState
    :param kwargs: Other parameters.
    """

    def __init__(self, random_state=None, **kwargs):
        """
        Initialize Linear SVM Wrapper Model.

        :param random_state:
            RandomState instance or None, optional (default=None)
            If int, random_state is the seed used by the random number
            generator;
            If RandomState instance, random_state is the random number
            generator;
            If None, the random number generator is the RandomState
            instance used by `np.random`.
        :type random_state: int or np.random.RandomState
        :param kwargs: Other parameters.
        """
        self.args = kwargs
        self.args['random_state'] = random_state
        self.model = CalibratedModel(sklearn.svm.LinearSVC(**self.args))

    def __repr__(self) -> str:
        params = self.get_params(deep=False)
        return _codegen_utilities.generate_repr_str(self.__class__, params)

    def get_model(self):
        """
        Return Linear SVM Wrapper Model.

        :return: Linear SVM Wrapper Model.
        """
        return self.model

    def fit(self, X, y, **kwargs):
        """
        Fit function for Linear SVM Wrapper Model.

        :param X: Input data.
        :type X: numpy.ndarray
        :param y: Input target values.
        :type y: numpy.ndarray
        :param kwargs: Other parameters.
        """
        try:
            self.model.fit(X, y, **kwargs)
        except Exception as e:
            raise FitException.from_exception(e, has_pii=True, target="LinearSVMWrapper"). \
                with_generic_msg(_generic_fit_error_message.format(self.__class__.__name__))
        if hasattr(self.model, "classes_"):
            self.classes_ = self.model.classes_
        else:
            self.classes_ = np.unique(y)

    def get_params(self, deep=True):
        """
        Return parameters for Linear SVM Wrapper Model.

        :param deep:
            If True, will return the parameters for this estimator
            and contained subobjects that are estimators.
        :type deep: bool
        :return: parameters for Linear SVM Wrapper Model
        """
        params = {'random_state': self.args['random_state']}

        if isinstance(self.model.model, CalibratedClassifierCV):
            params.update(self.model.model.estimator.get_params(deep=deep))
        return params

    def predict_proba(self, X):
        """
        Prediction class probabilities for X for Linear SVM Wrapper model.

        :param X: Input data.
        :type X: numpy.ndarray
        :return: Prediction probability values from Linear SVM Wrapper model.
        """
        try:
            return self.model.predict_proba(X)
        except Exception as e:
            raise PredictionException.from_exception(e, has_pii=True, target='LinearSVMWrapper'). \
                with_generic_msg(_generic_prediction_error_message.format(self.__class__.__name__))

    def predict(self, X):
        """
        Prediction function for Linear SVM Wrapper Model.

        :param X: Input data.
        :type X: numpy.ndarray
        :return: Prediction values from Linear SVM Wrapper model.
        """
        try:
            return self.model.predict(X)
        except Exception as e:
            raise PredictionException.from_exception(e, has_pii=True, target='LinearSVMWrapper'). \
                with_generic_msg(_generic_prediction_error_message.format(self.__class__.__name__))


class LightGBMRegressor(BaseEstimator, RegressorMixin, _AbstractModelWrapper):
    """
    LightGBM Regressor class.

    :param random_state:
        RandomState instance or None, optional (default=None)
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`.
    :type random_state: int or np.random.RandomState
    :param kwargs: Other parameters.
    """

    DEFAULT_MIN_DATA_IN_LEAF = 20

    def __init__(self, random_state=None, n_jobs=1, problem_info=None, **kwargs):
        """
        Initialize LightGBM Regressor class.

        :param random_state:
            RandomState instance or None, optional (default=None)
            If int, random_state is the seed used by the random number
            generator;
            If RandomState instance, random_state is the random number
            generator;
            If None, the random number generator is the RandomState
            instance used by `np.random`.
        :type random_state: int or np.random.RandomState
        :param problem_info: Problem metadata.
        :type problem_info: ProblemInfo
        :param kwargs: Other parameters.
        """
        self._kwargs = kwargs.copy()
        self.params = kwargs
        self.params['random_state'] = random_state
        self.params['n_jobs'] = n_jobs
        self.params = GPUHelper.lightgbm_add_gpu_support(problem_info, self.params)
        self.model = None
        self._min_data_in_leaf = "min_data_in_leaf"
        self._min_child_samples = "min_child_samples"

        self._problem_info = problem_info.clean_attrs(
            ['gpu_training_param_dict',
             'dataset_categoricals']) if problem_info is not None else None

        # Both 'min_data_in_leaf' and 'min_child_samples' are required
        Contract.assert_true(
            self._min_data_in_leaf in kwargs or self._min_child_samples in kwargs,
            message="Failed to initialize LightGBMRegressor. Neither min_data_in_leaf nor min_child_samples passed",
            target="LightGBMRegressor", log_safe=True
        )

    def get_model(self):
        """
        Return LightGBM Regressor model.

        :return:
            Returns the fitted model if fit method has been called.
            Else returns None
        """
        return self.model

    def fit(self, X, y, **kwargs):
        """
        Fit function for LightGBM Regressor model.

        :param X: Input data.
        :type X: numpy.ndarray
        :param y: Labels for the data.
        :type y: numpy.ndarray
        :param kwargs: Other parameters.
        :return: Returns self after fitting the model.
        """
        verbose_str = "verbose"
        n = X.shape[0]
        params = dict(self.params)
        if (self._min_data_in_leaf in params):
            if (self.params[self._min_data_in_leaf]
                    == LightGBMRegressor.DEFAULT_MIN_DATA_IN_LEAF):
                params[self._min_child_samples] = self.params[
                    self._min_data_in_leaf]
            else:
                params[self._min_child_samples] = int(
                    self.params[self._min_data_in_leaf] * n) + 1
            del params[self._min_data_in_leaf]
        else:
            min_child_samples = self.params[self._min_child_samples]
            if min_child_samples > 0 and min_child_samples < 1:
                # we'll convert from fraction to int as that's what LightGBM expects
                params[self._min_child_samples] = int(
                    self.params[self._min_child_samples] * n) + 1
            else:
                params[self._min_child_samples] = min_child_samples

        if verbose_str not in params:
            params[verbose_str] = -1

        if self._problem_info is not None and self._problem_info.dataset_categoricals is not None:
            n_categorical = len(np.where(self._problem_info.dataset_categoricals)[0])
            kwargs['categorical_feature'] = [i for i in range(n_categorical)]

        self.model = lgb.LGBMRegressor(**params)
        try:
            self.model.fit(X, y, **kwargs)
        except Exception as e:
            raise FitException.from_exception(e, has_pii=True, target="LightGbm"). \
                with_generic_msg(_generic_fit_error_message.format(self.__class__.__name__))

        return self

    def __setstate__(self, state):
        if "_kwargs" not in state:
            state["_kwargs"] = {}
        if "_problem_info" in state:
            state["_problem_info"] = state["_problem_info"].clean_attrs(
                ['gpu_training_param_dict',
                 'dataset_categoricals']) if state["_problem_info"] is not None else None

        super().__setstate__(state)

    def __getstate__(self):
        state = self.__dict__

        # Backwards compatibility to handle inferencing on old SDK
        # pipeline_categoricals in ProblemInfo will always be None since we cleaned it, so we can inject it as part
        # of model init instead of fit
        if self._problem_info is not None and self._problem_info.dataset_categoricals is not None:
            n_categorical = len(np.where(self._problem_info.dataset_categoricals)[0])
            state["params"]["categorical_feature"] = [i for i in range(n_categorical)]

        return state

    def get_params(self, deep: bool = True) -> Dict[str, Any]:
        """
        Return parameters for LightGBM Regressor model.

        :param deep:
            If True, will return the parameters for this estimator
            and contained subobjects that are estimators.
        :type deep: bool
        :return: Parameters for LightGBM Regressor model.
        """
        params = self._kwargs.copy()
        params["random_state"] = self.params["random_state"]
        params["n_jobs"] = self.params["n_jobs"]
        params["problem_info"] = self._problem_info

        return params

    def __repr__(self) -> str:
        params = self.get_params(deep=False)
        return _codegen_utilities.generate_repr_str(self.__class__, params)

    def _get_imports(self) -> List[Tuple[str, str, Any]]:
        if self._problem_info:
            return [
                _codegen_utilities.get_import(self._problem_info)
            ]
        else:
            return []

    def predict(self, X):
        """
        Prediction function for LightGBM Regressor model.

        :param X: Input data.
        :type X: numpy.ndarray
        :return: Prediction values from LightGBM Regressor model.
        """
        try:
            return self.model.predict(X)
        except Exception as e:
            raise PredictionException.from_exception(e, has_pii=True, target='LightGBMRegressor'). \
                with_generic_msg(_generic_prediction_error_message.format(self.__class__.__name__))


class DaskLightGBMRegressor(BaseEstimator, RegressorMixin, _AbstractModelWrapper):
    """
        Wrapper class for invoking Distributed lightgbm using DASK and TabularDataset
    """

    def __init__(self, random_state=None, problem_info=None, **kwargs):

        self._kwargs = kwargs.copy()
        self.params = kwargs
        self.params['random_state'] = random_state
        self._problem_info = problem_info
        self.model = None  # type: Optional[sklearn.base.BaseEstimator]
        self.params = GPUHelper.lightgbm_add_gpu_support(problem_info, self.params)

    def get_model(self):
        return self.model

    def fit(self, X, y, **kwargs):
        try:
            init_args = dict(self.params)
            LightGbmHelper.set_dask_lightgbm_advanced_params(init_args, self._problem_info)

            self.model = lgb.dask.DaskLGBMRegressor(**init_args)

            if self._problem_info.label_encoded_column_indexes:
                if self.params.get('device') != 'gpu':
                    logger.info("categorical col indexes {}".format(self._problem_info.label_encoded_column_indexes))
                    kwargs['categorical_feature'] = self._problem_info.label_encoded_column_indexes
                else:
                    # see https://github.com/microsoft/LightGBM/issues/4082
                    logger.info("not feeding categorical features since lightgbm max_bin param isn't compatible")

            self.model.fit(X, y, **kwargs)
            self.model = self.model.to_local()
        except Exception as e:
            raise FitException.from_exception(e, has_pii=True, target="DaskLightGbmRegressor"). \
                with_generic_msg(_generic_fit_error_message.format(self.__class__.__name__))

        return self

    def get_params(self, deep: bool = True) -> Dict[str, Any]:
        params = self._kwargs.copy()
        params["random_state"] = self.params["random_state"]
        params["problem_info"] = self._problem_info

        return params

    def predict(self, X):
        """
            This function is invoked
                - using dataflow during metric calculation phase during training sweeping loop.
                - using pandas dataframe during inference phase
        """
        try:
            if isinstance(X, dprep.Dataflow):
                X = X.to_pandas_dataframe()
            return self.model.predict(X)
        except Exception as e:
            raise PredictionException.from_exception(e, has_pii=True, target='LightGBMRegressor'). \
                with_generic_msg(_generic_prediction_error_message.format(self.__class__.__name__))


class XGBoostRegressor(BaseEstimator, RegressorMixin, _AbstractModelWrapper):
    """
    XGBoost Regressor class.

    :param random_state:
        RandomState instance or None, optional (default=None)
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`.
    :type random_state: int or np.random.RandomState
    :param n_jobs: Number of parallel threads.
    :type n_jobs: int
    :param kwargs: Other parameters
        Check https://xgboost.readthedocs.io/en/latest/parameter.html
        for more parameters.
    """
    # The version after which the XGBOOST started to create a warning as:
    #  src/objective/regression_obj.cu:152: reg:linear is now deprecated in favor of reg:squarederror.
    _RENAME_VERSION = version.parse('0.83')
    _OBJECTIVE = 'objective'
    _REG_LINEAR = 'reg:linear'
    _REG_SQUAREDERROR = 'reg:squarederror'
    _ALL_OBJECTIVES = {_REG_LINEAR, _REG_SQUAREDERROR}

    def __init__(self, random_state=0, n_jobs=1, problem_info=None, **kwargs):
        """
        Initialize XGBoost Regressor class.

        :param random_state:
            RandomState instance or None, optional (default=None)
            If int, random_state is the seed used by the random number
            generator.
            If RandomState instance, random_state is the random number
            generator.
            If None, the random number generator is the RandomState instance
            used by `np.random`.
        :type random_state: int or np.random.RandomState
        :param n_jobs: Number of parallel threads.
        :type n_jobs: int
        :param kwargs: Other parameters
            Check https://xgboost.readthedocs.io/en/latest/parameter.html
            for more parameters.
        """
        self.params = kwargs.copy()
        self.params['random_state'] = random_state if random_state is not None else 0
        self.params['n_jobs'] = n_jobs if n_jobs != -1 else 0
        self.params['verbosity'] = 0
        self.params = GPUHelper.xgboost_add_gpu_support(problem_info, self.params)
        self.model = None
        self._problem_info = problem_info.clean_attrs(['gpu_training_param_dict']) \
            if problem_info is not None else None
        self._kwargs = kwargs

        Contract.assert_true(
            xgboost_present, message="Failed to initialize XGBoostRegressor. xgboost is not installed, "
                                     "please install xgboost for including xgboost based models.",
            target='XGBoostRegressor', log_safe=True
        )

    def __setstate__(self, state):
        if "_kwargs" not in state:
            state["_kwargs"] = {}
        if "_problem_info" not in state:
            state["_problem_info"] = None
        state["_problem_info"] = state["_problem_info"].clean_attrs(['gpu_training_param_dict']) \
            if state["_problem_info"] is not None else None
        super().__setstate__(state)

    def __repr__(self) -> str:
        params = self.get_params(deep=False)
        params.update(self._kwargs)
        return _codegen_utilities.generate_repr_str(self.__class__, params)

    def _get_imports(self) -> List[Tuple[str, str, Any]]:
        if self._problem_info:
            return [
                _codegen_utilities.get_import(self._problem_info)
            ]
        else:
            return []

    def get_model(self):
        """
        Return XGBoost Regressor model.

        :return: Returns the fitted model if fit method has been called.
        Else returns None.
        """
        return self.model

    def _get_objective_safe(self) -> str:
        """
        Get the objective, which will not throw neither error nor warning.

        :return: The objective, which is safe to use: reg:linear or reg:squarederror.
        """
        if version.parse(xgb.__version__) < XGBoostRegressor._RENAME_VERSION:
            # This objective is deprecated in versions later then _RENAME_VERSION.
            return XGBoostRegressor._REG_LINEAR
        return XGBoostRegressor._REG_SQUAREDERROR

    def _replace_objective_maybe(self, params_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check the self.params for unsafe objective and replace it by the safe one.

        Replae the objective, so that we will not get neither error nor warning during
        XGBoostRegressor fitting.
        """
        params_dict = copy.deepcopy(params_dict)
        if XGBoostRegressor._OBJECTIVE in self.params.keys():
            objective = params_dict.get(XGBoostRegressor._OBJECTIVE)
            if objective in XGBoostRegressor._ALL_OBJECTIVES:
                params_dict[XGBoostRegressor._OBJECTIVE] = self._get_objective_safe()
        else:
            params_dict[XGBoostRegressor._OBJECTIVE] = self._get_objective_safe()
        return params_dict

    def fit(self, X, y, **kwargs):
        """
        Fit function for XGBoost Regressor model.

        :param X: Input data.
        :type X: numpy.ndarray
        :param y: Input target values.
        :type y: numpy.ndarray
        :param kwargs: other parameters
            Check https://xgboost.readthedocs.io/en/latest/parameter.html
            for more parameters.
        :return: Self after fitting the model.
        """
        args = dict(self.params)
        args = self._replace_objective_maybe(args)
        verbose_str = "verbose"
        if verbose_str not in args:
            args[verbose_str] = -10

        self.model = xgb.XGBRegressor(**args)
        try:
            self.model.fit(X, y, **kwargs)
        except Exception as e:
            raise FitException.from_exception(e, has_pii=True, target="Xgboost"). \
                with_generic_msg(_generic_fit_error_message.format(self.__class__.__name__))

        return self

    def get_params(self, deep=True):
        """
        Return parameters for XGBoost Regressor model.

        :param deep:
            If True, will return the parameters for this estimator and contained subobjects that are estimators.
        :type deep: bool
        :return: Parameters for the XGBoost classifier model.
        """
        if deep:
            if self.model:
                return self.model.get_params(deep)
            else:
                return self.params
        else:
            params = {
                "random_state": self.params["random_state"],
                "n_jobs": self.params["n_jobs"],
                "problem_info": self._problem_info,
            }
            params.update(self._kwargs)
            return params

    def predict(self, X):
        """
        Prediction function for XGBoost Regressor model.

        :param X: Input data.
        :type X: numpy.ndarray
        :return: Prediction values from XGBoost Regressor model.
        """
        if self.model is None:
            raise UntrainedModelException.create_without_pii(target="Xgboost")
        return self.model.predict(X)


class CatBoostRegressor(RegressorMixin, _AbstractModelWrapper):
    """Model wrapper for the CatBoost Regressor."""

    def __init__(self, random_state=0, thread_count=1, **kwargs):
        """
        Construct a CatBoostRegressor.

        :param random_state:
            RandomState instance or None, optional (default=None)
            If int, random_state is the seed used by the random number
            generator.
            If RandomState instance, random_state is the random number
            generator.
            If None, the random number generator is the RandomState instance
            used by `np.random`.
        :type random_state: int or np.random.RandomState
        :param n_jobs: Number of parallel threads.
        :type n_jobs: int
        :param kwargs: Other parameters
            Check https://catboost.ai/docs/concepts/python-reference_parameters-list.html
            for more parameters.
        """
        self.params = kwargs
        self.params['random_state'] = random_state
        self.params['thread_count'] = thread_count
        self.model = None

        Contract.assert_true(
            catboost_present, message="Failed to initialize CatBoostRegressor. CatBoost is not installed, "
                                      "please install CatBoost for including CatBoost based models.",
            target='CatBoostRegressor', log_safe=True
        )

    def __repr__(self):
        return _codegen_utilities.generate_repr_str(self.__class__, self.get_params(deep=False))

    def get_model(self):
        """
        Return CatBoostRegressor model.

        :return: Returns the fitted model if fit method has been called.
        Else returns None.
        """
        return self.model

    def fit(self, X, y, **kwargs):
        """
        Fit function for CatBoostRegressor model.

        :param X: Input data.
        :param y: Input target values.
        :param kwargs: Other parameters
            Check https://catboost.ai/docs/concepts/python-reference_parameters-list.html
            for more parameters.
        :return: Self after fitting the model.
        """
        args = dict(self.params)
        verbose_str = "verbose"
        if verbose_str not in args:
            args[verbose_str] = False

        self.model = catb.CatBoostRegressor(**args)
        self.model.fit(X, y, **kwargs)

        return self

    def get_params(self, deep=True):
        """
        Return parameters for the CatBoostRegressor model.

        :param deep: If True, returns the model parameters for sub-estimators as well.
        :return: Parameters for the CatBoostRegressor model.
        """
        if self.model and deep:
            return self.model.get_params(deep)
        else:
            return self.params

    def predict(self, X):
        """
        Predict the target based on the dataset features.

        :param X: Input data.
        :return: Model predictions.
        """
        if self.model is None:
            raise UntrainedModelException.create_without_pii(target='CatBoostRegressor')
        return self.model.predict(X)


class TabnetRegressor(RegressorMixin, _AbstractModelWrapper):
    """Model wrapper for the Tabnet Regressor."""

    def __init__(self, num_steps=3, hidden_features=16, epochs=10, learning_rate=0.03, problem_info=None, **kwargs):
        """
        Construct a TabnetRegressor.

        :param kwargs: Other parameters
        """
        self.params = kwargs
        self.params['num_steps'] = num_steps if num_steps is not None else 3
        self.params['hidden_features'] = hidden_features if hidden_features is not None else 16
        self.params['epochs'] = epochs if epochs is not None else 10
        self.params['learning_rate'] = learning_rate if learning_rate is not None else 0.03
        self.params['problem_info'] = problem_info
        self.model = None

        Contract.assert_true(
            tabnet_present, message="Failed to initialize TabnetRegressor. Tabnet is not installed, "
                                    "please install pytorch and Tabnet for including Tabnet based models.",
            target=self.__class__.__name__, log_safe=True
        )

    def __repr__(self):
        return _codegen_utilities.generate_repr_str(self.__class__, self.get_params(deep=False))

    def get_model(self):
        """
        Return TabnetRegressor model.

        :return: Returns the fitted model if fit method has been called.
        Else returns None.
        """
        return self.model

    def fit(self, X, y, **kwargs):
        """
        Fit function for TabnetRegressor model.

        :param X: Input data.
        :param y: Input target values.
        :param kwargs: Other parameters
        :return: Self after fitting the model.
        """
        args = dict(self.params)

        self.model = tabnet.TabnetRegressor(**args)
        self.model.fit(X, y, **kwargs)

        return self

    def get_params(self, deep=True):
        """
        Return parameters for the TabnetRegressor model.

        :param deep: If True, returns the model parameters for sub-estimators as well.
        :return: Parameters for the TabnetRegressor model.
        """
        if self.model and deep:
            return self.model.get_params(deep)
        else:
            return self.params

    def predict(self, X):
        """
        Predict the target based on the dataset features.

        :param X: Input data.
        :return: Model predictions.
        """
        if self.model is None:
            raise UntrainedModelException.create_without_pii(target=self.__class__.__name__)
        return self.model.predict(X)


class QuantileTransformerWrapper(BaseEstimator, TransformerMixin):
    """
    Quantile transformer wrapper class.

    Transform features using quantiles information.

    :param n_quantiles:
        Number of quantiles to be computed. It corresponds to the number
        of landmarks used to discretize the cumulative density function.
    :type n_quantiles: int
    :param output_distribution:
        Marginal distribution for the transformed data.
        The choices are 'uniform' (default) or 'normal'.
    :type output_distribution: string

    Read more at:
    http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.QuantileTransformer.html.
    """

    def __init__(self, n_quantiles=1000, output_distribution="uniform"):
        """
        Initialize function for Quantile transformer.

        :param n_quantiles:
            Number of quantiles to be computed. It corresponds to the number
            of landmarks used to discretize the cumulative density function.
        :type n_quantiles: int
        :param output_distribution:
            Marginal distribution for the transformed data.
            The choices are 'uniform' (default) or 'normal'.
        :type output_distribution: string
        """
        self.transformer = preprocessing.QuantileTransformer(
            n_quantiles=n_quantiles,
            output_distribution=output_distribution)

    def __repr__(self):
        return repr(self.transformer)

    def _get_imports(self) -> List[Tuple[str, str, Any]]:
        return [
            _codegen_utilities.get_import(self.transformer)
        ]

    def __str__(self):
        """
        Return transformer details into string.

        return: String representation of Quantile transform.
        """
        return self.transformer.__str__()

    def fit(self, y):
        """
        Fit function for Quantile transform.

        :param y: The data used to scale along the features axis.
        :type y: numpy.ndarray or scipy.sparse.spmatrix
        :return: Object of QuantileTransformerWrapper.
        :rtype: azureml.automl.runtime.shared.model_wrappers.QuantileTransformerWrapper
        """
        try:
            self.transformer.fit(y.reshape(-1, 1))
        except Exception as e:
            raise FitException.from_exception(e, has_pii=True, target="QuantileTransformerWrapper"). \
                with_generic_msg(_generic_fit_error_message.format(self.__class__.__name__))
        return self

    def get_params(self, deep=True):
        """
        Return parameters of Quantile transform as dictionary.

        :param deep:
            If True, will return the parameters for this estimator
            and contained subobjects that are estimators.
        :type deep: bool
        :return: Dictionary of Quantile transform parameters.
        """
        return self.transformer.get_params(deep)

    def transform(self, y):
        """
        Transform function for Quantile transform.

        :param y: The data used to scale along the features axis.
        :type y: typing.Union[numpy.ndarray, scipy.sparse.spmatrix]
        :return: The projected data of Quantile transform.
        :rtype: typing.Union[numpy.ndarray, scipy.sparse.spmatrix]
        """
        try:
            return self.transformer.transform(y.reshape(-1, 1)).reshape(-1)
        except Exception as e:
            raise TransformException.from_exception(
                e, has_pii=True, target="QuantileTransformerWrapper",
                reference_code='model_wrappers.QuantileTransformerWrapper.transform'). \
                with_generic_msg(_generic_transform_error_message.format(self.__class__.__name__))

    def inverse_transform(self, y):
        """
        Inverse transform function for Quantile transform. Back-projection to the original space.

        :param y: The data used to scale along the features axis.
        :type y: numpy.ndarray or scipy.sparse.spmatrix
        :return: The projected data of Quantile inverse transform.
        :rtype: typing.Union[numpy.ndarray, scipy.sparse.spmatrix]
        """
        try:
            return self.transformer.inverse_transform(y.reshape(-1, 1)).reshape(-1)
        except Exception as e:
            raise TransformException.from_exception(
                e, has_pii=True, target="QuantileTransformerWrapper_Inverse",
                reference_code='model_wrappers.QuantileTransformerWrapper_Inverse.inverse_transform'). \
                with_generic_msg(_generic_transform_error_message.format(self.__class__.__name__))


class DropColumnsTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, columns_to_keep: Union[int, List[int]]):
        if not isinstance(columns_to_keep, list):
            self.columns_to_keep = [columns_to_keep]
        else:
            self.columns_to_keep = columns_to_keep
        arr = np.array(self.columns_to_keep, dtype=int)
        self.model = ColumnTransformer([("selectcolumn", "passthrough", arr)], remainder="drop")

    def fit(self, X: DataInputType, y: pd.Series) -> 'DropColumnsTransformer':
        # there is nothing to fit
        return self

    def transform(self, X: DataInputType) -> DataInputType:
        if self.columns_to_keep:
            return self.model.fit_transform(X)
        else:
            return X

    def get_params(self, deep=True):
        """
        Return parameters of DropColumnsTransformer as dictionary.

        :param deep:
            If True, will return the parameters for this estimator
            and contained subobjects that are estimators.
        :type deep: bool
        :return: Dictionary of drop columns transform parameters.
        """

        if deep:
            return self.model.get_params(deep)
        else:
            params = {}
            params["columns_to_keep"] = self.columns_to_keep
            return params


class IdentityTransformer(BaseEstimator, TransformerMixin):
    """
    Identity transformer class.

    Returns the same X it accepts.
    """

    def fit(self,
            X: np.ndarray,
            y: Optional[np.ndarray] = None) -> Any:
        """
        Take X and does nothing with it.

        :param X: Features to transform.
        :param y: Target values.
        :return: This transformer.
        """
        return self

    def transform(self,
                  X: np.ndarray,
                  y: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Perform the identity transform.

        :param X: Features to tranform.
        :param y: Target values.
        :return: The same X that was passed
        """
        return X


class LogTransformer(BaseEstimator, TransformerMixin):
    """
    Log transformer class.

    :param safe:
        If true, truncate values outside the transformer's
        domain to the nearest point in the domain.
    :type safe: bool
    :return: Object of class LogTransformer.

    """

    def __init__(self, safe=True):
        """
        Initialize function for Log transformer.

        :param safe:
            If true, truncate values outside the transformer's
            domain to the nearest point in the domain.
        :type safe: bool
        :return: Object of class LogTransformer.
        """
        self.base = np.e
        self.y_min = None
        self.scaler = None
        self.lower_range = 1e-5
        self.safe = safe

    def __repr__(self):
        return "{}(safe={})".format(self.__class__.__name__, self.safe)

    def __str__(self):
        """
        Return transformer details into string.

        return: string representation of Log transform.
        """
        return "LogTransformer(base=e, y_min=%.5f, scaler=%s, safe=%s)" % \
               (self.y_min if self.y_min is not None else 0,
                self.scaler,
                self.safe)

    def fit(self, y, y_min=None):
        """
        Fit function for Log transform.

        :param y: Input training data.
        :type y: numpy.ndarray
        :param y_min: Minimum value of y, will be inferred if not set
        :type y_min: float
        :return: Returns an instance of the LogTransformer model.
        """
        if y_min is None:
            self.y_min = np.min(y)
        else:
            if (y_min is not None) and y_min <= np.min(y):
                self.y_min = y_min
            else:
                self.y_min = np.min(y)
                warnings.warn(
                    'Caution: y_min greater than observed minimum in y')

        if self.y_min > self.lower_range:
            self.y_min = self.lower_range
            try:
                self.scaler = preprocessing.StandardScaler(
                    copy=False, with_mean=False,
                    with_std=False).fit(y.reshape(-1, 1))
            except Exception as e:
                raise FitException.from_exception(e, has_pii=True, target="LogTransformer"). \
                    with_generic_msg(_generic_fit_error_message.format(self.__class__.__name__))
        else:
            y_max = np.max(y)
            try:
                self.scaler = preprocessing.MinMaxScaler(
                    feature_range=(self.lower_range, 1)).fit(
                    np.array([y_max, self.y_min]).reshape(-1, 1))
            except Exception as e:
                raise FitException.from_exception(e, has_pii=True, target="LogTransformer"). \
                    with_generic_msg(_generic_fit_error_message.format(self.__class__.__name__))

        return self

    def get_params(self, deep=True):
        """
        Return parameters of Log transform as dictionary.

        :param deep:
            If True, will return the parameters for this estimator
            and contained subobjects that are estimators.
        :type deep: bool
        :return: Dictionary of Log transform parameters.
        """
        return {"base": self.base,
                "y_min": self.y_min,
                "scaler": self.scaler,
                "safe": self.safe
                }

    def return_y(self, y):
        """
        Return log value of y.

        :param y: Input data.
        :type y: numpy.ndarray
        :return: The log transform array.
        """
        return np.log(y)

    def transform(self, y):
        """
        Transform function for Log transform to return the log value.

        :param y: Input data.
        :type y: numpy.ndarray
        :return: The log transform array.
        """
        if self.y_min is None:
            raise UntrainedModelException.create_without_pii(target='LogTransformer')
        elif np.min(y) < self.y_min and \
                np.min(self.scaler.transform(
                    y.reshape(-1, 1)).reshape(-1, )) <= 0:
            if self.safe:
                warnings.warn("y_min greater than observed minimum in y, "
                              "clipping y to domain")
                y_copy = y.copy()
                y_copy[y < self.y_min] = self.y_min
                try:
                    return self.return_y(
                        self.scaler.transform(y_copy.reshape(-1, 1)).reshape(-1, ))
                except Exception as e:
                    raise TransformException.from_exception(
                        e, has_pii=True, target="LogTransformer",
                        reference_code='model_wrappers.LogTransformer.transform.y_min_greater'). \
                        with_generic_msg(_generic_transform_error_message.format(self.__class__.__name__))
            else:
                raise DataException._with_error(
                    AzureMLError.create(
                        TransformerYMinGreater, target="LogTransformer", transformer_name="LogTransformer"
                    )
                )
        else:
            try:
                return self.return_y(
                    self.scaler.transform(y.reshape(-1, 1)).reshape(-1, ))
            except Exception as e:
                raise TransformException.from_exception(
                    e, has_pii=True, target="LogTransformer",
                    reference_code='model_wrappers.LogTransformer.transform'). \
                    with_generic_msg(_generic_transform_error_message.format(self.__class__.__name__))

    def inverse_transform(self, y):
        """
        Inverse transform function for Log transform.

        :param y: Input data.
        :type y: numpy.ndarray
        :return: Inverse Log transform.
        """
        # this inverse transform has no restrictions, can exponetiate anything
        if self.y_min is None:
            raise UntrainedModelException.create_without_pii(target='LogTransformer')
        try:
            return self.scaler.inverse_transform(
                np.exp(y).reshape(-1, 1)).reshape(-1, )
        except Exception as e:
            raise TransformException.from_exception(
                e, has_pii=True, target='LogTransformer',
                reference_code='model_wrappers.LogTransformer.inverse_transform'). \
                with_generic_msg(_generic_transform_error_message.format(self.__class__.__name__))


class PowerTransformer(BaseEstimator, TransformerMixin):
    """
    Power transformer class.

    :param power: Power to raise y values to.
    :type power: float
    :param safe:
        If true, truncate values outside the transformer's domain to
        the nearest point in the domain.
    :type safe: bool
    """

    def __init__(self, power=1, safe=True):
        """
        Initialize function for Power transformer.

        :param power: Power to raise y values to.
        :type power: float
        :param safe:
            If true, truncate values outside the transformer's domain
            to the nearest point in the domain.
        :type safe: bool
        """
        # power = 1 is the identity transformation
        self.power = power
        self.y_min = None
        self.accept_negatives = False
        self.lower_range = 1e-5
        self.scaler = None
        self.safe = safe

        # check if the exponent is everywhere defined
        if self.power > 0 and \
                (((self.power % 2 == 1) or (1 / self.power % 2 == 1))
                 or (self.power % 2 == 0 and self.power > 1)):
            self.accept_negatives = True
            self.y_min = -np.inf
            self.offset = 0
            self.scaler = preprocessing.StandardScaler(
                copy=False, with_mean=False, with_std=False).fit(
                np.array([1], dtype=float).reshape(-1, 1))

    def __repr__(self):
        params = {
            "power": self.power,
            "safe": self.safe
        }

        return "{}({})".format(
            self.__class__.__name__,
            ", ".join(["{}={}".format(k, repr(params[k])) for k in params])
        )

    def __str__(self):
        """
        Return transformer details into string.

        return: String representation of Power transform.
        """
        return \
            "PowerTransformer(power=%.1f, y_min=%.5f, scaler=%s, safe=%s)" % (
                self.power,
                self.y_min if self.y_min is not None else 0,
                self.scaler,
                self.safe)

    def return_y(self, y, power, invert=False):
        """
        Return some 'power' of 'y'.

        :param y: Input data.
        :type y: numpy.ndarray
        :param power: Power value.
        :type power: float
        :param invert:
            A boolean whether or not to perform the inverse transform.
        :type invert: bool
        :return: The transformed targets.
        """
        # ignore invert, the power has already been inverted
        # can ignore invert because no offsetting has been done
        if self.accept_negatives:
            if np.any(y < 0):
                mult = np.sign(y)
                y_inter = np.multiply(np.power(np.absolute(y), power), mult)
            else:
                y_inter = np.power(y, power)
        else:
            # these are ensured to only have positives numbers as inputs
            y_inter = np.power(y, power)

        if invert:
            try:
                return self.scaler.inverse_transform(
                    y_inter.reshape(-1, 1)).reshape(-1, )
            except Exception as e:
                raise TransformException.from_exception(
                    e, has_pii=True, target="PowerTransformer",
                    reference_code='model_wrappers.PowerTransformer.return_y'). \
                    with_generic_msg(_generic_transform_error_message.format(self.__class__.__name__))
        else:
            return y_inter

    def get_params(self, deep=True):
        """
        Return parameters of Power transform as dictionary.

        :param deep:
            If True, will return the parameters for this estimator
            and contained subobjects that are estimators.
        :type deep: bool
        :return: Dictionary of Power transform parameters.
        """
        return {
            "power": self.power,
            "scaler": self.scaler,
            "y_min": self.y_min,
            "accept_negatives": self.accept_negatives,
            "safe": self.safe
        }

    def fit(self, y, y_min=None):
        """
        Fit function for Power transform.

        :param y: Input training data.
        :type y: numpy.ndarray
        :param y_min: Minimum value of y, will be inferred if not set.
        :type y_min: float
        :return: Returns an instance of the PowerTransformer model.
        """
        if y_min is None:
            self.y_min = np.min(y)
        else:
            if (y_min is not None) and y_min <= np.min(y):
                self.y_min = y_min
            else:
                self.y_min = np.min(y)
                warnings.warn(
                    'Caution: y_min greater than observed minimum in y')

        if self.y_min > self.lower_range:
            self.y_min = self.lower_range
            try:
                self.scaler = preprocessing.StandardScaler(
                    copy=False, with_mean=False,
                    with_std=False).fit(y.reshape(-1, 1))
            except Exception as e:
                raise FitException.from_exception(e, has_pii=True, target="PowerTransformer"). \
                    with_generic_msg(_generic_fit_error_message.format(self.__class__.__name__))
        else:
            y_max = np.max(y)
            try:
                self.scaler = preprocessing.MinMaxScaler(
                    feature_range=(self.lower_range, 1)).fit(
                    np.array([y_max, self.y_min]).reshape(-1, 1))
            except Exception as e:
                raise FitException.from_exception(e, has_pii=True, target="PowerTransformer"). \
                    with_generic_msg(_generic_fit_error_message.format(self.__class__.__name__))
        return self

    def transform(self, y):
        """
        Transform function for Power transform.

        :param y: Input data.
        :type y: numpy.ndarray
        :return: Power transform result.
        """
        if self.y_min is None and not (self.power > 0 and self.power % 2 == 1):
            raise UntrainedModelException.create_without_pii(target='PowerTransformer')
        elif np.min(y) < self.y_min and not self.accept_negatives and np.min(
                self.scaler.transform(y.reshape(-1, 1)).reshape(-1, )) <= 0:
            if self.safe:
                warnings.warn(
                    "y_min greater than observed minimum in y, clipping y to "
                    "domain")
                y_copy = y.copy()
                y_copy[y < self.y_min] = self.y_min
                try:
                    return self.return_y(
                        self.scaler.transform(y_copy.reshape(-1, 1)).reshape(-1, ),
                        self.power, invert=False)
                except Exception as e:
                    raise TransformException.from_exception(
                        e, has_pii=True, target="PowerTransformer",
                        reference_code='model_wrappers.PowerTransformer.transform.y_min_greater'). \
                        with_generic_msg(_generic_transform_error_message.format(self.__class__.__name__))
            else:
                raise DataException._with_error(
                    AzureMLError.create(
                        TransformerYMinGreater, target="PowerTransformer", transformer_name="PowerTransformer"
                    )
                )
        else:
            try:
                return self.return_y(
                    self.scaler.transform(y.reshape(-1, 1)).reshape(-1, ),
                    self.power, invert=False)
            except Exception as e:
                raise TransformException.from_exception(
                    e, has_pii=True, target="PowerTransformer",
                    reference_code='model_wrappers.PowerTransformer.transform'). \
                    with_generic_msg(_generic_transform_error_message.format(self.__class__.__name__))

    def inverse_transform(self, y):
        """
        Inverse transform function for Power transform.

        :param y: Input data.
        :type y: numpy.ndarray
        :return: Inverse Power transform result.
        """
        if self.y_min is None and \
                not (self.power > 0 and self.power % 2 == 1):
            raise UntrainedModelException.create_without_pii(target="PowerTransformer")
        elif not self.accept_negatives and np.min(y) <= 0:
            if self.safe:
                warnings.warn(
                    "y_min greater than observed minimum in y, clipping y to "
                    "domain")
                transformed_min = np.min(y[y > 0])
                y_copy = y.copy()
                y_copy[y < transformed_min] = transformed_min
                return self.return_y(y_copy, 1 / self.power, invert=True)
            else:
                raise DataException._with_error(
                    AzureMLError.create(PowerTransformerInverseTransform, target="PowerTransformer")
                )
        else:
            return self.return_y(y, 1 / self.power, invert=True)


class BoxCoxTransformerScipy(BaseEstimator, TransformerMixin):
    """
    Box Cox transformer class for normalizing non-normal data.

    :param lambda_val:
        Lambda value for Box Cox transform, will be inferred if not set.
    :type lambda_val: float
    :param safe:
        If true, truncate values outside the transformer's domain to
        the nearest point in the domain.
    :type safe: bool
    """

    def __init__(self, lambda_val=None, safe=True):
        """
        Initialize function for Box Cox transformer.

        :param lambda_val:
            Lambda value for Box Cox transform, will be inferred if not set.
        :type lambda_val: float
        :param safe:
            If true, truncate values outside the transformer's domain
            to the nearest point in the domain.
        :type safe: bool
        """
        # can also use lambda_val = 0 as equivalent to natural log transformer
        self.lambda_val = lambda_val
        self.lower_range = 1e-5
        self.y_min = None
        self.scaler = None
        self.fitted = False
        self.safe = safe

    def get_params(self, deep: bool = True) -> Dict[str, Any]:
        return {
            "lambda_val": self.lambda_val,
            "safe": self.safe
        }

    def __repr__(self):
        params = self.get_params(deep=False)
        return _codegen_utilities.generate_repr_str(self.__class__, params)

    def __str__(self):
        """
        Return transformer details into string.

        return: String representation of Box Cox transform.
        """
        return ("BoxCoxTransformer(lambda=%.3f, y_min=%.5f, scaler=%s, "
                "safe=%s)" %
                (self.lambda_val if self.lambda_val is not None else 0,
                 self.y_min if self.y_min is not None else 0,
                 self.scaler,
                 self.safe))

    def fit(self, y, y_min=None):
        """
        Fit function for Box Cox transform.

        :param y: Input training data.
        :type y: numpy.ndarray
        :param y_min: Minimum value of y, will be inferred if not set.
        :type y_min: float
        :return: Returns an instance of the BoxCoxTransformerScipy model.
        """
        self.fitted = True
        if y_min is None:
            self.y_min = np.min(y)
        else:
            if (y_min is not None) and y_min <= np.min(y):
                self.y_min = y_min
            else:
                self.y_min = np.min(y)
                warnings.warn(
                    'Caution: y_min greater than observed minimum in y')
        if self.y_min > self.lower_range:
            self.y_min = self.lower_range
            try:
                self.scaler = preprocessing.StandardScaler(
                    copy=False,
                    with_mean=False,
                    with_std=False).fit(y.reshape(-1, 1))
            except Exception as e:
                raise FitException.from_exception(e, has_pii=True, target="BoxCoxTransformer"). \
                    with_generic_msg(_generic_fit_error_message.format(self.__class__.__name__))
        else:
            y_max = np.max(y)
            try:
                self.scaler = preprocessing.MinMaxScaler(
                    feature_range=(self.lower_range, 1)).fit(
                    np.array([y_max, self.y_min]).reshape(-1, 1))
            except Exception as e:
                raise FitException.from_exception(e, has_pii=True, target="BoxCoxTransformer"). \
                    with_generic_msg(_generic_fit_error_message.format(self.__class__.__name__))

        # reset if already fitted
        if self.lambda_val is None or self.fitted:
            try:
                y, self.lambda_val = boxcox(
                    self.scaler.transform(y.reshape(-1, 1)).reshape(-1, ))
            except Exception as e:
                raise TransformException.from_exception(
                    e, has_pii=True, target="BoxCoxTransformer",
                    reference_code='model_wrappers.BoxCoxTransformer.fit'). \
                    with_generic_msg(_generic_transform_error_message.format(self.__class__.__name__))
        return self

    def transform(self, y):
        """
        Transform function for Box Cox transform.

        :param y: Input data.
        :type y: numpy.ndarray
        :return: Box Cox transform result.
        """
        if self.lambda_val is None:
            raise UntrainedModelException.create_without_pii(target="BoxCoxTransformer")
        elif np.min(y) < self.y_min and \
                np.min(
                    self.scaler.transform(y.reshape(-1, 1)).reshape(-1, )) <= 0:
            if self.safe:
                warnings.warn("y_min greater than observed minimum in y, "
                              "clipping y to domain")
                y_copy = y.copy()
                y_copy[y < self.y_min] = self.y_min
                try:
                    return boxcox(
                        self.scaler.transform(y_copy.reshape(-1, 1)).reshape(-1, ),
                        self.lambda_val)
                except Exception as e:
                    raise TransformException.from_exception(
                        e, has_pii=True, target="BoxCoxTransformer",
                        reference_code='model_wrappers.BoxCoxTransformer.transform.y_min_greater'). \
                        with_generic_msg(_generic_transform_error_message.format(self.__class__.__name__))
            else:
                raise DataException._with_error(
                    AzureMLError.create(
                        TransformerYMinGreater, target="BoxCoxTransformer", transformer_name="BoxCoxTransformer"
                    )
                )
        else:
            try:
                return boxcox(
                    self.scaler.transform(y.reshape(-1, 1)).reshape(-1, ),
                    self.lambda_val)
            except Exception as e:
                raise TransformException.from_exception(
                    e, has_pii=True, target="BoxCoxTransformer",
                    reference_code='model_wrappers.BoxCoxTransformer.transform'). \
                    with_generic_msg(_generic_transform_error_message.format(self.__class__.__name__))

    def inverse_transform(self, y):
        """
        Inverse transform function for Box Cox transform.

        :param y: Input data.
        :type y: numpy.ndarray
        :return: Inverse Box Cox transform result.
        """
        # inverse box_cox can take any number
        if self.lambda_val is None:
            raise UntrainedModelException.create_without_pii(target="BoxCoxTransformer_Inverse")
        else:
            try:
                return self.scaler.inverse_transform(
                    inv_boxcox(y, self.lambda_val).reshape(-1, 1)).reshape(-1, )
            except Exception as e:
                raise TransformException.from_exception(
                    e, has_pii=True, target="BoxCoxTransformer_Inverse",
                    reference_code='model_wrappers.BoxCoxTransformerScipy.inverse_transform'). \
                    with_generic_msg(_generic_transform_error_message.format(self.__class__.__name__))


class GPUHelper(object):
    """Helper class for adding GPU support."""

    @staticmethod
    def xgboost_add_gpu_support(problem_info, xgboost_args):
        """Add GPU for XGBOOST."""
        if problem_info is not None and problem_info.gpu_training_param_dict is not None and \
                problem_info.gpu_training_param_dict.get("processing_unit_type", "cpu") == "gpu":
            if xgboost_args.get('tree_method') == 'hist':
                xgboost_args['tree_method'] = 'gpu_hist'

                # to make sure user can still use cpu machine for inference
                xgboost_args['predictor'] = 'cpu_predictor'
        return xgboost_args

    @staticmethod
    def lightgbm_add_gpu_support(problem_info, lightgbm_params):
        """Add GPU for LigtGBM."""
        if problem_info is not None and problem_info.gpu_training_param_dict is not None and \
                problem_info.gpu_training_param_dict.get("processing_unit_type", "cpu") == "gpu":
            logger.info("turning on usage of gpu device")
            lightgbm_params['device'] = 'gpu'

            # We have seen lightgbm gpu fit can fail on bin size too big, the bin size during fit may come from
            # dataset / the pipeline spec itself. With one hot encoding, the categorical features from dataset should
            # not have big cardinality that causing the bin size too big, so the only source is pipeline itself. Cap to
            # 255 max if it exceeded the size.
            if lightgbm_params.get('max_bin', 0) > 255:
                logger.info("limiting max_bin to 255")
                lightgbm_params['max_bin'] = 255
        return lightgbm_params


class LightGbmHelper:

    @staticmethod
    def set_dask_lightgbm_advanced_params(init_args, problem_info):
        TREE_LEARNER = "tree_learner"

        logger.info("Lightgbm is being fed with following data size --  samples={} and features={}".format(
            problem_info.dataset_samples,
            problem_info.dataset_features))

        # if we have more than 200 columns we consider it as wide
        # https://lightgbm.readthedocs.io/en/latest/Parallel-Learning-Guide.html
        if problem_info.dataset_features > 200:
            init_args[TREE_LEARNER] = "voting"
            logger.info("using voting parallel lightgbm")
        else:
            init_args[TREE_LEARNER] = "data"
            logger.info("using data parallel lightgbm")

        min_child_samples_percentage = 0
        if 'min_child_samples' in init_args:
            min_child_samples_percentage = init_args['min_child_samples']
            del init_args['min_child_samples']
        if 'min_data_in_leaf' in init_args:
            min_child_samples_percentage = init_args['min_data_in_leaf']
            del init_args['min_data_in_leaf']

        if min_child_samples_percentage > 0 and min_child_samples_percentage < 1:
            # Current miro recommendation for min_child_samples/min_data_in_leaf is not tuned for large data as it
            # frequently results in 'histogram build' failures. Hence we reduce by factor of 10
            min_samples = int(min_child_samples_percentage * problem_info.dataset_samples * 0.1) + 1
            init_args['min_child_samples'] = min_samples
            logger.warning("Altered the suggested value for min_child_samples. New value is {}".format(min_samples))

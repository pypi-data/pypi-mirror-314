# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Definitions for regression metrics."""
from azureml.training.tabular.score._regression import (
    RegressionMetric,
    ExplainedVariance,
    R2,
    Spearman,
    MAPE,
    MeanAbsoluteError,
    NormMeanAbsoluteError,
    MedianAbsoluteError,
    NormMedianAbsoluteError,
    RMSLE,
    NormRMSLE,
    RMSE,
    NormRMSE,
    Residuals,
    PredictedTrue,
    _mape,
    _smape
)

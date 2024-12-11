# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Validation for AutoML metrics."""
from azureml.training.tabular.score._validation import (
    validate_classification,
    log_classification_debug,
    validate_regression,
    log_regression_debug,
    validate_forecasting,
    log_forecasting_debug,
    _check_arrays_first_dim,
    convert_decimal_to_float,
    _check_array_values,
    _check_array_type,
    _check_arrays_same_type,
    _check_dim,
    format_1d,
    log_failed_splits
)

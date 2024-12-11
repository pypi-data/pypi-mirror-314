# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utilities used to infer auto features."""
from azureml.training.tabular.featurization.timeseries.forecasting_heuristic_utils import (
    STL_DECOMPOSITION_ERROR,
    PACF_ERROR,
    STRONG_SEASONALITY,
    DUPLICATED_INDEX,
    CANNOT_DETECT_FREQUENCY,
    get_heuristic_max_horizon,
    get_frequency_safe,
    timedelta_to_freq_safe,
    frequency_based_lags,
    _get_seconds_from_hour_offset_maybe,
    _log_warn_maybe,
    analyze_pacf_one_grain,
    analyze_pacf_per_grain,
    auto_cv_one_series,
    auto_cv_per_series,
    try_get_auto_parameters
)

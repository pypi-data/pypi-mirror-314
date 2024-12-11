# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Decompose the target value to the Trend and Seasonality."""
from azureml.training.tabular.featurization.timeseries.stl_featurizer import (
    STLFeaturizer,
    _sm_is_ver9,
    _complete_short_series,
    _extend_series_for_sm9_bug,
    TimeSeriesDataSet
)

# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Generic utility functions for the AML forecasting package."""
from azureml.training.tabular.timeseries.forecasting_utilities import (
    ForecastingUtilConstants,
    get_period_offsets_from_dates,
    grain_level_to_dict,
    make_groupby_map,
    flatten_list,
    _range,
    invert_dict_of_lists,
    array_equal_with_nans,
    get_pipeline_step,
    is_iterable_but_not_string,
    subtract_list_from_list
)

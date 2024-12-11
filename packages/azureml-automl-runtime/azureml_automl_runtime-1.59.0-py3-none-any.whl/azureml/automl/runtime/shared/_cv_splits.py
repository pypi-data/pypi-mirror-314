# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Class for processing cross validation strategies for datasets."""
from typing import Any, cast, Iterable, List, Optional

import logging
import numpy as np
import pandas as pd
import uuid

from functools import reduce

from azureml._common._error_definition import AzureMLError
from azureml._common._error_definition.user_error import BadArgument, ArgumentBlankOrEmpty, ArgumentOutOfRange
from azureml.automl.core.shared._diagnostics.automl_error_definitions import InvalidArgumentType, \
    FeatureUnsupportedForIncompatibleArguments, ConflictingValueForArguments
from azureml.automl.core.shared._diagnostics.contract import Contract
from sklearn import model_selection
from azureml.automl.core.shared import constants, logging_utilities
from azureml.automl.core.shared.exceptions import ConfigException, DataException
from azureml.automl.core.shared.logging_utilities import function_debug_log_wrapped
from azureml.automl.runtime.shared import memory_utilities
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.runtime.shared.rolling_origin_validator import RollingOriginValidator
from azureml.automl.runtime._time_series_data_set import TimeSeriesDataSet
from azureml.training.tabular.score._cv_splits import (
    _CVSplits,
    _CVType,
    FeaturizedCVSplit,
    FeaturizedTrainValidTestSplit
)

logger = logging.getLogger(__name__)

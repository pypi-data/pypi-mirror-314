# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""The extended imputer converter."""
import sys

import numpy as np

from sklearn.base import clone
from sklearn.impute import SimpleImputer
from azureml.automl.core.onnx_convert.onnx_convert_constants import OnnxConvertConstants
from azureml.automl.runtime.onnx_convert.operator_converters._abstract_operator_converter import (
    _AbstractOperatorConverter)


# Import the onnx related packages, only if the python version is compatible.
if sys.version_info < OnnxConvertConstants.OnnxIncompatiblePythonVersion:
    from onnxconverter_common.data_types import Int64TensorType
    from skl2onnx._supported_operators import update_registered_converter
    from skl2onnx.common._topology import Operator, Scope
    from skl2onnx.common._container import ModelComponentContainer
    from skl2onnx.shape_calculators.imputer import calculate_sklearn_imputer_output_shapes
    from skl2onnx.operator_converters.imputer_op import convert_sklearn_imputer


class ImputerConverter(_AbstractOperatorConverter):
    """The imputer with support of int64 values."""

    def __init__(self):
        """Construct the imputer op converter with support of Int64 conversion."""
        type(self).OPERATOR_ALIAS = 'AutomlImputer'

    def setup(self):
        """Set up the converter."""
        update_registered_converter(SimpleImputer,
                                    ImputerConverter.OPERATOR_ALIAS,
                                    calculate_sklearn_imputer_output_shapes,
                                    ImputerConverter._convert_automl_imputer)

    @staticmethod
    def _convert_automl_imputer(scope: Scope, operator: Operator, container: ModelComponentContainer) -> None:
        """
        Do the actual conversion.

        :param scope: The scope, where the operator will be defined.
        :param operator: The operator to be converted.
        :param container: The container operator will be added.
        """
        if isinstance(operator.inputs[0].type, Int64TensorType):
            # Even though the calculations were done on integer columns, scikit learn statistics
            # are calculated as floats. This results in failure during conversion. To avoid this
            # issue, we are replacing statistics by rounded integer.
            # Create unfitted operator to avoid modi
            imputer = clone(operator.raw_operator)
            # "fit" the operator
            if hasattr(operator.raw_operator, 'indicator_'):
                setattr(imputer, 'indicator_', operator.raw_operator.indicator_)
            if operator.raw_operator.fill_value is not None:
                imputer.fill_value = np.round(operator.raw_operator.fill_value)
            if hasattr(operator.raw_operator, 'statistics_'):
                imputer.statistics_ = np.round(operator.raw_operator.statistics_)
            operator.raw_operator = imputer
        convert_sklearn_imputer(scope, operator, container)

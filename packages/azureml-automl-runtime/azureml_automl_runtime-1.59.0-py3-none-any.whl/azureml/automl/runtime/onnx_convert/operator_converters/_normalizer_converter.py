# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import sys

import numpy as np

from sklearn.preprocessing import Normalizer
from azureml.automl.core.onnx_convert.onnx_convert_constants import OnnxConvertConstants
from azureml.automl.runtime.onnx_convert.operator_converters._abstract_operator_converter import (
    _AbstractOperatorConverter)


# Import the onnx related packages, only if the python version is compatible.
if sys.version_info < OnnxConvertConstants.OnnxIncompatiblePythonVersion:
    from onnxconverter_common.data_types import Int64TensorType
    from onnxconverter_common.onnx_ops import apply_div
    from skl2onnx._supported_operators import update_registered_converter
    from skl2onnx.common._topology import Operator, Scope
    from skl2onnx.common._container import ModelComponentContainer
    from skl2onnx.shape_calculators.scaler import calculate_sklearn_scaler_output_shapes
    from skl2onnx.operator_converters.common import concatenate_variables
    from skl2onnx.operator_converters.normaliser import convert_sklearn_normalizer


class NormalizerConverter(_AbstractOperatorConverter):
    """
    Fixed version of Normalizer.

    This class corrects for the issue about incorrect normalization in ONNX runtime in case
    of normalization by maximal value. When calculating maximal value for
    normalization ONNX runtime takes just maximal value, while scikit-learn takes "
    absolute maximal value. In the code below we are taking the absolute maximal value.
    https://github.com/microsoft/onnxruntime/issues/16451
    """

    def __init__(self):
        """Construct the noralizer which correctly supports """
        type(self).OPERATOR_ALIAS = 'FixedNormalizer'

    def setup(self):
        """Set up the converter."""
        update_registered_converter(Normalizer,
                                    NormalizerConverter.OPERATOR_ALIAS,
                                    calculate_sklearn_scaler_output_shapes,
                                    NormalizerConverter._convert_normalizer)

    @staticmethod
    def _convert_normalizer(scope: Scope, operator: Operator, container: ModelComponentContainer) -> None:
        """
        Do the actual conversion.

        :param scope: The scope, where the operator will be defined.
        :param operator: The operator to be converted.
        :param container: The container operator will be added.
        """
        if operator.raw_operator.norm != 'max':
            convert_sklearn_normalizer(scope, operator, container)
        else:
            # Do the correction for normalization by max.
            if len(operator.inputs) > 1:
                # If there are multiple input tensors,
                # we combine them using a FeatureVectorizer
                feature_name = concatenate_variables(scope, operator.inputs, container)
            else:
                # No concatenation is needed, we just use the first variable's name
                feature_name = operator.inputs[0].full_name
            norm = scope.get_unique_variable_name('norm')
            norm_abs = scope.get_unique_variable_name('norm_abs')
            container.add_node(
                'Abs', feature_name, norm_abs,
                name=scope.get_unique_operator_name('Abs'))
            container.add_node(
                'ReduceMax', norm_abs, norm, axes=[1], keepdims=1,
                name=scope.get_unique_operator_name('ReduceMax'))
            apply_div(
                scope, [feature_name, norm], operator.outputs[0].full_name, container,
                operator_name=scope.get_unique_operator_name('MaxNormalizerNorm'))

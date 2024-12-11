# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""ImputationMarker operator converter."""
import numbers
import numpy as np
import six


import sys
import azureml.automl.core.onnx_convert
from azureml.automl.core.onnx_convert.onnx_convert_constants import OnnxConvertConstants
from onnxconverter_common.data_types import Int64TensorType
# Import the onnx related packages, only if the python version is compatible.
if sys.version_info < OnnxConvertConstants.OnnxIncompatiblePythonVersion:
    from skl2onnx.proto import onnx_proto
    from skl2onnx.common.data_types import Int64TensorType
    from skl2onnx.common.data_types import FloatTensorType
    from skl2onnx.common.data_types import StringTensorType
    from skl2onnx.common.data_types import DictionaryType
    from skl2onnx.common.data_types import SequenceType

    from skl2onnx.common._apply_operation import apply_cast, apply_identity, apply_reshape, apply_mul
    from skl2onnx.common.utils import check_input_and_output_types, check_input_and_output_numbers
    from skl2onnx.common.utils_classifier import _finalize_converter_classes
    from skl2onnx import update_registered_converter

# AutoML modules.
from azureml.automl.core.shared.exceptions import OnnxConvertException    # noqa: E402
from ._abstract_operator_converter import _AbstractOperatorConverter    # noqa: E402

import sklearn    # noqa: E402
from sklearn.base import BaseEstimator, ClassifierMixin    # noqa: E402


class _YTransformLabelEncoder(BaseEstimator, ClassifierMixin):
    """
    Virtual operator for converting the y transformer LabelEncoder.

    Containing the actual label encoder to do the y transform.
    This class is used by convert the y transformers.
    Since the object of this class needs to be put into last step of
    the reconstructed pipeline, it inherits the BaseEstimator and ClassifierMixin.
    But it's a dummy estimator, and only used for onnx conversion.
    """

    def __init__(self, le):
        """
        Construct the Virtual operator.

        :param le: The raw original operator.
        """
        self.label_encoder = le


class YTransformerLabelEncoderConverter(_AbstractOperatorConverter):
    """Y Transformer LabelEncoder operator converter."""

    def __init__(self):
        """Construct the Y Transformer LabelEncoder operator converter."""
        type(self).OPERATOR_ALIAS = 'AutoMLYTransLabelEncoder'

    def setup(self):
        """Set up the converter."""
        update_registered_converter(_YTransformLabelEncoder,
                                    YTransformerLabelEncoderConverter.OPERATOR_ALIAS,
                                    YTransformerLabelEncoderConverter._calc_y_trans_labelencoder_output_shapes,
                                    YTransformerLabelEncoderConverter._convert_automl_y_trans_labelencoder)

    @staticmethod
    def _calc_y_trans_labelencoder_output_shapes(operator):
        N = operator.inputs[0].type.shape[0]
        class_labels = operator.raw_operator.classes_
        if all(isinstance(i, np.ndarray) for i in class_labels):
            class_labels = np.concatenate(class_labels)

        if all(isinstance(i, np.ndarray) for i in class_labels):
            class_labels = np.concatenate(class_labels)
        if all(isinstance(i, (six.string_types, six.text_type)) for i in class_labels):
            operator.outputs[0].type = StringTensorType(shape=[N])
        elif all(isinstance(i, (numbers.Real)) for i in class_labels):
            operator.outputs[0].type = FloatTensorType(shape=[N])
        else:
            # For other types we treat the class labels as string.
            operator.outputs[0].type = StringTensorType(shape=[N])

        if len(operator.inputs) > 0:
            operator.outputs[1].type = operator.inputs[1].type

    @staticmethod
    def _convert_automl_y_trans_labelencoder(scope, operator, container):
        """
        Convert the reverse Y transformer into LabelEncoder.

        We have to write this conerter as regular label encoder encodes Any
        to int64. ONNX encoder can do the conversion based of keys_*
        and values_* attributes. The key is an input, the value is an output.
        :param scope: The scope of operator
        :param operator: The operator to be converted.
        :param container: The container foroperator.
        """
        op = operator.raw_operator
        op_type = OnnxConvertConstants.LabelEncoder
        attrs = {'name': scope.get_unique_operator_name(op_type)}
        # Set the inputs.
        if isinstance(operator.inputs[0].type, FloatTensorType):
            attrs['keys_floats'] = [float(i) for i in range(len(op.classes_))]
        elif isinstance(operator.inputs[0].type, Int64TensorType):
            attrs['keys_int64s'] = [i for i in range(len(op.classes_))]
        else:
            attrs['keys_strings'] = [str(i) for i in range(len(op.classes_))]
        classes = op.classes_
        # Set the outputs.
        if np.issubdtype(classes.dtype, np.floating):
            attrs['values_floats'] = classes
        elif np.issubdtype(classes.dtype, np.signedinteger):
            attrs['values_int64s'] = classes
        elif classes.dtype == np.bool_:
            # If we are dealing with booleans, we want to convert
            # it to string value.
            attrs['values_strings'] = [str(c) for c in op.classes_]
        else:
            attrs['values_strings'] = classes
        attrs['default_string'] = '__unknown__'

        # By default this label encoder output is string type, cast to float if needed.
        need_cast = False
        cast_to_type = None
        if isinstance(operator.outputs[0].type, FloatTensorType):
            lbl_out = scope.get_unique_variable_name('lbl_out')
            need_cast = True
            cast_to_type = onnx_proto.TensorProto.FLOAT
        else:
            lbl_out = operator.outputs[0].full_name

        container.add_node(op_type, operator.inputs[0].full_name,
                           lbl_out, op_domain=OnnxConvertConstants.OnnxMLDomain,
                           **attrs)
        if need_cast:
            apply_cast(scope, lbl_out, operator.outputs[0].full_name, container, to=cast_to_type)

        if len(operator.inputs) > 0:
            apply_identity(scope, operator.inputs[1].full_name, operator.outputs[1].full_name, container)

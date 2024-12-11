# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Base abstract operator converter."""
from abc import ABC, abstractmethod
import sys

from azureml.automl.core.shared.exceptions import OnnxConvertException
from azureml.automl.core.onnx_convert.onnx_convert_constants import OnnxConvertConstants

# Import the onnx related packages, only if the python version is compatible.
if sys.version_info < OnnxConvertConstants.OnnxIncompatiblePythonVersion:
    from onnxconverter_common.onnx_ops import apply_cast
    from skl2onnx import proto


class _AbstractOperatorConverter(ABC):
    """Abstract base class for the operator converters."""

    # Operator alias used by the upper level code, a static base property.
    # Subclasses should override this value in there constructor.
    OPERATOR_ALIAS = '__InvalidAlias__'

    def get_alias(self):
        """
        Get the converter's alias.

        :return: The operator alias of instance of subclasses.
        """
        converter_tp = type(self)
        alias = self.OPERATOR_ALIAS
        # Check if the alias is valid or not.
        if alias == _AbstractOperatorConverter.OPERATOR_ALIAS:
            msg = 'Invalid Operator Alias "{0}" assigned in operator converter class {1}'
            raise OnnxConvertException(msg.format(alias, converter_tp),
                                       reference_code="_abstract_operator_converter."
                                                      "_AbstractOperatorConverter.get_alias")\
                .with_generic_msg(msg.format("[MASKED]", "[MASKED]"))
        return alias

    @abstractmethod
    def setup(self):
        """Abstract method for setting up the converter."""
        raise NotImplementedError

    @staticmethod
    def convert_integer_to_float(variable, scope, container):
        """
        Convert integer opetator to float and return the new name.

        :param variable: The variable to be converted.
        :param scope: The scope variable belongs to.
        :param container: The container variable belongs to.
        """
        new_name = scope.get_unique_variable_name('cast')
        apply_cast(scope, variable.full_name, new_name,
                   container, to=proto.onnx_proto.TensorProto.FLOAT)
        return new_name

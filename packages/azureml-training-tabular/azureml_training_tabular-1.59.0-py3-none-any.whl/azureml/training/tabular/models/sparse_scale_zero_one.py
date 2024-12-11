# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""SparseScaleZeroOne"""
import sklearn
from sklearn.base import BaseEstimator, TransformerMixin

from azureml._base_sdk_common._docstring_wrapper import experimental

from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    GenericFitError, GenericTransformError)
from azureml.automl.core.shared.exceptions import (
    FitException, UntrainedModelException, TransformException
)
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from ._abstract_model_wrapper import _AbstractModelWrapper


@experimental
class SparseScaleZeroOne(BaseEstimator, TransformerMixin, _AbstractModelWrapper):
    """Transforms the input data by appending previous rows."""

    def __init__(self):
        """Initialize Sparse Scale Transformer."""
        super().__init__()
        self.scaler = None
        self.model = None

    def get_model(self):
        """
        Return Sparse Scale model.

        :return: Sparse Scale model.
        """
        return self.model

    def fit(self, X, y=None):
        """
        Fit function for Sparse Scale model.

        :param X: Input data.
        :type X: scipy.sparse.spmatrix
        :param y: Input target values.
        :type y: numpy.ndarray
        :return: Returns self after fitting the model.
        """
        self.model = sklearn.preprocessing.MaxAbsScaler()
        try:
            self.model.fit(X)
            return self
        except Exception as e:
            raise FitException._with_error(
                AzureMLError.create(
                    GenericFitError, target="SparseScaleZeroOne", transformer_name=self.__class__.__name__,
                    has_pii=True,
                ), inner_exception=e) from e

    def transform(self, X):
        """
        Transform function for Sparse Scale model.

        :param X: Input data.
        :type X: scipy.sparse.spmatrix
        :return: Transformed output of MaxAbsScaler.
        """
        if self.model is None:
            raise UntrainedModelException(target=SparseScaleZeroOne, has_pii=False)
        try:
            X = self.model.transform(X)
        except Exception as e:
            raise TransformException._with_error(
                AzureMLError.create(
                    GenericTransformError, target="SparseScaleZeroOne", transformer_name=self.__class__.__name__,
                    has_pii=True,
                ), inner_exception=e) from e
        X.data = (X.data + 1) / 2
        return X

    def get_params(self, deep=True):
        """
        Return parameters for Sparse Scale model.

        :param deep:
            If True, will return the parameters for this estimator
            and contained subobjects that are estimators.
        :type deep: bool
        :return: Parameters for Sparse Scale model.
        """
        return {}

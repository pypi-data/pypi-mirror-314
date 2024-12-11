# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Target Type Transformer"""
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
from typing import Any
from azureml.automl.core.constants import PredictionTransformTypes
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared.reference_codes import ReferenceCodes


class TargetTypeTransformer(BaseEstimator, TransformerMixin):

    """Target Type Transformer class for post-processing the target column."""

    def __init__(self, target_type: str) -> None:
        """
        Constructor for TargetTypeTransformer.

        :param target_type:
            Prediction Transform Type to be used for casting the target column.
        :type target_type: str
        :return: Object of class TargetTypeTransformer.
        """
        self.target_type = target_type

    def fit(self, y: np.ndarray) -> 'TargetTypeTransformer':
        """
        Fit function for Target Type transform.

        :param y: Input training data.
        :type y: numpy.ndarray
        :return: Returns an instance of the TargetTypeTransformer model.
        """
        return self

    def transform(self, y: np.ndarray) -> np.ndarray:
        """
        Transform function for Target Type transform.

        :param y: Input data.
        :type y: numpy.ndarray
        :return: TargetType transform result.
        """
        return y

    def inverse_transform(self, y_pred: np.ndarray, convert_type=False, *args: Any, **kwargs: Any) -> np.ndarray:
        """
        Inverse transform function for TargetType transform.

        :param y_pred: Input data.
        :type y_pred: numpy.ndarray
        :param convert_type: If true, convert type of return value to integer, otherwise just round
                             the value. Note: conversion of np.nan to integer results in big numbers.
        :param args: Not in use.
        :param kwargs: Not in use.
        :return: Inverse TargetType transform result.
        """
        Contract.assert_type(convert_type, 'convert_type', bool,
                             reference_code=ReferenceCodes._TARGET_TYPE_WRONG_CONV_TYPE, log_safe=True)
        if (self.target_type == PredictionTransformTypes.INTEGER):
            y_pred = y_pred.round()
            if convert_type:
                y_pred = y_pred.astype(int)
        # No need to force float casting since default target column type is float.
        return y_pred

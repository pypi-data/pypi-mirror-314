# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""DifferencingYTransformer model"""
from typing import Optional, Dict
import numpy as np
import pandas as pd
import sklearn
import sklearn.pipeline
from typing import TYPE_CHECKING
from azureml._base_sdk_common._docstring_wrapper import experimental
from .._types import GrainType


# NOTE:
# Here we import type checking only for type checking time.
# during runtime TYPE_CHECKING is set to False.
if TYPE_CHECKING:
    from azureml.automl.runtime.featurizer.transformer.timeseries.timeseries_transformer import TimeSeriesTransformer


@experimental
class YPipelineTransformer(sklearn.pipeline.Pipeline):

    """
    YPipeline Transformer class for y_transformers.

    :param pipeline: Pipeline of y_transformers.
    :type pipeline: sklearn.pipeline.Pipeline
    :return: Object of class YPipelineTransformer.
    """

    def __init__(self, pipeline: sklearn.pipeline.Pipeline) -> None:
        """
        Initialize YPipelineTransformer class.
        """
        self.pipeline = pipeline
        super().__init__(self.pipeline.steps, memory=self.pipeline.memory)
        self.steps = pipeline.__dict__.get("steps")

    def fit(self, y: np.ndarray) -> 'YPipelineTransformer':
        """
        Fit function for YPipeline Transformer.

        :param y: Input training data.
        :type y: numpy.ndarray
        :return: Returns an instance of the YPipelineTransformer model.
        """
        return self

    def transform(self, y: np.ndarray) -> np.ndarray:
        """
        Transform function for YPipeline Transformer.

        :param y: Input data.
        :type y: numpy.ndarray
        :return: YPipelineTransformer result.
        """
        for _, tf in self.steps:
            y = tf.transform(y)
        return y

    def inverse_transform(self, y_pred: np.ndarray, x_test: Optional[pd.DataFrame] = None,
                          y_train: Optional[np.ndarray] = None, x_train: Optional[pd.DataFrame] = None,
                          timeseries_transformer: 'Optional[TimeSeriesTransformer]' = None,
                          last_known: Dict[GrainType, pd.Series] = {}) -> np.ndarray:
        """
        Inverse transform function for YPipeline pipeline.

        :param y_pred: Prediction target values.
        :type y_pred: numpy.ndarray
        :param x_test: Input test data.
        :type x_test: pandas.DataFrame
        :param y_train: Input train target values.
        :type y_train: numpy.ndarray
        :param x_train: Input train data.
        :type x_train: pandas.DataFrame
        :param timeseries_transformer: Timeseries Transformer for forecasting task.
        :type timeseries_transformer: azureml.automl.runtime.featurizer.transformer.timeseries.\
            timeseries_transformer.TimeSeriesTransformer
        :param last_known: last known date as a reference.
        :type last_known: Dict[GrainType, pd.Series]
        :return: Inverse YPipelineTransformer result.
        """
        for _, tf in self.steps:
            y_pred = tf.inverse_transform(y_pred, x_test=x_test,
                                          y_train=y_train, x_train=x_train,
                                          timeseries_transformer=timeseries_transformer,
                                          last_known=last_known)
        return y_pred

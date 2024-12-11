# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""DifferencingYTransformer model"""
import copy
from typing import List, Optional, cast, Tuple, Dict
import numpy as np
import logging
import pandas as pd
import sklearn
import sklearn.pipeline
from typing import TYPE_CHECKING
from azureml._base_sdk_common._docstring_wrapper import experimental
from azureml.automl.core.shared import constants, logging_utilities as log_utils
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared.constants import TimeSeriesInternal
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.shared.types import GrainType
from azureml.automl.runtime.shared import forecasting_utils
from sklearn.base import (BaseEstimator, TransformerMixin)


logger = logging.getLogger(__name__)

# NOTE:
# Here we import type checking only for type checking time.
# during runtime TYPE_CHECKING is set to False.
if TYPE_CHECKING:
    from azureml.automl.runtime.featurizer.transformer.timeseries.timeseries_transformer import TimeSeriesTransformer


@experimental
class DifferencingYTransformer(BaseEstimator, TransformerMixin):

    """DifferencingYTransformer class for non-stationary target column."""

    def __init__(self, non_stationary_time_series_ids: List[GrainType],
                 horizon_column_name: str = TimeSeriesInternal.HORIZON_NAME) -> None:
        """
        Initialize Differencing Y Transformer class.

        :param non_stationary_time_series_ids: non_stationary_time_series_ids of data.
        :type non_stationary_time_series_ids: List[GrainType]
        :param horizon_column_name: horizon_column_name of data.
        :type horizon_column_name: str
        """
        self.non_stationary_time_series_ids = non_stationary_time_series_ids
        self.horizon_column_name = horizon_column_name

    @staticmethod
    def get_differencing_y_transformer(
        y_pipeline: sklearn.pipeline.Pipeline
    ) -> 'Optional[DifferencingYTransformer]':
        """
        Check if y_pipeline contains DifferencingYTransformer or not.

        :param y_pipeline: Pipeline of y_transformers.
        :type y_pipeline: sklearn.pipeline.Pipeline
        :return: Optional[DifferencingYTransformer]
        """
        difference_transformer = None   # type: Optional[DifferencingYTransformer]
        if y_pipeline is not None:
            difference_transformer = forecasting_utils.get_pipeline_step(
                y_pipeline, TimeSeriesInternal.DIFFERENCING_Y_TRANSFORMER_NAME
            )

        return difference_transformer

    def fit(self, y: np.ndarray) -> 'DifferencingYTransformer':
        """
        Fit function for DifferencingY Transformer.

        :param y: Input training data.
        :type y: numpy.ndarray
        :return: Returns an instance of the DifferencingYTransformer model.
        """
        return self

    def transform(self, y: np.ndarray) -> np.ndarray:
        """
        Transform function for DifferencingY.

        :param y: Input data.
        :type y: numpy.ndarray
        :return: DifferencingY transform result.
        """
        return y

    def _get_index_and_reset(self, df: pd.DataFrame) -> Tuple[List[str], pd.DataFrame]:
        """
        Get the index of a data frame or an empty list if it is not there.

        Note: as a side effect this method will drop index on the data frame. No new
        data frame will be created.
        :param df: The data frame to be used.
        :return: The old index and the data frame with index reset.
        """
        index_list = df.index.names
        if len(index_list) == 1 and index_list[0] is None:
            index_list.clear()
        # We will drop the range index and will not the time or multiindex.
        df.reset_index(inplace=True, drop=not index_list)
        return index_list, df

    def _get_reference_val(self,
                           grain_dict_start_dates: List[pd.DataFrame],
                           first_train_grain_index: pd.Timestamp,
                           time_column_name: str,
                           freq: Optional[pd.DateOffset] = None
                           ) -> float:
        """
        Get reference val for start dates in inverse transform.

        :param dict_start_dates: Dictionary that holds the reference dates.
        :type dict_start_dates: Dict[GrainType, pd.DataFrame]
        :param time_column_name: time column name of input data.
        :type time_column_name: str.
        :param first_train_grain_index: First time index of input data.
        :type first_train_grain_index: pd.Timestamp
        :param freq: freq of fitted data.
        :type freq: Optional[pd.DateOffset]
        :return: reference val result.
        """
        reference_val = None     # type: Optional[float]
        time_iter = first_train_grain_index - freq if freq is not None else first_train_grain_index
        for horizon, value in enumerate(grain_dict_start_dates):
            if value[time_column_name] == time_iter:
                reference_val =\
                    grain_dict_start_dates[horizon][TimeSeriesInternal.DUMMY_TARGET_COLUMN]
                break

        Contract.assert_value(reference_val,
                              "reference_val",
                              reference_code=ReferenceCodes._FORECAST_FAILED_TO_GET_REF_VAL_CROSS_VALID,
                              log_safe=True)

        return cast(reference_val, float)

    def inverse_transform(self, y_pred: np.ndarray, x_test: Optional[pd.DataFrame] = None,
                          y_train: Optional[np.ndarray] = None, x_train: Optional[pd.DataFrame] = None,
                          timeseries_transformer: 'Optional[TimeSeriesTransformer]' = None,
                          last_known: Optional[Dict[GrainType, pd.Series]] = None) -> np.ndarray:
        """
        Inverse transform function for DifferencingY transform.

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
        :param last_known: last known date as a reference for rolling_forecast.
        :type last_known: Dict[GrainType, pd.Series]
        :return: Re-differenced result.
        """
        with log_utils.log_activity(logger,
                                    activity_name=constants.TelemetryConstants.RUN_STATIONARY_INVERSE_TRANSFORM_NAME):

            if timeseries_transformer is None:
                return y_pred

            stationary_featurizer = forecasting_utils.get_pipeline_step(
                timeseries_transformer.pipeline, TimeSeriesInternal.MAKE_STATIONARY_FEATURES
            )

            # stationary_featurizer is required to inverse transform.
            Contract.assert_value(
                stationary_featurizer,
                "stationary_featurizer",
                reference_code=ReferenceCodes._FORECAST_FAILED_TO_STATIONARY_FEATURIZER,
                log_safe=True
            )

            # For missing values, transform and inverse_transform are not supported.
            if not stationary_featurizer.do_stationarization:
                return y_pred

            # Forecasting for x_test does not have an index.
            x_test_index_names, x_test = self._get_index_and_reset(x_test)

            # This check is added for single timeseries dataset.
            # Single timeseries data for inverse transforms called from metrics_utilities have DUMMY_GRAIN_COLUMN.
            # Inverse transform called from forecast does not have DUMMY_GRAIN_COLUMN names.
            has_origin = False
            ix = copy.deepcopy(timeseries_transformer.grain_column_names)
            if TimeSeriesInternal.ORIGIN_TIME_COLNAME_DEFAULT in x_test_index_names:
                ix.append(self.horizon_column_name)
                has_origin = True

            if timeseries_transformer.grain_column_names == [constants.TimeSeriesInternal.DUMMY_GRAIN_COLUMN] and \
                    timeseries_transformer.grain_column_names[0] not in x_test.columns:
                x_test[constants.TimeSeriesInternal.DUMMY_GRAIN_COLUMN] =\
                    constants.TimeSeriesInternal.DUMMY_GRAIN_COLUMN

            x_test[TimeSeriesInternal.DUMMY_TARGET_COLUMN] = y_pred
            dict_start_dates = stationary_featurizer.start_values
            dict_last_dates = stationary_featurizer.last_values

            # Here, x_train is None due to forecasting of x_test.
            # Also, x_train and x_test can be the same dataframes.
            x_train_index_names = []
            if x_train is not None:
                x_train[TimeSeriesInternal.DUMMY_TARGET_COLUMN] = y_train
                x_train_index_names, x_train = self._get_index_and_reset(x_train)
                x_train_groupby_ob = x_train.groupby(ix)

            for index, df_test_grain in x_test.groupby(ix):
                grain = index
                if has_origin:
                    grain = index[:-1]
                    if len(grain) == 1:
                        # Unbox the tuple if we have single-column grain.
                        grain = grain[0]

                if grain in self.non_stationary_time_series_ids:
                    for col in stationary_featurizer.columns_to_be_processed:
                        first_grain_index = df_test_grain[timeseries_transformer.time_column_name].min()
                        reference_value = None     # type: Optional[float]
                        if dict_start_dates and (grain in dict_start_dates):
                            min_index_in_dict = dict_start_dates[grain][0][timeseries_transformer.time_column_name]
                            max_index_in_dict = dict_last_dates[grain][timeseries_transformer.time_column_name]

                            # This condition is added for rolling_forecast, and reference value is updated.
                            if last_known and len(last_known) != 0:
                                reference_value = last_known[grain][col]
                            elif first_grain_index == min_index_in_dict:
                                # The train set is being summated.
                                reference_value = dict_start_dates[grain][0][col]
                            elif has_origin and first_grain_index > min_index_in_dict and \
                                    first_grain_index <= min_index_in_dict + (
                                        (stationary_featurizer.lagging_length + index[-1] - 1)
                                        * stationary_featurizer.freq
                                    ):
                                # if max_horizon is more than 1,
                                # nans from look-back features for both regression and ensemble models will be removed.
                                # reference value is taken from start dates based on max_horizon.
                                reference_value = self._get_reference_val(
                                    dict_start_dates[grain],
                                    first_grain_index,
                                    timeseries_transformer.time_column_name,
                                    stationary_featurizer.freq
                                )

                                Contract.assert_value(
                                    reference_value,
                                    "reference_value",
                                    reference_code=ReferenceCodes._FORECAST_FAILED_TO_GET_REF_VAL_TRAIN_FULL,
                                    log_safe=True
                                )

                            elif first_grain_index > max_index_in_dict:
                                # reference val is the last observation in last_dates of stationarity featurizers.
                                # forecast function and train/valid configs use this implementation.
                                reference_value = dict_last_dates[grain][col]
                            elif first_grain_index > min_index_in_dict and \
                                    first_grain_index <= max_index_in_dict:
                                # Cross-validation
                                # For cross validation case, x_train needs to be inversed too.
                                # Getting the reference values from inversed x_train.
                                x_train_grain = x_train_groupby_ob.get_group(index)
                                x_train_grain.sort_values(by=timeseries_transformer.time_column_name, inplace=True)
                                first_train_grain_index = x_train_grain[timeseries_transformer.time_column_name].min()
                                train_ref = None     # type: float
                                if first_train_grain_index == min_index_in_dict:
                                    train_ref = dict_start_dates[grain][0][col]
                                # if max_horizon is more than 1,
                                # nans from look-back features for both regression and ensemble models will be removed.
                                # reference value is taken from start dates based on max_horizon.
                                elif has_origin and \
                                    first_train_grain_index > min_index_in_dict and \
                                        first_train_grain_index <= min_index_in_dict + (
                                            (stationary_featurizer.lagging_length + index[-1] - 1)
                                            * stationary_featurizer.freq
                                        ):
                                    train_ref = self._get_reference_val(
                                        dict_start_dates[grain],
                                        first_train_grain_index,
                                        timeseries_transformer.time_column_name,
                                        stationary_featurizer.freq
                                    )

                                reference_value = np.r_[
                                    train_ref, x_train_grain.loc[:, col]
                                ].cumsum().astype('float64')[-1]

                            x_test.at[df_test_grain.index, col] = np.r_[
                                reference_value,
                                x_test.loc[df_test_grain.index, col]
                            ].cumsum().astype('float64')[1:]

            if x_test_index_names:
                x_test.set_index(x_test_index_names, inplace=True)
            if x_train_index_names:
                x_train.set_index(x_train_index_names, inplace=True)

            return cast(np.ndarray, x_test.pop(TimeSeriesInternal.DUMMY_TARGET_COLUMN).values)

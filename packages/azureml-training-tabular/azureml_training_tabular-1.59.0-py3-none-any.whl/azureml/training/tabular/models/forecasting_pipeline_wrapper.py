# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import copy
import logging
import math
import uuid
from typing import Any, Dict, List, Optional, Tuple, Union, cast

import numpy as np
import pandas as pd
from pandas.tseries.frequencies import to_offset
from scipy.stats import norm
from sklearn.pipeline import Pipeline as SKPipeline

from azureml.automl.core.automl_base_settings import AutoMLBaseSettings
from azureml.automl.core.forecasting_parameters import ForecastingParameters
from ._timeseries._multi_grain_forecast_base import _MultiGrainForecastBase
from .forecasting_pipeline_wrapper_base import ForecastingPipelineWrapperBase
from .stack_ensemble import StackEnsembleRegressor
from .voting_ensemble import PreFittedSoftVotingRegressor

from azureml.automl.core.shared.constants import TimeSeries, TimeSeriesInternal
from azureml._common._error_definition import AzureMLError
from azureml.automl.core.constants import PredictionTransformTypes
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    AutoMLInternalLogSafe,
    DataShapeMismatch,
    ForecastPredictNotSupported,
    GenericFitError,
    GenericPredictError,
    QuantileRange,
    TimeseriesContextAtEndOfY,
    TimeseriesInsufficientDataForecast,
    TimeseriesNoDataContext,
    TimeseriesNonContiguousTargetColumn,
    TimeseriesNothingToPredict
)
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.shared.exceptions import (
    FitException,
    ValidationException,
    PredictionException,
    DataException,
    UserException)
from .._types import GrainType
from ..featurization.utilities import get_min_points
from ..timeseries import forecasting_utilities
from ..timeseries._frequency_fixer import fix_data_set_regularity_may_be

logger = logging.getLogger(__name__)


class RegressionPipeline(SKPipeline):
    """
    A pipeline with quantile predictions.

    This pipeline is a wrapper on the sklearn.pipeline.Pipeline to
    provide methods related to quantile estimation on predictions.
    """

    def __init__(self, pipeline: SKPipeline, stddev: Union[float, List[float]]) -> None:
        """
        Create a pipeline.

        :param pipeline: The pipeline to wrap.
        :param stddev:
            The standard deviation of the residuals from validation fold(s).
        """
        # We have to initiate the parameters from the constructor to avoid warnings.
        self.pipeline = pipeline
        if not isinstance(stddev, list):
            stddev = [stddev]
        self._stddev = stddev  # type: List[float]
        super().__init__(pipeline.steps, memory=pipeline.memory)
        self._quantiles = [0.5]

    @property
    def stddev(self) -> List[float]:
        """The standard deviation of the residuals from validation fold(s)."""
        return self._stddev

    @property
    def quantiles(self) -> List[float]:
        """Quantiles for the pipeline to predict."""
        return self._quantiles

    @quantiles.setter
    def quantiles(self, quantiles: Union[float, List[float]]) -> None:
        if not isinstance(quantiles, list):
            quantiles = [quantiles]

        for quant in quantiles:
            if quant <= 0 or quant >= 1:
                raise ValidationException._with_error(
                    AzureMLError.create(QuantileRange, target="quantiles", quantile=str(quant))
                )

        self._quantiles = quantiles

    def predict_quantiles(self, X: Any, **predict_params: Any) -> pd.DataFrame:
        """
        Get the prediction and quantiles from the fitted pipeline.

        :param X: The data to predict on.
        :return: The requested quantiles from prediction.
        :rtype: pandas.DataFrame
        """
        try:
            pred = self.predict(X, **predict_params)
        except Exception as e:
            raise PredictionException._with_error(
                AzureMLError.create(
                    GenericPredictError, target="RegressionPipeline",
                    transformer_name=self.__class__.__name__
                ), inner_exception=e) from e
        return self._get_ci(pred, np.full(len(pred), self._stddev[0]), self._quantiles)

    def _get_ci(self, y_pred: np.ndarray, stddev: np.ndarray, quantiles: List[float]) -> pd.DataFrame:
        """
        Get Confidence intervales for predictions.

        :param y_pred: The predicted values.
        :param stddev: The standard deviations.
        :param quantiles: The desired quantiles.
        """
        res = pd.DataFrame()
        for quantile in quantiles:
            ci_bound = 0.0
            if quantile != 0.5:
                z_score = norm.ppf(quantile)
                ci_bound = z_score * stddev
            res[quantile] = pd.Series(y_pred + ci_bound)
        return res


class ForecastingPipelineWrapper(RegressionPipeline, ForecastingPipelineWrapperBase):
    """A pipeline for forecasting."""

    # Constants for errors and warnings
    # Non recoverable errors.
    FATAL_WRONG_DESTINATION_TYPE = (
        "The forecast_destination argument has wrong type, " "it is a {}. We expected a datetime."
    )
    FATAL_DATA_SIZE_MISMATCH = "The length of y_pred is different from the X_pred"
    FATAL_WRONG_X_TYPE = "X_pred has unsupported type, x should be pandas.DataFrame, " "but it is a {}."
    FATAL_WRONG_Y_TYPE = "y_pred has unsupported type, y should be numpy.array or pandas.DataFrame, " "but it is a {}."
    FATAL_NO_DATA_CONTEXT = (
        "No y values were provided for one of time series. "
        "We expected non-null target values as prediction context because there "
        "is a gap between train and test and the forecaster "
        "depends on previous values of target. "
    )
    FATAL_NO_DESTINATION_OR_X_PRED = (
        "Input prediction data X_pred and forecast_destination are both None. " +
        "Please provide either X_pred or a forecast_destination date, but not both."
    )
    FATAL_DESTINATION_AND_X_PRED = (
        "Input prediction data X_pred and forecast_destination are both set. " +
        "Please provide either X_pred or a forecast_destination date, but not both."
    )
    FATAL_DESTINATION_AND_Y_PRED = (
        "Input prediction data y_pred and forecast_destination are both set. " +
        "Please provide either y_pred or a forecast_destination date, but not both."
    )
    FATAL_Y_ONLY = "If y_pred is provided X_pred should not be None."
    FATAL_NO_LAST_DATE = (
        "The last training date was not provided." "One of time series in scoring set was not present in training set."
    )
    FATAL_EARLY_DESTINATION = (
        "Input prediction data X_pred or input forecast_destination contains dates " +
        "prior to the latest date in the training data. " +
        "Please remove prediction rows with datetimes in the training date range " +
        "or adjust the forecast_destination date."
    )
    FATAL_NO_TARGET_IN_Y_DF = "The y_pred is a data frame, " "but it does not contain the target value column"
    FATAL_WRONG_QUANTILE = "Quantile should be a number between 0 and 1 (not inclusive)."

    FATAL_NO_TS_TRANSFORM = ("The time series transform is absent. "
                             "Please try training model again.")
    FATAL_NONPOSITIVE_HORIZON = "Forecast horizon must be a positive integer."

    # Constants
    TEMP_PRED_COLNAME = "__predicted"

    def __init__(self, pipeline: SKPipeline, stddev: List[float],
                 metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Create a pipeline.

        :param pipeline: The pipeline to wrap.
        :type pipeline: sklearn.pipeline.Pipeline
        :param stddev:
            The standard deviation of the residuals from validation fold(s).
        """
        self.adj_dict = []
        # We set empty metadata here and pipulate it in the future to pass validation
        # in the scikit-learn.
        self.metadata = {}
        RegressionPipeline.__init__(self, pipeline, stddev)
        for _, transformer in pipeline.steps:
            # FIXME: Work item #400231
            if type(transformer).__name__ == "TimeSeriesTransformer":
                ts_transformer = transformer

        if "ts_transformer" not in vars() or ts_transformer is None:
            msg = f'Failed to initialize ForecastingPipelineWrapper: \
                {ForecastingPipelineWrapperBase.FATAL_NO_TS_TRANSFORM}'
            raise ValidationException._with_error(AzureMLError.create(
                AutoMLInternalLogSafe, target="ForecastingPipelineWrapper", error_message=msg,
                error_details='')
            )
        y_transformer = None
        if hasattr(self.pipeline, 'y_transformer'):
            y_transformer = self.pipeline.y_transformer
        ForecastingPipelineWrapperBase.__init__(self, ts_transformer, y_transformer, metadata)

        # Calling fit naive here as we don't explicitly calling the fit method.
        if self._get_not_none_ts_transformer().has_unique_target_grains_dropper:
            self._fit_naive(True)

    def __setstate__(self, state: Dict[str, Any]):
        if "_y_transformer" not in state:
            state["_y_transformer"] = None
        self.__dict__.update(state)

    def _get_preprocessors_and_forecaster(self) -> Tuple[List[Any], Any]:
        """
        Get the list of data preprocessors and the forecaster object.

        The data preprocessors should have a scikit-like API and the forecaster should have a 'predict' method.
        """
        Contract.assert_non_empty(self.pipeline.steps, f'{type(self).__name__}.pipeline.steps')
        _, step_collection = zip(*self.pipeline.steps)
        preprocessors = list(step_collection[:-1])
        forecaster = step_collection[-1]

        return preprocessors, forecaster

    def _extend_internal(self, preprocessors: List[Any], forecaster: Any, X_known: pd.DataFrame,
                         ignore_data_errors: bool = False) -> Any:
        """
        Extend a copy of the forecaster on the known data after transforming it.

        This method does not modify the input forecaster; it extends and returns a copy of the input forecaster.
        """
        extended_forecaster = forecaster
        if self._model_is_extendable(forecaster) and not X_known.empty:
            _, X_ts_features_known = self._apply_preprocessors(preprocessors, X_known,
                                                               select_latest_origin_times=True)
            y_known = X_ts_features_known.pop(self.target_column_name).to_numpy()
            extended_forecaster = copy.deepcopy(forecaster)
            self._extend_transformed(extended_forecaster, X_ts_features_known, y_known)

        return extended_forecaster

    def _forecast_internal(self, preprocessors: List[Any], forecaster: Any, X_in: pd.DataFrame,
                           ignore_data_errors: bool) -> pd.DataFrame:
        """
        Make a forecast on the input data using the given preprocessors and forecasting model.

        This is an internal method containing core forecasting logic shared by public forecasting methods.
        """
        # Preprocess/featurize the data
        X_in, X_ts_features = self._apply_preprocessors(preprocessors, X_in,
                                                        select_latest_origin_times=True)
        y_known_series = X_ts_features.pop(self.target_column_name)

        try:
            y_out = forecaster.predict(X_in)
        except Exception as e:
            raise PredictionException._with_error(
                AzureMLError.create(
                    GenericPredictError, target="ForecastingPipelineWrapper",
                    transformer_name=self.__class__.__name__
                ), inner_exception=e) from e

        # Inversing the transform after prediction.
        if self._y_transformer is not None:
            y_out = self._y_transformer.inverse_transform(y_out,
                                                          x_test=X_ts_features,
                                                          y_train=None,
                                                          x_train=None,
                                                          timeseries_transformer=self._ts_transformer)

            # Here, y_known_values are inversed the transform, since in recursive_forecast,
            # differencing is also applied recursively.
            y_known_values = self._y_transformer.inverse_transform(y_known_series.values,
                                                                   x_test=X_ts_features,
                                                                   y_train=None,
                                                                   x_train=None,
                                                                   timeseries_transformer=self._ts_transformer)

            # Updating y_known_series for inversed values.
            y_known_series = pd.Series(y_known_values, index=y_known_series.index)

        X_ts_features[TimeSeriesInternal.DUMMY_TARGET_COLUMN] = y_out
        X_out = self._postprocess_output(X_ts_features, y_known_series)
        return X_out

    def _recursive_forecast(self, preprocessors: List[Any], forecaster: Any,
                            Xy_pred: pd.DataFrame,
                            ignore_data_errors: bool) -> pd.DataFrame:
        """
        Produce forecasts recursively on a rolling origin.

        Each iteration makes a forecast for the next 'max_horizon' periods
        with respect to the current origin, then advances the origin by the
        horizon duration. The prediction context for each forecast is set so
        that the forecaster uses forecasted target values for times prior to the current
        origin time for constructing lookback (lag, rolling window) features.

        This method assumes that Xy_pred is time-sorted and regular. That is, its time index must not
        have any gaps. If Xy_pred includes known targets, they must be contiguous and non-NaN.

        :param Xy_pred: The prediction data frame returned by _prepare_prediction_data_for_forecast.
        :param ignore_data_errors: Ignore errors in user data.
        :returns: Data frame where missing values in the target of Xy_pred are filled with corresponding forecasts.
        :rtype: pandas.DataFrame
        """

        start_rows = {tsid: 0 for tsid in self.forecast_origin}
        Xy_expand_fcst = pd.DataFrame()
        first_iter = True
        while len(start_rows) > 0:
            new_start_rows: Dict[GrainType, int] = {}

            # Get a batch of prediction data
            # A batch is an expanding window that starts at the beginning of the prediction data
            # and goes up to the end of the maximum horizon for the current iteration
            df_batch_list: List[pd.DataFrame] = []
            for tsid, df_one in Xy_pred.groupby(self.grain_column_names):
                df_batch_one = df_one
                start_idx = start_rows.get(tsid)
                if start_idx is not None:
                    if first_iter:
                        # Count known target values on first iteration to set the starting index
                        num_known = np.sum(pd.notnull(df_one[self.target_column_name]))
                        start_idx += num_known
                    h_ahead_idx = start_idx + self.max_horizon
                    df_batch_one = df_one.iloc[:h_ahead_idx]
                    if h_ahead_idx < df_one.shape[0]:
                        new_start_rows[tsid] = h_ahead_idx
                df_batch_list.append(df_batch_one)

            # Get the forecasted values on the batch
            Contract.assert_non_empty(df_batch_list, 'df_batch_list')
            Xy_batch = pd.concat(df_batch_list)
            Xy_expand_fcst = self._forecast_internal(preprocessors, forecaster, Xy_batch, ignore_data_errors)

            if len(new_start_rows) > 0:
                # Join forecasted values into the prediction data
                # forecasted values will be fed into lookback feature values for the next iteration
                merge_columns = [self._time_col_name] + self.grain_column_list
                Xy_pred.drop(columns=[self.target_column_name], inplace=True, errors='ignore')
                Xy_pred = \
                    Xy_pred.merge(Xy_expand_fcst[[self.target_column_name]], how='left', on=merge_columns, copy=False)

            start_rows = new_start_rows
            first_iter = False

        return Xy_expand_fcst

    def _pipeline_forecast_internal(
            self,
            X_pred: Optional[pd.DataFrame] = None,
            y_pred: Optional[Union[pd.DataFrame, np.ndarray]] = None,
            Xy_pred_in: Optional[pd.DataFrame] = None,
            dict_rename_back: Optional[Dict[str, str]] = None,
            forecast_destination: Optional[pd.Timestamp] = None,
            ignore_data_errors: bool = False,
            preprocessors: Optional[List[Any]] = None,
            forecaster: Optional[Any] = None
    ) -> Tuple[np.ndarray, pd.DataFrame]:
        """
        Do the forecast on the data frame X_pred.

        :param X_pred: the prediction dataframe combining X_past and X_future in a time-contiguous manner.
                       Empty values in X_pred will be imputed.
        :param y_pred: the target value combining definite values for y_past and missing values for Y_future.
                       If None the predictions will be made for every X_pred.
        :param ignore_data_errors: Ignore errors in user data.
        :type ignore_data_errors: bool
        :returns: Y_pred, with the subframe corresponding to Y_future filled in with the respective forecasts.
                  Any missing values in Y_past will be filled by imputer.
        :rtype: tuple
        """
        Xy_pred, Xy_known, max_horizon_exceeded = \
            self._prepare_prediction_data_for_forecast(Xy_pred_in, ignore_data_errors=ignore_data_errors)
        use_recursive_forecast = max_horizon_exceeded and self._lag_or_rw_enabled()

        # Check for known input and extend the model on (transformed) known actuals, if applicable
        if not Xy_known.empty and self._model_is_extendable(forecaster):
            forecaster = self._extend_internal(preprocessors, forecaster, Xy_known,
                                               ignore_data_errors=ignore_data_errors)

        # Get the forecast
        if use_recursive_forecast:
            test_feats = self._recursive_forecast(preprocessors, forecaster, Xy_pred, ignore_data_errors)
        else:
            test_feats = self._forecast_internal(preprocessors, forecaster, Xy_pred, ignore_data_errors)

        # Order the time series data frame as it was encountered as in initial input.
        if X_pred is not None:
            test_feats = self.align_output_to_input(Xy_pred_in, test_feats)
        else:
            test_feats.sort_index(inplace=True)
        # Gap adjustment
        if (not max_horizon_exceeded and hasattr(self, 'adj_dict') and self.adj_dict and
                TimeSeriesInternal.ADJUSTMENT in self.adj_dict and self.adj_dict[TimeSeriesInternal.ADJUSTMENT]):
            test_feats = ForecastingPipelineWrapperBase._adjust_forecast(test_feats,
                                                                         self.adj_dict,
                                                                         self.target_column_name,
                                                                         self.time_column_name,
                                                                         self.grain_column_names)
        y_pred = test_feats[self.target_column_name].to_numpy()

        # name index columns back as needed.
        if len(dict_rename_back) > 0:
            test_feats.rename_axis(index=dict_rename_back, inplace=True)

        return y_pred, test_feats

    def _rolling_forecast_internal(self, preprocessors: List[Any], forecaster: Any,
                                   Xy_ts_features: pd.DataFrame,
                                   step: int,
                                   ignore_data_errors: bool) -> pd.DataFrame:
        return self._forecaster_rolling_forecast(preprocessors, forecaster, Xy_ts_features, step)

    def apply_time_series_transform(self, X: pd.DataFrame, y: Optional[np.ndarray] = None) -> pd.DataFrame:
        """
        Apply all time series transforms to the data frame X.

        :param X: The data frame to be transformed.
        :type X: pandas.DataFrame
        :returns: The transformed data frame, having date, grain and origin
                  columns as indexes.
        :rtype: pandas.DataFrame

        """
        X_copy = X.copy()
        if y is not None:
            X_copy[self.target_column_name] = y
        for i in range(len(self.pipeline.steps) - 1):
            # FIXME: Work item #400231
            if type(self.pipeline.steps[i][1]).__name__ == "TimeSeriesTransformer":
                X_copy = self.pipeline.steps[i][1].transform(X_copy)
                # When we made a time series transformation we need to break and return X.
                if self.origin_col_name in X_copy.index.names:
                    X_copy = self._ts_transformer._select_latest_origin_dates(X_copy)
                X_copy.sort_index(inplace=True)
                # If the target column was created by featurizers, drop it.
                if self.target_column_name in X_copy:
                    X_copy.drop(self.target_column_name, axis=1, inplace=True)
                return X_copy
            else:
                X_copy = self.pipeline.steps[i][1].transform(X_copy)

    def _pipeline_forecast_quantiles_internal(
            self,
            X_pred: pd.DataFrame,
            pred: np.ndarray,
            transformed_data: pd.DataFrame,
            Xy_pred_in: Optional[pd.DataFrame] = None,
            ignore_data_errors: bool = False) -> pd.DataFrame:
        """
        Get the prediction and quantiles from the fitted pipeline.

        :param X_pred: the prediction dataframe combining X_past and X_future in a time-contiguous manner.
                       Empty values in X_pred will be imputed.
        :param y_pred: the target value combining definite values for y_past and missing values for Y_future.
                       If None the predictions will be made for every X_pred.
        :param forecast_destination: Forecast_destination: a time-stamp value.
                                     Forecasts will be made all the way to the forecast_destination time,
                                     for all grains. Dictionary input { grain -> timestamp } will not be accepted.
                                     If forecast_destination is not given, it will be imputed as the last time
                                     occurring in X_pred for every grain.
        :type forecast_destination: pandas.Timestamp
        :param ignore_data_errors: Ignore errors in user data.
        :type ignore_data_errors: bool
        :return: A dataframe containing time, grain, and corresponding quantiles for requested prediction.
        """
        Xy_pred, Xy_known, max_horizon_exceeded = \
            self._prepare_prediction_data_for_forecast(Xy_pred_in, ignore_data_errors=ignore_data_errors)

        use_recursive_forecast = max_horizon_exceeded and self._lag_or_rw_enabled()

        NOT_KNOWN_Y = 'y_not_known'
        max_horizon_featurizer = forecasting_utilities.get_pipeline_step(
            self._ts_transformer.pipeline, TimeSeriesInternal.MAX_HORIZON_FEATURIZER)
        horizon_column = None if max_horizon_featurizer is None else max_horizon_featurizer.horizon_colname

        freq = self.data_frequency
        dict_known = self.forecast_origin.copy()
        if not Xy_known.empty:
            for tsid, df_known_one in Xy_known.groupby(self.grain_column_names):
                dict_known[tsid] = df_known_one[self._time_col_name].iloc[-1]

        dfs = []
        for grain, df_one in transformed_data.groupby(self.grain_column_names):
            if grain in dict_known.keys():
                # Index levels are always sorted, but it is not guaranteed for data frame.
                df_one.sort_index(inplace=True)
                # Some y values are known for the given grain.
                df_one[NOT_KNOWN_Y] = df_one.index.get_level_values(self.time_column_name) > dict_known[grain]
            else:
                # Nothing is known. All data represent forecast.
                df_one[NOT_KNOWN_Y] = True
            dfs.append(df_one)
        transformed_data = pd.concat(dfs)
        # Make sure data sorted in the same order as input.
        if X_pred is not None:
            transformed_data = self.align_output_to_input(Xy_pred_in, transformed_data)
        # Some of our values in NOT_KNOWN_Y will be NaN, we need to say, that we "know" this y
        # and replace it with NaN.
        transformed_data[NOT_KNOWN_Y] = transformed_data.apply(
            lambda x: x[NOT_KNOWN_Y] if not pd.isnull(x[NOT_KNOWN_Y]) else False, axis=1)
        if horizon_column is not None and horizon_column in transformed_data.columns:
            # We also need to set horizons to make sure that horizons column
            # can be converted to integer.
            transformed_data[horizon_column] = transformed_data.apply(
                lambda x: x[horizon_column] if not pd.isnull(x[horizon_column]) else 1, axis=1)
        # Make sure y is aligned to data frame.
        pred = transformed_data[TimeSeriesInternal.DUMMY_TARGET_COLUMN].values

        horizon_stddevs = np.zeros(len(pred))
        horizon_stddevs.fill(np.NaN)
        try:
            if self._horizon_idx is None and horizon_column is not None:
                self._horizon_idx = self._ts_transformer.get_engineered_feature_names().index(horizon_column)
        except ValueError:
            self._horizon_idx = None

        is_not_known = transformed_data[NOT_KNOWN_Y].values.astype(int)
        MOD_TIME_COLUMN_CONSTANT = 'mod_time'
        # Retrieve horizon, if available, otherwise calculate it.
        # We also need to find the time difference from the origin to include it as a factor in our uncertainty
        # calculation. This is represented by mod_time and for horizon aware models will reprsent number of
        # max horizons from the original origin, otherwise number steps from origin.
        if self._horizon_idx is not None:
            horizons = transformed_data.values[:, self._horizon_idx].astype(int)

            if use_recursive_forecast:
                def add_horizon_counter(grp):
                    """
                    Get the modulo time column.

                    This method is used to calculate the number of times the horizon has "rolled". In the case of the
                    rolling/recursive forecast, each time delta that is beyond our max horizon is a forecast from the
                    previous time delta's forecast used as input to the lookback features. Since the estimation is
                    growing each time we recurse, we want to calculate the quantile with some added
                    uncertainty (growing with time). We use the modulo column from this method to do so. We also apply
                    this strategy on a per-grain basis.
                    """
                    grains = grp.name
                    if grains in dict_known:
                        last_known_single_grain = dict_known[grains]
                        forecast_times = grp.index.get_level_values(self.time_column_name)
                        date_grid = pd.date_range(
                            last_known_single_grain, forecast_times.max(), freq=freq
                        )
                        # anything forecast beyond the max horizon will need a time delta to increase uncertainty
                        grp[MOD_TIME_COLUMN_CONSTANT] = [
                            (math.ceil(date_grid.get_loc(forecast_times[i]) / self.max_horizon)
                             if forecast_times[i] >= last_known_single_grain else 1)
                            for i in range(len(grp))
                        ]
                    else:
                        # If we have encountered grain not present in the training set, we will set mod_time to 1
                        # as finally we will get NaN as a prediction.
                        grp[MOD_TIME_COLUMN_CONSTANT] = 1

                    return grp

                mod_time = transformed_data \
                    .groupby(self.grain_column_names, group_keys=False) \
                    .apply(add_horizon_counter)[MOD_TIME_COLUMN_CONSTANT].values
            else:
                mod_time = [1] * len(horizons)
        else:
            # If no horizon is present we are doing a forecast with no lookback features.
            # The last known timestamp can be used to calculate the horizon. We can then apply
            # an increase in uncertainty as horizon increases.
            def add_horizon(grp):
                grains = grp.name
                if grains in dict_known:
                    last_known_single_grain = dict_known[grains]
                    forecast_times = grp.index.get_level_values(self.time_column_name)
                    date_grid = pd.date_range(
                        last_known_single_grain, forecast_times.max(), freq=freq
                    )

                    grp[MOD_TIME_COLUMN_CONSTANT] = [
                        (date_grid.get_loc(forecast_times[i])
                         if forecast_times[i] >= last_known_single_grain else 1)
                        for i in range(len(grp))
                    ]
                else:
                    # If we have encountered grain not present in the training set, we will set mod_time to 1
                    # as finally we will get NaN as a prediction.
                    grp[MOD_TIME_COLUMN_CONSTANT] = 1
                return grp

            # We can groupby grain and then apply the horizon based on the time index within the grain
            # and the last known timestamps. We still need to know the horizons, but in this case the model
            # is not horizon aware, so there should only be one stddev and any forecast will use that value
            # with horizon (mod_time) used to increase uncertainty.
            mod_time = transformed_data.groupby(self.grain_column_names, group_keys=False) \
                .apply(add_horizon)[MOD_TIME_COLUMN_CONSTANT].values
            horizons = [1] * len(mod_time)

        for idx, horizon in enumerate(horizons):
            horizon = horizon - 1  # horizon needs to be 1 indexed
            try:
                horizon_stddevs[idx] = self._stddev[horizon] * is_not_known[idx] * math.sqrt(mod_time[idx])
            except IndexError:
                # In case of short training set cv may have nor estimated
                # stdev for highest horizon(s). Fix it by returning np.NaN
                horizon_stddevs[idx] = np.NaN

        # Get the prediction quantiles
        pred_quantiles = self._get_ci(pred, horizon_stddevs, self.quantiles)

        # Get time and grain columns from transformed data
        transformed_data = transformed_data.reset_index()
        time_column = transformed_data[self.time_column_name]
        grain_df = None
        if (self.grain_column_names is not None) and \
                (self.grain_column_names[0] != TimeSeriesInternal.DUMMY_GRAIN_COLUMN):
            grain_df = transformed_data[self.grain_column_names]

        return pd.concat((time_column, grain_df, pred_quantiles), axis=1)

    def _postprocess_output(self, X: pd.DataFrame, known_y: Optional[pd.Series]) -> pd.DataFrame:
        """
        Postprocess the data before returning it to user.

        Trim the data frame to the size of input.
        :param X: The data frame to be trimmed.
        :param known_y: The known or inferred y values.
                        We need to replace the existing values by them
        :returns: The data frame with the gap removed.

        """
        # If user have provided known y values, replace forecast by them even
        # if these values were imputed.
        if known_y is not None and any(not pd.isnull(val) for val in known_y):
            PRED_TARGET = "forecast"
            known_df = known_y.rename(TimeSeriesInternal.DUMMY_TARGET_COLUMN).to_frame()
            X.rename({TimeSeriesInternal.DUMMY_TARGET_COLUMN: PRED_TARGET}, axis=1, inplace=True)
            # Align known y and X with merge on indices
            X_merged = X.merge(known_df, left_index=True, right_index=True, how="inner")
            assert X_merged.shape[0] == X.shape[0]

            # Replace all NaNs in the known y column by forecast.

            def swap(x):
                return (
                    x[PRED_TARGET]
                    if pd.isnull(x[TimeSeriesInternal.DUMMY_TARGET_COLUMN])
                    else x[TimeSeriesInternal.DUMMY_TARGET_COLUMN]
                )

            X_merged[TimeSeriesInternal.DUMMY_TARGET_COLUMN] = X_merged.apply(lambda x: swap(x), axis=1)
            X = X_merged.drop(PRED_TARGET, axis=1)

        y_ = self._convert_target_type_maybe(X.pop(TimeSeriesInternal.DUMMY_TARGET_COLUMN).values)
        X[TimeSeriesInternal.DUMMY_TARGET_COLUMN] = y_
        return X

    def predict(self, X: pd.DataFrame) -> None:
        logger.error("The API predict is not supported for a forecast model.")
        raise UserException._with_error(
            AzureMLError.create(
                ForecastPredictNotSupported, target="predict",
                reference_code=ReferenceCodes._FORECASTING_PREDICT_NOT_SUPPORT
            )
        )

    def _raise_insufficient_data_maybe(
            self, X: pd.DataFrame, grain: Optional[str], min_points: int, operation: str
    ) -> None:
        """
        Raise the exception about insufficient grain size.

        :param X: The grain to be checked.
        :param grain: The grain name.
        :param min_points: The minimal number of points needed.
        :param operation: The name of an operation for which the validation
                          is being performed.
        :raises: DataException
        """
        if X.shape[0] < min_points:
            raise DataException._with_error(AzureMLError.create(
                TimeseriesInsufficientDataForecast, target="X", grains=grain,
                operation=operation,
                max_horizon=self._ts_transformer.max_horizon,
                lags=str(self._ts_transformer.get_target_lags()),
                window_size=self._ts_transformer.get_target_rolling_window_size(),
                reference_code=ReferenceCodes._FORECASTING_INSUFFICIENT_DATA
            ))

    def _get_automl_base_settings(self) -> AutoMLBaseSettings:
        """Generate the AutoMLBaseSettings safely."""
        if self._ts_transformer.pipeline is not None:
            window_size = self._ts_transformer.get_target_rolling_window_size()  # type: Optional[int]
            if window_size == 0:
                window_size = TimeSeriesInternal.WINDOW_SIZE_DEFAULT
            target_lags = self._ts_transformer.get_target_lags()  # type: Optional[List[int]]
            if target_lags == [0]:
                target_lags = TimeSeriesInternal.TARGET_LAGS_DEFAULT
        else:
            window_size = self._ts_transformer.parameters.get(TimeSeriesInternal.WINDOW_SIZE, 0)
            lags = self._ts_transformer.parameters.get(TimeSeriesInternal.LAGS_TO_CONSTRUCT)
            if lags is None:
                target_lags = [0]
            target_lags = lags.get(self.target_column_name, [0])
        grains = self._ts_transformer.grain_column_names
        if grains == [TimeSeriesInternal.DUMMY_GRAIN_COLUMN]:
            grains = []
        freq_str = self._ts_transformer.freq
        # If the frequency can not be converted to a pd.DateOffset,
        # then we need to set it to None.
        try:
            to_offset(freq_str)
        except BaseException:
            freq_str = None
        fc = ForecastingParameters(
            time_column_name=self._ts_transformer.time_column_name,
            time_series_id_column_names=grains,
            forecast_horizon=self._ts_transformer.max_horizon,
            group_column_names=None,
            target_lags=target_lags,
            feature_lags=self._ts_transformer.parameters.get(
                TimeSeries.FEATURE_LAGS, TimeSeriesInternal.FEATURE_LAGS_DEFAULT),
            target_rolling_window_size=window_size,
            seasonality=self._ts_transformer.parameters.get(
                TimeSeries.SEASONALITY, TimeSeriesInternal.SEASONALITY_VALUE_DEFAULT),
            country_or_region_for_holidays=self._ts_transformer.parameters.get(TimeSeries.COUNTRY_OR_REGION),
            use_stl=self._ts_transformer.parameters.get(
                TimeSeries.USE_STL, TimeSeriesInternal.USE_STL_DEFAULT),
            short_series_handling_configuration=self._ts_transformer.parameters.get(
                TimeSeries.SHORT_SERIES_HANDLING_CONFIG,
                TimeSeriesInternal.SHORT_SERIES_HANDLING_CONFIG_DEFAULT),
            freq=freq_str,
            target_aggregation_function=self._ts_transformer.parameters.get(
                TimeSeries.TARGET_AGG_FUN, TimeSeriesInternal.TARGET_AGG_FUN_DEFAULT)
        )
        if self._ts_transformer.parameters.get(TimeSeries.DROP_COLUMN_NAMES):
            fc.drop_column_names = self._ts_transformer.parameters.get(TimeSeries.DROP_COLUMN_NAMES)
        return AutoMLBaseSettings(
            primary_metric='r2_score',
            is_timeseries=True,
            featurization=self._ts_transformer._featurization_config,
            forecasting_parameters=fc)

    def _preprocess_check(
            self, X: pd.DataFrame, y: np.ndarray, operation: str, pad_short_grains: bool
    ) -> Tuple[pd.DataFrame, np.ndarray]:
        """
        Do the simple preprocessing and check for model retraining and in sample forecasting.

        :param X: The prediction data frame.
        :param y: The array of target values.
        :param operation: The name of an operation for which the preprocessing
                          is being performed.
        :param pad_short_grains: If true the short grains will be padded.
        :return: The tuple of sanitized data.
        """
        # Data checks.
        self._check_data(X, y, None)
        if X.shape[0] != y.shape[0]:
            raise DataException._with_error(
                AzureMLError.create(
                    DataShapeMismatch, target='X_and_y',
                    reference_code=ReferenceCodes._FORECASTING_DATA_SHAPE_MISMATCH
                )
            )

        # Ensure the type of a time and grain columns.
        X = self._check_convert_grain_types(X)
        X = self._convert_time_column_name_safe(X, ReferenceCodes._FORECASTING_PREPROCESS_INVALID_VALUE)

        # Fix the data set frequency and aggregate data.
        automl_settings = self._get_automl_base_settings()
        fixed_ds = fix_data_set_regularity_may_be(
            X, y,
            automl_settings=automl_settings,
            # We do not set the reference code here, because we check that freq can be
            # convertible to string or None in AutoMLTimeSeriesSettings.
            freq_ref_code=""
        )
        # If short grain padding is disabled, we need to check if the short grain
        # are present.
        short_series_handling_configuration = self._ts_transformer.parameters.get(
            TimeSeries.SHORT_SERIES_HANDLING_CONFIG, TimeSeriesInternal.SHORT_SERIES_HANDLING_CONFIG_DEFAULT
        )
        if short_series_handling_configuration is None:
            min_points = get_min_points(
                window_size=self._ts_transformer.get_target_rolling_window_size(),
                lags=self._ts_transformer.get_target_lags(),
                max_horizon=self._ts_transformer.max_horizon,
                cv=None,
                n_step=None,
            )
            if self._ts_transformer.grain_column_names == [TimeSeriesInternal.DUMMY_GRAIN_COLUMN]:
                self._raise_insufficient_data_maybe(fixed_ds.data_x, None, min_points, operation)
            else:
                for grain, df in fixed_ds.data_x.groupby(self._ts_transformer.grain_column_names):
                    self._raise_insufficient_data_maybe(df, grain, min_points, operation)
        # Pad the short series if needed
        # We have to import short_grain_padding here because importing it at the top causes the cyclic
        # import while importing ml_engine.
        from ..timeseries import _short_grain_padding

        if pad_short_grains:
            X, y = _short_grain_padding.pad_short_grains_or_raise(
                fixed_ds.data_x, cast(np.ndarray, fixed_ds.data_y),
                freq=self._ts_transformer.freq_offset,
                automl_settings=automl_settings, ref_code="")
            return X, y
        return fixed_ds.data_x, cast(np.ndarray, fixed_ds.data_y)

    def _in_sample_fit(self, X: pd.DataFrame, y: np.ndarray) -> Tuple[np.ndarray, pd.DataFrame]:
        """
        Predict the data from the training set.

        :param X: The prediction data frame.
        :param y: The array of target values.
        :return: The array and the data frame with predictions.
        """
        X_copy = X.copy()
        X_agg, _ = self.preaggregate_data_set(X, y, is_training_set=False)
        was_aggregated = False
        if X_agg.shape != X.shape:
            was_aggregated = True
        X_copy, y = self._preprocess_check(X_copy, y, "in-sample forecasting", False)
        X_copy = self._create_prediction_data_frame(X_copy, y, forecast_destination=None, ignore_data_errors=True)

        ts_transformer = self._get_not_none_ts_transformer()
        if ts_transformer.has_unique_target_grains_dropper:
            unique_X = ts_transformer.unique_target_grains_dropper.get_unique_grain(X_copy)
            if unique_X is not None:
                unique_y = unique_X.pop(TimeSeriesInternal.DUMMY_TARGET_COLUMN).values
                self._naive_model.fit(unique_X, unique_y)
        y = X_copy.pop(TimeSeriesInternal.DUMMY_TARGET_COLUMN).values
        test_feats = None  # type: Optional[pd.DataFrame]
        for i in range(len(self.pipeline.steps) - 1):
            # FIXME: Work item #400231
            if type(self.pipeline.steps[i][1]).__name__ == "TimeSeriesTransformer":
                test_feats = self.pipeline.steps[i][1].transform(X_copy, y)
                # We do not need the target column now.
                # The target column is deleted by the rolling window during transform.
                # If there is no rolling window we need to make sure the column was dropped.
                if self._ts_transformer.target_column_name in test_feats.columns:
                    # We want to store the y_known_series for future use.
                    test_feats.drop(self._ts_transformer.target_column_name, inplace=True, axis=1)
                # If origin times are present, remove nans from look-back features and select the latest origins
                if self.origin_col_name in test_feats.index.names:
                    y = np.zeros(test_feats.shape[0])
                    test_feats, _ = self._ts_transformer._remove_nans_from_look_back_features(test_feats, y)
                    test_feats = self._ts_transformer._select_latest_origin_dates(test_feats)
                X_copy = test_feats.copy()
            else:
                X_copy = self.pipeline.steps[i][1].transform(X_copy)
        # TODO: refactor prediction in the separate method and make AML style error.
        try:
            y_preds = self.pipeline.steps[-1][1].predict(X_copy)
        except Exception as e:
            raise PredictionException._with_error(
                AzureMLError.create(
                    GenericPredictError, target="ForecastingPipelineWrapper",
                    transformer_name=self.__class__.__name__
                ), inner_exception=e) from e

        cast(pd.DataFrame, test_feats)[TimeSeriesInternal.DUMMY_TARGET_COLUMN] = y_preds
        test_feats = self._postprocess_output(test_feats, known_y=None)
        # Order the time series data frame as it was encountered as in initial input.
        if not was_aggregated:
            test_feats = self.align_output_to_input(X, test_feats)
        y_pred = test_feats[TimeSeriesInternal.DUMMY_TARGET_COLUMN].values
        return y_pred, test_feats

    def fit(self, X: pd.DataFrame, y: np.ndarray) -> "ForecastingPipelineWrapper":
        ForecastingPipelineWrapperBase.fit(self, X, y)
        return self

    def _pipeline_fit_internal(self, X: pd.DataFrame, y: np.ndarray) -> "ForecastingPipelineWrapper":
        """
        Train the model on different data.

        :param X: The prediction data frame.
        :param y: The array of target values.
        :return: The instance of ForecastingPipelineWrapper trained on X and y.
        """
        X.reset_index(drop=True, inplace=True)
        # Drop rows, containing NaN in timestamps or in y.

        if any(np.isnan(y_one) for y_one in y) or X[self.time_column_name].isnull().any():
            X[TimeSeriesInternal.DUMMY_TARGET_COLUMN] = y
            X = X.dropna(subset=[self.time_column_name, TimeSeriesInternal.DUMMY_TARGET_COLUMN], inplace=False, axis=0)
            y = X.pop(TimeSeriesInternal.DUMMY_TARGET_COLUMN).values
        X, y = self._preprocess_check(X, y, "fitting", True)
        for i in range(len(self.pipeline.steps) - 1):
            # FIXME: Work item #400231
            if type(self.pipeline.steps[i][1]).__name__ == "TimeSeriesTransformer":
                X = self.pipeline.steps[i][1].fit_transform(X, y)
                y = X.pop(TimeSeriesInternal.DUMMY_TARGET_COLUMN).values
                # If origin times are present, remove nans from look-back features and select the latest origins
                if self.origin_col_name in X.index.names:
                    X, y = self._ts_transformer._remove_nans_from_look_back_features(X, y)
            else:
                if hasattr(self.pipeline.steps[i][1], "fit_transform"):
                    X = self.pipeline.steps[i][1].fit_transform(X, y)
                else:
                    X = self.pipeline.steps[i][1].fit(X, y).transform(X)
        # TODO: refactor prediction in the separate method and make AML style error.
        try:
            self.pipeline.steps[-1][1].fit(X, y)
        except Exception as e:
            raise FitException._with_error(
                AzureMLError.create(
                    GenericFitError,
                    reference_code=ReferenceCodes._FORECASTING_PIPELINE_FIT_FAILURE,
                    transformer_name=self.__class__.__name__,
                ), inner_exception=e) from e
        return self

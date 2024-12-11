# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, cast, Dict, Generator, List, Optional, Tuple, Type, TYPE_CHECKING, Union
from abc import abstractmethod, ABC
import copy
import logging
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline as SKPipeline
import uuid
import warnings

from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared.constants import TimeSeries, TimeSeriesInternal
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared._diagnostics.validation import Validation
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    ArgumentOutOfRange,
    AutoMLInternal,
    AutoMLInternalLogSafe,
    ForecastPredictionTimesMisaligned,
    ForecastingEmptyDataAfterAggregation,
    GenericPredictError,
    InvalidArgumentType,
    MissingColumnsInData,
    PandasDatetimeConversion,
    RollingForecastMissingTargetValues,
    TimeseriesContextAtEndOfY,
    TimeseriesDfContainsNaN,
    TimeseriesCustomFeatureTypeConversion,
    TimeseriesDfDatesOutOfPhase,
    TimeseriesDfInvalidArgFcPipeYOnly,
    TimeseriesDfInvalidArgOnlyOneArgRequired,
    TimeseriesDfFrequencyError,
    TimeseriesGrainAbsentNoGrainInTrain,
    TimeseriesGrainAbsentNoLastDate,
    TimeseriesMissingValuesInY,
    TimeseriesNoDataContext,
    TimeseriesNonContiguousTargetColumn,
    TimeseriesNothingToPredict,
    TimeseriesNoUsableGrains,
    TimeseriesWrongShapeDataSizeMismatch,
    TimeseriesWrongShapeDataEarlyDest,
)
from azureml.automl.core.shared.exceptions import (
    DataException,
    InvalidOperationException,
    PredictionException,
    UntrainedModelException,
    ValidationException
)
from azureml.automl.core.shared.forecasting_exception import ForecastingDataException, ForecastingConfigException
from ._forecast_scenario_data import _ForecastScenarioData
from ._timeseries._multi_grain_forecast_base import _MultiGrainForecastBase
from .forecasting_models import Naive
from .stack_ensemble import StackEnsembleRegressor
from .voting_ensemble import PreFittedSoftVotingRegressor
from .._types import GrainType
from ..timeseries import forecasting_utilities, _freq_aggregator
from ..timeseries._frequency_fixer import fix_df_frequency
from ..timeseries._time_series_column_helper import convert_check_grain_value_types
from ..timeseries._time_series_data_config import TimeSeriesDataConfig
from ..timeseries._time_series_data_set import TimeSeriesDataSet

_logger = logging.getLogger(__name__)

# NOTE:
# Here we import type checking only for type checking time.
# during runtime TYPE_CHECKING is set to False.
if TYPE_CHECKING:
    from azureml._common._error_definition.error_definition import ErrorDefinition
    from ..featurization.timeseries.timeseries_transformer import TimeSeriesTransformer
    from ..featurization.timeseries.time_series_imputer import TimeSeriesImputer
    from ..featurization.timeseries.stationary_featurizer import StationaryFeaturizer


class ForecastingPipelineWrapperBase(ABC):
    """Base class for forecast model wrapper."""
    FATAL_NO_TARGET_IMPUTER = 'No target imputers were found in TimeSeriesTransformer.'
    FATAL_NO_TS_TRANSFORM = "The time series transform is absent. " "Please try training model again."
    _ACTUAL_COLUMN_NAME_BASE = '_automl_actual'
    _FORECAST_COLUMN_NAME_BASE = '_automl_forecast'
    _FORECAST_ORIGIN_COLUMN_NAME = '_automl_forecast_origin'

    _FORECAST_SCENARIO_FORECAST = "forecast"
    _FORECAST_SCENARIO_FORECAST_QUANTILES = "forecast_quantiles"
    _FORECAST_SCENARIO_ROLLING_FORECAST = "rolling_forecast"

    def __init__(
            self,
            ts_transformer: Optional['TimeSeriesTransformer'] = None,
            y_transformer: Optional[SKPipeline] = None,
            metadata: Optional[Dict[str, Any]] = None,
    ):
        self._y_transformer = y_transformer
        self._quantiles = [.5]
        self._horizon_idx = None  # type: Optional[int]
        self.forecast_origin = {}  # type: Dict[GrainType, pd.Timestamp]
        self._ts_transformer = None  # type: Optional['TimeSeriesTransformer']
        self._time_col_name = None  # type: Optional[str]
        self._origin_col_name = None  # type: Optional[str]
        self.grain_column_names = None  # type: Optional[GrainType]
        self.target_column_name = None  # type: Optional[str]
        self._ts_transformer = cast('TimeSeriesTransformer', self._ts_transformer)
        self.grain_column_names = cast(List[str], self.grain_column_names)
        self._naive_model = None  # type: Optional[Naive]
        if ts_transformer is not None:
            self._update_params(ts_transformer)
        self.metadata = metadata if metadata else {}

    def _update_params(self, ts_transformer: 'TimeSeriesTransformer') -> None:
        """Set object timeseries metadata from the ts_transformer."""
        self._ts_transformer = ts_transformer
        self._origin_col_name = ts_transformer.origin_column_name
        self._time_col_name = ts_transformer.time_column_name
        self.grain_column_names = ts_transformer.grain_column_names
        self.target_column_name = ts_transformer.target_column_name
        self.data_frequency = cast(pd.DateOffset, ts_transformer.freq_offset)
        self.forecast_origin = ts_transformer.dict_latest_date
        if ts_transformer.has_unique_target_grains_dropper:
            if ts_transformer.unique_target_grain_dropper.last_validation_X_y[0] is not None:
                self._update_forecast_origin(ts_transformer.unique_target_grain_dropper.last_validation_X_y[0])
            else:
                self._update_forecast_origin(ts_transformer.unique_target_grain_dropper.last_X_y[0])

    @property
    def time_column_name(self) -> str:
        """Return the name of the time column."""
        return cast(str, self._time_col_name)

    @property
    def user_target_column_name(self) -> Optional[str]:
        return self._ts_transformer.user_target_column_name if self._ts_transformer is not None else None

    @property
    def forecast_origin_column_name(self) -> str:
        return self._FORECAST_ORIGIN_COLUMN_NAME

    @property
    def actual_column_name(self) -> str:
        actual_name = self._ACTUAL_COLUMN_NAME_BASE
        user_target_name = self.user_target_column_name
        if user_target_name is not None:
            actual_name = actual_name + '_' + user_target_name

        return actual_name

    @property
    def forecast_column_name(self) -> str:
        forecast_name = self._FORECAST_COLUMN_NAME_BASE
        user_target_name = self.user_target_column_name
        if user_target_name is not None:
            forecast_name = forecast_name + '_' + user_target_name

        return forecast_name

    @property
    def origin_col_name(self) -> str:
        """Return the origin column name."""
        # Note this method will return origin column name,
        # which is only used for reconstruction of a TimeSeriesDataSet.
        # If origin column was introduced during transformation it is still None
        # on ts_transformer.
        if self._origin_col_name is None:
            self._origin_col_name = self._get_not_none_ts_transformer().origin_column_name
        # TODO: Double check type: Union[str, List[str]]
        ret = self._origin_col_name if self._origin_col_name \
            else TimeSeriesInternal.ORIGIN_TIME_COLNAME_DEFAULT
        return cast(str, ret)

    @property
    def max_horizon(self) -> int:
        """Return max hiorizon used in the model."""
        return self._get_not_none_ts_transformer().max_horizon

    @property
    def target_lags(self) -> List[int]:
        """Return target lags if any."""
        return self._get_not_none_ts_transformer().get_target_lags()

    @property
    def target_rolling_window_size(self) -> int:
        """Return the size of rolling window."""
        return self._get_not_none_ts_transformer().get_target_rolling_window_size()

    @abstractmethod
    def _get_preprocessors_and_forecaster(self) -> Tuple[List[Any], Any]:
        """
        Get the list of data preprocessors and the forecaster object.

        The data preprocessors should have a scikit-like API and the forecaster should have a 'predict' method.
        """
        raise NotImplementedError()

    @abstractmethod
    def _forecast_internal(self, preprocessors: List[Any], forecaster: Any, X_in: pd.DataFrame,
                           ignore_data_errors: bool) -> pd.DataFrame:
        """Make a forecast on the input data using the given preprocessors and forecasting model."""
        raise NotImplementedError()

    @abstractmethod
    def _rolling_forecast_internal(self, preprocessors: List[Any], forecaster: Any,
                                   Xy_ts_features: pd.DataFrame,
                                   step: int,
                                   ignore_data_errors: bool) -> pd.DataFrame:
        """
        Internal rolling forecast interface.
        """
        raise NotImplementedError()

    def _forecaster_rolling_forecast(
            self, preprocessors: List[Any], forecaster: Any,
            Xy_ts_features: pd.DataFrame,
            step: int) -> pd.DataFrame:
        """
        Produce forecasts on a rolling origin over a test set.

        This method contains the internal logic for making a rolling forecast for a non-DNN model.
        The input data frame is assumed to contain regular, full, featurized timeseries. That is, no observation
        gaps or missing target values and all features needed by the model should be present.
        """
        ts_transformer = self._get_not_none_ts_transformer()
        origin_times = self.forecast_origin.copy()
        Contract.assert_non_empty(origin_times, 'origin_times')

        forecaster_ext = forecaster
        extendable_forecaster = self._model_is_extendable(forecaster)

        df_fcst_list: List[pd.DataFrame] = []

        stationarity_transform = forecasting_utilities.get_pipeline_step(
            ts_transformer.pipeline,
            TimeSeriesInternal.MAKE_STATIONARY_FEATURES
        )
        if stationarity_transform is not None:
            stationary_transform_latest_backup = copy.deepcopy(stationarity_transform.last_values)

        while len(origin_times) > 0:
            new_origin_times: Dict[GrainType, pd.Timestamp] = {}

            # Internal loop over series to assemble the current "batch", or, horizon-sized window
            # for each series starting at the current set of origin times.
            df_batch_list: List[pd.DataFrame] = []
            df_known_list: List[pd.DataFrame] = []

            for tsid, df_one in Xy_ts_features.groupby(self.grain_column_names):
                origin_time = origin_times.get(tsid)
                if origin_time is None:
                    continue
                horizon_time = origin_time + self.max_horizon * self.data_frequency
                tidx = df_one.index.get_level_values(self._time_col_name)
                if extendable_forecaster or stationarity_transform is not None:
                    # If model is extendable, get known/context data for extension
                    df_one_known = df_one[tidx <= origin_time]
                    if not df_one_known.empty:
                        if extendable_forecaster:
                            df_known_list.append(df_one_known)
                        if (self._y_transformer is not None and stationarity_transform is not None
                                and len(df_one_known) != 0):
                            # Here, we are getting reference values, stationarity_transform.last_values,
                            # after inversing the transform since the data is already differenced.
                            y_differenced = df_one_known.pop(self.target_column_name).values
                            y_summated = \
                                self._y_transformer.inverse_transform(
                                    y_pred=y_differenced,
                                    x_test=df_one_known,
                                    y_train=None,
                                    x_train=None,
                                    timeseries_transformer=self._ts_transformer,
                                    last_known=stationary_transform_latest_backup)
                            df_one_known[self.target_column_name] = y_differenced
                            last_index = df_one_known.index.get_level_values(self.time_column_name).max()
                            stationarity_transform.last_values[tsid] =\
                                df_one_known.loc[last_index:last_index].reset_index().iloc[0]
                            stationarity_transform.last_values[tsid][self.target_column_name] = y_summated[-1]

                # Extract the current batch for the series
                df_one_batch = df_one[(tidx > origin_time) & (tidx <= horizon_time)]
                if ts_transformer.origin_column_name in df_one.index.names:
                    # If the index has origin times, lookback features are present.
                    # Get rid of any rows in the batch with lookback features that have origin times
                    # later than the current origin time for the iteration.
                    # Then, select latest/most-recent available lookback features
                    df_one_batch = \
                        ts_transformer._select_known_before_date(df_one_batch, origin_time, self.data_frequency)
                    df_one_batch = ts_transformer._select_latest_origin_dates(df_one_batch)
                df_batch_list.append(df_one_batch)

                # Set the origin time for the next iteration; advance by 'step' time periods
                # If the horizon time is past the end of the time index, we're done with this series
                if horizon_time < tidx.max():
                    new_origin_times[tsid] = origin_time + step * self.data_frequency

            X_batch = pd.concat(df_batch_list, sort=False)
            X_batch.drop(columns=[self.target_column_name], inplace=True)

            # Extend the forecaster if applicable
            if extendable_forecaster and len(df_known_list) > 0:
                X_known = pd.concat(df_known_list, sort=False)
                forecaster_ext = copy.deepcopy(forecaster)
                y_known = X_known.pop(self.target_column_name).to_numpy()
                self._extend_transformed(forecaster_ext, X_known, y_known)

            # Run the remaining preprocessors and get predictions on the batch for all series
            try:
                X_in = X_batch
                for preproc in preprocessors:
                    X_in = preproc.transform(X_in)
                y_batch_fcst = forecaster_ext.predict(X_in)
            except Exception as e:
                raise PredictionException._with_error(
                    AzureMLError.create(
                        GenericPredictError, target="rolling_forecast_internal",
                        transformer_name=self.__class__.__name__
                    ), inner_exception=e) from e

            # Each forecast batch should be a simple (no index) data frame
            # with time, forecast origin, tsid, and forecast columns
            keep_columns = [self.time_column_name] + self.grain_column_list
            X_batch.reset_index(inplace=True)
            X_batch = X_batch[keep_columns]
            X_batch[self.forecast_column_name] = y_batch_fcst
            X_batch = (X_batch.groupby(self.grain_column_names, group_keys=False)
                       .apply(lambda X: X.assign(**{self.forecast_origin_column_name: origin_times[X.name]})))

            # Inversing the predictions for each batch and update the reference point for next batch.
            X_batch = self._inverse_transform_target_maybe(X_batch, stationarity_transform)

            df_fcst_list.append(X_batch)
            origin_times = new_origin_times
        if stationarity_transform is not None:
            stationarity_transform.last_values = stationary_transform_latest_backup
        # Gap adjustment
        if (hasattr(self, 'adj_dict') and self.adj_dict and TimeSeriesInternal.ADJUSTMENT in self.adj_dict
                and self.adj_dict[TimeSeriesInternal.ADJUSTMENT]):
            df_fcst_list = self._adjust_forecast_rolling(df_fcst_list,
                                                         self.adj_dict,
                                                         self.forecast_column_name,
                                                         self.grain_column_names,
                                                         self.time_column_name)
        return pd.concat(df_fcst_list, sort=False)

    def _inverse_transform_target_maybe(
            self, X_batch: pd.DataFrame,
            stationarity_transform: 'Optional[StationaryFeaturizer]') -> pd.DataFrame:
        """
        Apply inverse transformation to y values.

        *Note:* Here we are having the assumption that predictions are stored in
        self.forecast_column_name column, this method is intended to be called in
        the rolling forecast scenario.
        If there is no _y_transformer no changes will be made to the data set.
        :param X_batch: The predictions to be processed by the y inverse transformer.
        :param stationarity_transform: The stationary transform if any.
        :return: transformed data.
        """
        if self._y_transformer is not None:
            last_known_ = stationarity_transform.last_values if stationarity_transform is not None else None
            y = self._y_transformer.inverse_transform(y_pred=X_batch[self.forecast_column_name].to_numpy(),
                                                      x_test=X_batch,
                                                      y_train=None,
                                                      x_train=None,
                                                      timeseries_transformer=self._ts_transformer,
                                                      last_known=last_known_)
            X_batch[self.forecast_column_name] = self._convert_target_type_maybe(y)
        return X_batch

    def is_grain_dropped(self, grain: GrainType) -> bool:
        """
        Return true if the grain is going to be dropped.

        :param grain: The grain to test if it will be dropped.
        :return: True if the grain will be dropped.
        """
        ts_transformer = self._get_not_none_ts_transformer()
        short_grain_dropper = forecasting_utilities.get_pipeline_step(
            ts_transformer.pipeline, TimeSeriesInternal.SHORT_SERIES_DROPPEER)
        unique_target_grain_dropper = ts_transformer.unique_target_grain_dropper

        if short_grain_dropper is None and not ts_transformer.has_unique_target_grains_dropper:
            return False
        # Any grain that has not seen before will also be dropped.
        for dropper in [unique_target_grain_dropper, short_grain_dropper]:
            if dropper is not None and grain not in dropper.grains_to_keep:
                return True

        return False

    @abstractmethod
    def _pipeline_fit_internal(
            self, X: pd.DataFrame, y: np.ndarray
    ) -> 'ForecastingPipelineWrapperBase':
        raise NotImplementedError

    @abstractmethod
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
        raise NotImplementedError

    @abstractmethod
    def _pipeline_forecast_quantiles_internal(
            self,
            X_pred: pd.DataFrame,
            pred: np.ndarray,
            transformed_data: pd.DataFrame,
            Xy_pred_in: pd.DataFrame,
            ignore_data_errors: Optional[bool] = False
    ) -> pd.DataFrame:
        raise NotImplementedError

    # region Scenario forecast

    def _scenario_forecast(
            self,
            forecast_scenario: str,
            X_pred: Optional[pd.DataFrame] = None,
            y_pred: Optional[Union[pd.DataFrame, np.ndarray]] = None,
            forecast_destination: Optional[pd.Timestamp] = None,
            ignore_data_errors: bool = False,
            step: int = 1,
            pred: Optional[np.ndarray] = None,
            transformed_data: Optional[np.ndarray] = None,
            preprocessors: Optional[List[Any]] = None,
            forecaster: Optional[Any] = None,
    ) -> Tuple[Optional[np.ndarray], pd.DataFrame]:
        forecast_list = []
        forecast_df_list = []
        forecast_scenario_data = self._prepare_prediction_input_common(
            X_pred=X_pred, y_pred=y_pred,
            forecast_destination=forecast_destination,
            ignore_data_errors=ignore_data_errors)

        for data_scenario in _ForecastScenarioData._DATA_SCENARIO:
            df = forecast_scenario_data.get_scenario_data(data_scenario)
            if df.empty:
                continue
            elif data_scenario == _ForecastScenarioData._DATA_SCENARIO_UNIQUE:
                forecast, forecast_df = self._scenario_forecast_naive(
                    forecast_scenario, df, step, ignore_data_errors, forecast_scenario_data.dict_rename_back,
                    pred, transformed_data)
            else:
                # default to use automl pipeline forecaster
                forecast, forecast_df = self._scenario_forecast_automl(
                    forecast_scenario, X_pred, y_pred, df, ignore_data_errors, step,
                    forecast_scenario_data.dict_rename_back, forecast_destination,
                    preprocessors, forecaster, pred, transformed_data)
            if forecast is not None:
                forecast_list.append(forecast)
            forecast_df_list.append(forecast_df)

        if len(forecast_list) > 0:
            forecast = np.concatenate(forecast_list)
        columns_in_results = self._get_forecast_columns_in_results(forecast_scenario, X_pred)
        forecast_df = self._merge_forecast_result_df(
            forecast_df_list, columns_in_results,
            forecast_scenario == ForecastingPipelineWrapperBase._FORECAST_SCENARIO_ROLLING_FORECAST)

        return forecast, forecast_df

    def _get_forecast_columns_in_results(self, forecast_scenario: str, X_pred: pd.DataFrame) -> Optional[List[str]]:
        columns_in_results = None
        if forecast_scenario == ForecastingPipelineWrapperBase._FORECAST_SCENARIO_ROLLING_FORECAST:
            effective_ts_ids = self._get_effective_time_series_ids(X_pred)
            # Sort by tsid, forecasting origin, and time, respectively.
            sort_columns: List[Any] = effective_ts_ids.copy() if effective_ts_ids is not None else []
            sort_columns.extend([self.forecast_origin_column_name, self.time_column_name])
            columns_in_results = sort_columns + [self.forecast_column_name, self.actual_column_name]
        elif forecast_scenario == ForecastingPipelineWrapperBase._FORECAST_SCENARIO_FORECAST_QUANTILES:
            columns_in_results = [self.time_column_name]
            columns_in_results.extend(self.grain_column_list)
            columns_in_results.extend(self._quantiles)

        return columns_in_results

    def _scenario_forecast_naive(
            self,
            forecast_scenario: str,
            Xy_pred_in: pd.DataFrame,
            step: int,
            ignore_data_errors: bool,
            dict_rename_back: Optional[Dict[str, Any]],
            pred: Optional[np.ndarray] = None,
            transformed_data: Optional[np.ndarray] = None
    ) -> Tuple[Optional[np.ndarray], pd.DataFrame]:
        forecast = None
        if forecast_scenario == ForecastingPipelineWrapperBase._FORECAST_SCENARIO_ROLLING_FORECAST:
            forecast_df = self._rolling_forecast_naive(Xy_pred_in, step, ignore_data_errors)
        elif forecast_scenario == ForecastingPipelineWrapperBase._FORECAST_SCENARIO_FORECAST_QUANTILES:
            Contract.assert_non_empty(pred, "pred", log_safe=True)
            Contract.assert_non_empty(transformed_data, "transformed_data", log_safe=True)
            forecast_df = self._forecast_quantile_naive(cast(np.ndarray, pred), cast(pd.DataFrame, transformed_data))
        else:
            forecast_df = self._forecast_naive(Xy_pred_in, ignore_data_errors, dict_rename_back)
            forecast = forecast_df[TimeSeriesInternal.DUMMY_TARGET_COLUMN]
        return forecast, forecast_df

    def _scenario_forecast_automl(
            self,
            forecast_scenario: str,
            X_pred: Optional[pd.DataFrame],
            y_pred: Optional[Union[pd.DataFrame, np.ndarray]],
            Xy_pred_in: pd.DataFrame,
            ignore_data_errors: bool,
            step: int,
            dict_rename_back: Optional[Dict[str, Any]],
            forecast_destination: Optional[pd.Timestamp] = None,
            preprocessors: Optional[List[Any]] = None,
            forecaster: Optional[Any] = None,
            pred: Optional[np.ndarray] = None,
            transformed_data: Optional[np.ndarray] = None
    ) -> Tuple[Optional[np.ndarray], pd.DataFrame]:
        forecast = None
        if forecast_scenario == ForecastingPipelineWrapperBase._FORECAST_SCENARIO_ROLLING_FORECAST:
            Contract.assert_non_empty(preprocessors, "preprocessors", log_safe=True)
            forecast_df = self._pipeline_rolling_forecast_internal(
                Xy_pred_in, step, cast(List[Any], preprocessors), forecaster, ignore_data_errors)
        elif forecast_scenario == ForecastingPipelineWrapperBase._FORECAST_SCENARIO_FORECAST_QUANTILES:
            ts_transformer = self._get_not_none_ts_transformer()
            Contract.assert_non_empty(pred, "pred", log_safe=True)
            Contract.assert_non_empty(transformed_data, "transformed_data", log_safe=True)
            pred = cast(np.ndarray, pred)
            transformed_data = cast(pd.DataFrame, transformed_data)
            if ts_transformer.has_unique_target_grains_dropper:
                transformed_data, pred = ts_transformer.unique_target_grain_dropper.get_target_X_y(
                    transformed_data, pred, self.grain_column_list, is_unique_target=False
                )
            forecast_df = self._pipeline_forecast_quantiles_internal(
                X_pred, pred, transformed_data, Xy_pred_in, ignore_data_errors)
        else:
            forecast, forecast_df = self._pipeline_forecast_internal(
                X_pred, y_pred, Xy_pred_in, dict_rename_back, forecast_destination,
                ignore_data_errors, preprocessors, forecaster)
        return forecast, forecast_df

    # endregion

    def forecast(
            self,
            X_pred: Optional[pd.DataFrame] = None,
            y_pred: Optional[Union[pd.DataFrame, np.ndarray]] = None,
            forecast_destination: Optional[pd.Timestamp] = None,
            ignore_data_errors: bool = False
    ) -> Tuple[np.ndarray, pd.DataFrame]:
        """
        Do the forecast on the data frame X_pred.

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
        :returns: Y_pred, with the subframe corresponding to Y_future filled in with the respective forecasts.
                  Any missing values in Y_past will be filled by imputer.
        :rtype: tuple
        """
        _logger.info("Entring the forecast method.")
        if hasattr(self, "metadata"):
            for k, v in self.metadata.items():
                _logger.info(f'{k}: {v}')
        # Extract the preprocessors and estimator/forecaster from the internal pipeline
        preprocessors, forecaster = self._get_preprocessors_and_forecaster()
        self._update_params(preprocessors[0])

        # check the format of input
        self._check_data(X_pred, y_pred, forecast_destination)

        forecast, forecast_df = self._scenario_forecast(
            ForecastingPipelineWrapperBase._FORECAST_SCENARIO_FORECAST, X_pred, y_pred,
            forecast_destination=forecast_destination, ignore_data_errors=ignore_data_errors,
            preprocessors=preprocessors, forecaster=forecaster
        )
        Contract.assert_non_empty(forecast, "forecast")
        forecast = cast(np.ndarray, forecast)
        _logger.info("forecast method complete.")

        return forecast, forecast_df

    def _merge_forecast_result_df(
            self,
            forecast_df_list: List[pd.DataFrame],
            cols_in_result_df: Optional[List[str]],
            sort_result: Optional[bool] = False
    ) -> pd.DataFrame:
        """Merged forecast results and output the selected columns."""
        # uniform index for concat as origin column may not be presented.
        if len(forecast_df_list) == 1:
            forecast_df = forecast_df_list[0]
        else:
            all_indices_mapping = {}  # type: Dict[str, List[pd.DataFrame]]
            for df in forecast_df_list:
                indices = df.index.names
                is_pandas_default_indices = (len(indices) == 1 and indices[0] is None)
                if not is_pandas_default_indices:
                    for idx in indices:
                        if idx not in all_indices_mapping:
                            all_indices_mapping[idx] = []
                        all_indices_mapping[idx].append(df)
                # drop pandas default numeric index
                df.reset_index(inplace=True, drop=is_pandas_default_indices)
            all_indices = set(all_indices_mapping.keys())
            for df in forecast_df_list:
                missing_index = all_indices.difference(df.columns)
                if missing_index:
                    for idx in missing_index:
                        # if missing, using first known value to impute.
                        # The naive forecast result df may not the same as the normal forecast df as there is a
                        # discrepancy in the output indices between TCN forecast and automl forecast.
                        df[idx] = all_indices_mapping[idx][0].iloc(0)
                if all_indices:
                    df.set_index(list(all_indices), inplace=True, drop=True)
            forecast_df = pd.concat(forecast_df_list, sort=False)
        if cols_in_result_df:
            cols_in_result_df = list(filter(lambda x: x in forecast_df.columns, cols_in_result_df))
            forecast_df = forecast_df[cols_in_result_df]
        if sort_result:
            forecast_df.sort_values(cols_in_result_df, inplace=True, ignore_index=True)
        return forecast_df

    def forecast_quantiles(
            self,
            X_pred: Optional[pd.DataFrame] = None,
            y_pred: Optional[Union[pd.DataFrame, np.ndarray]] = None,
            quantiles: Optional[Union[float, List[float]]] = None,
            forecast_destination: Optional[pd.Timestamp] = None,
            ignore_data_errors: bool = False) -> pd.DataFrame:
        """
        Get the prediction and quantiles from the fitted pipeline.

        :param X_pred: the prediction dataframe combining X_past and X_future in a time-contiguous manner.
                       Empty values in X_pred will be imputed.
        :param y_pred: the target value combining definite values for y_past and missing values for Y_future.
                       If None the predictions will be made for every X_pred.
        :param quantiles: The list of quantiles at which we want to forecast.
        :type quantiles: float or list of floats
        :param forecast_destination: Forecast_destination: a time-stamp value.
                                     Forecasts will be made all the way to the forecast_destination time,
                                     for all grains. Dictionary input { grain -> timestamp } will not be accepted.
                                     If forecast_destination is not given, it will be imputed as the last time
                                     occurring in X_pred for every grain.
        :type forecast_destination: pandas.Timestamp
        :param ignore_data_errors: Ignore errors in user data.
        :type ignore_data_errors: bool
        :return: A dataframe containing the columns and predictions made at requested quantiles.
        """
        default_quantiles = self.quantiles
        if quantiles:
            self.quantiles = quantiles
        # First get the point forecast
        pred, transformed_data = self.forecast(X_pred, y_pred, forecast_destination, ignore_data_errors)
        _, forecast_df = self._scenario_forecast(
            ForecastingPipelineWrapperBase._FORECAST_SCENARIO_FORECAST_QUANTILES,
            X_pred, y_pred,
            forecast_destination=forecast_destination, ignore_data_errors=ignore_data_errors,
            pred=pred, transformed_data=transformed_data,
        )
        self.quantiles = default_quantiles
        return forecast_df

    def fit(self, X: pd.DataFrame, y: np.ndarray) -> 'ForecastingPipelineWrapperBase':
        """
        Fit the model with input X and y.

        :param X: Input X data.
        :param y: Input y data.
        """
        if self._get_not_none_ts_transformer().has_unique_target_grains_dropper:
            self._fit_naive(True)
        return self._pipeline_fit_internal(X, y)

    def _update_forecast_origin(self, df: pd.DataFrame) -> None:
        for grain, df_one in df.groupby(self.grain_column_list):
            self.forecast_origin[grain] = pd.Timestamp(df_one.reset_index()[self.time_column_name].values[-1])

    def _extend_internal(self, preprocessors: List[Any], forecaster: Any, X_known: pd.DataFrame,
                         ignore_data_errors: bool = False) -> Any:
        """
        Extend the forecaster on the known data if it is extendable.

        The base class implementation is a placeholder; subclasses override this method to support their
        own extension logic.
        """
        return forecaster

    def _check_data(self, X_pred: pd.DataFrame,
                    y_pred: Union[pd.DataFrame, np.ndarray],
                    forecast_destination: pd.Timestamp) -> None:
        """
        Check the user input.

        :param X_pred: the prediction dataframe combining X_past and X_future in a time-contiguous manner.
                       Empty values in X_pred will be imputed.
        :param y_pred: the target value combining definite values for y_past and missing values for Y_future.
        :param forecast_destination: Forecast_destination: a time-stamp value.
                                     Forecasts will be made all the way to the forecast_destination time,
                                     for all grains. Dictionary input { grain -> timestamp } will not be accepted.
                                     If forecast_destination is not given, it will be imputed as the last time
                                     occurring in X_pred for every grain.
        :raises: DataException

        """
        # Check types
        # types are not PII
        if X_pred is not None and not isinstance(X_pred, pd.DataFrame):
            raise ForecastingConfigException._with_error(
                AzureMLError.create(
                    InvalidArgumentType,
                    target='X_pred',
                    reference_code=ReferenceCodes._TSDF_INVALID_ARG_FC_PIPELINE_X_PRED,
                    argument='X_pred',
                    expected_types='pandas.DataFrame',
                    actual_type=str(type(X_pred))
                )
            )
        if y_pred is not None and not isinstance(y_pred, pd.DataFrame) and not isinstance(y_pred, np.ndarray):
            raise ForecastingConfigException._with_error(
                AzureMLError.create(
                    InvalidArgumentType,
                    target='y_pred',
                    reference_code=ReferenceCodes._TSDF_INVALID_ARG_FC_PIPELINE_Y_PRED,
                    argument='y_pred',
                    expected_types='numpy.array or pandas.DataFrame',
                    actual_type=str(type(y_pred))
                )
            )
        if forecast_destination is not None and not isinstance(forecast_destination, pd.Timestamp) and not isinstance(
                forecast_destination, np.datetime64):
            raise ForecastingConfigException._with_error(
                AzureMLError.create(
                    InvalidArgumentType,
                    target='forecast_destination',
                    reference_code=ReferenceCodes._TSDF_INVALID_ARG_FC_PIPELINE_FC_DES,
                    argument='forecast_destination',
                    expected_types='pandas.Timestamp, numpy.datetime64',
                    actual_type=str(type(forecast_destination))
                )
            )
        # Check wrong parameter combinations.
        if (forecast_destination is None) and (X_pred is None):
            raise ForecastingConfigException._with_error(
                AzureMLError.create(
                    TimeseriesDfInvalidArgOnlyOneArgRequired,
                    target='forecast_destination, X_pred',
                    reference_code=ReferenceCodes._TSDF_INVALID_ARG_FC_PIPELINE_NO_DESTINATION_OR_X_PRED,
                    arg1='X_pred',
                    arg2='forecast_destination'
                )
            )
        if (forecast_destination is not None) and (X_pred is not None):
            raise ForecastingConfigException._with_error(
                AzureMLError.create(
                    TimeseriesDfInvalidArgOnlyOneArgRequired,
                    target='forecast_destination, X_pred',
                    reference_code=ReferenceCodes._TSDF_INVALID_ARG_FC_PIPELINE_DESTINATION_AND_X_PRED,
                    arg1='X_pred',
                    arg2='forecast_destination'
                )
            )
        if (forecast_destination is not None) and (y_pred is not None):
            raise ForecastingConfigException._with_error(
                AzureMLError.create(
                    TimeseriesDfInvalidArgOnlyOneArgRequired,
                    target='forecast_destination, y_pred',
                    reference_code=ReferenceCodes._TSDF_INVALID_ARG_FC_PIPELINE_DESTINATION_AND_Y_PRED,
                    arg1='y_pred',
                    arg2='forecast_destination'
                )
            )
        if X_pred is None and y_pred is not None:
            # If user provided only y_pred raise the error.
            raise ForecastingConfigException._with_error(
                AzureMLError.create(
                    TimeseriesDfInvalidArgFcPipeYOnly,
                    target='X_pred, y_pred',
                    reference_code=ReferenceCodes._TSDF_INVALID_ARG_FC_PIPELINE_Y_ONLY
                )
            )

    def short_grain_handling(self) -> bool:
        """Return true if short or absent grains handling is enabled for the model."""
        return forecasting_utilities.get_pipeline_step(
            self._get_not_none_ts_transformer().pipeline, TimeSeriesInternal.SHORT_SERIES_DROPPEER) is not None

    def _lag_or_rw_enabled(self) -> bool:
        tst = self._get_not_none_ts_transformer()
        if forecasting_utilities.get_pipeline_step(
                tst.pipeline, TimeSeriesInternal.LAG_LEAD_OPERATOR):
            return True
        elif forecasting_utilities.get_pipeline_step(
                tst.pipeline, TimeSeriesInternal.ROLLING_WINDOW_OPERATOR):
            return True

        return False

    def _get_y_imputer_for_tsid(self, tsid: GrainType) -> 'TimeSeriesImputer':
        """Get the fitted target value imputer for the given time-series ID."""
        imputer = self._get_not_none_ts_transformer().y_imputers.get(tsid)
        if imputer is None:
            # Should not happen on fitted time series transformer.
            raise UntrainedModelException(
                self.FATAL_NO_TARGET_IMPUTER,
                target=self.__class__.__name__, has_pii=False)

        return imputer

    def _prepare_prediction_input_common(self,
                                         X_pred: Optional[pd.DataFrame] = None,
                                         y_pred: Optional[Union[pd.DataFrame, np.ndarray]] = None,
                                         forecast_destination: Optional[pd.Timestamp] = None,
                                         ignore_data_errors: bool = False) -> _ForecastScenarioData:
        """
        Apply data preparation steps that are common to all forecasting modes.

        Steps include: basic validation checks on the input, type conversions, aggregation (when applicable),
        and creating the initial prediction data frame with features and target values. This data frame may
        contain time index gaps and missing values and may be unsorted.
        """
        self._check_data(X_pred, y_pred, forecast_destination)
        dict_rename: Dict[Any, str] = {}
        dict_rename_back: Dict[str, Any] = {}
        if X_pred is not None:
            # Check that the grains have correct types.
            X_pred = self._check_convert_grain_types(X_pred)

            # Handle the case where both an index and column have the same name. Merge/groupby both
            # cannot handle cases where column name is also in index above version 0.23. In addition,
            # index is only accepted as a kwarg in versions >= 0.24
            pd_compatible = pd.__version__ >= '0.24.0'
            if pd_compatible:
                for ix_name in X_pred.index.names:
                    if ix_name in X_pred.columns:
                        temp_name = 'temp_{}'.format(uuid.uuid4())
                        dict_rename[ix_name] = temp_name
                        dict_rename_back[temp_name] = ix_name
                if len(dict_rename) > 0:
                    X_pred = X_pred.rename_axis(index=dict_rename)

            # Aggregate the data if necessary
            X_pred = self._convert_time_column_name_safe(X_pred, ReferenceCodes._FORECASTING_CONVERT_INVALID_VALUE)
            X_pred, y_pred = self.preaggregate_data_set(X_pred, y_pred)

        # Create the prediction data frame which includes the target
        Xy_pred = self._create_prediction_data_frame(X_pred, y_pred, forecast_destination, ignore_data_errors)

        forecast_scenario_data = _ForecastScenarioData.from_prepared_input_data(
            Xy_pred, self._get_not_none_ts_transformer(), self.grain_column_list, dict_rename_back)
        return forecast_scenario_data

    def _iterate_common_prediction_data_preparation(self, Xy_pred: pd.DataFrame,
                                                    ignore_data_errors: bool) -> Generator[
            Tuple[GrainType, pd.Timestamp, TimeSeriesDataSet], None, None]:
        """
        Apply data preparation steps per-timeseries that are common to all forecasting modes.

        This method operates on the initial prediction data frame produced by _prepare_prediction_input_common
        and does the following steps per-timeseries: check for, and exclude, series missing from the training record,
        time-sort the data, check if forecasting period overlaps the training period, fill any gaps in the time index
        all the way back to expected start of the forecasting period, and mark rows with missing target values.
        The gap filling also includes frequency alignment checks and attempts to work around misaligned rows
        using the frequency fixer module.

        On each iteration, this method yields a tuple of the series ID, start time of the user input, and
        TimeSeriesDataSet object containing the prepared series. Downstream per-series preparation can then
        loop over the output to ensure the data contract enforced by this method.
        """
        ts_transformer = self._get_not_none_ts_transformer()
        time_misalign_reported = False
        for tsid, df_one in Xy_pred.groupby(self.grain_column_names):
            # If the grain is categorical, groupby may result in the empty
            # data frame. If it is the case, skip it.
            if df_one.shape[0] == 0:
                continue

            if self.forecast_origin.get(tsid) is None:
                if not self.short_grain_handling():
                    # Throw generic error about missing series if no short series handling
                    raise ForecastingDataException._with_error(
                        AzureMLError.create(TimeseriesGrainAbsentNoGrainInTrain, target='X_pred',
                                            reference_code=ReferenceCodes._TS_GRAIN_ABSENT_MDL_WRP_CHK_GRAIN,
                                            grain=tsid)
                    )
                continue

            expected_start = self.forecast_origin[tsid] + self.data_frequency

            # Make a TimeSeriesDataSet for further processing
            # Validate the data to ensure required columns are present and index is unique
            tsds_one = TimeSeriesDataSet(df_one, time_column_name=ts_transformer.time_column_name,
                                         time_series_id_column_names=ts_transformer.grain_column_names,
                                         target_column_name=ts_transformer.target_column_name)
            tsds_one.data.sort_index(inplace=True)
            input_start_time = tsds_one.time_index[0]

            # Error when input start is in the training period
            if expected_start > input_start_time:
                raise ForecastingDataException._with_error(
                    AzureMLError.create(
                        TimeseriesWrongShapeDataEarlyDest,
                        target='X_pred',
                        reference_code=ReferenceCodes._TS_WRONG_SHAPE_FATAL_EARLY_DESTINATION2
                    )
                )

            # Fill observation gaps with missing values, includes train/test gap if present
            try:
                tsds_one = tsds_one.fill_datetime_gap(freq=self.data_frequency, origin=expected_start)
            except ForecastingDataException as exc:
                # If failure is due to frequency misalignment. Attempt to fix it and try filling gaps again.
                if exc.error_code == TimeseriesDfFrequencyError().code:
                    if not time_misalign_reported:
                        self._warn_or_raise(ForecastPredictionTimesMisaligned,
                                            ReferenceCodes._FORECAST_PRED_DATA_TIMES_MISALIGNED,
                                            ignore_data_errors)
                        time_misalign_reported = True
                    df_one_fixed = fix_df_frequency(
                        tsds_one.data.reset_index(),
                        tsds_one.time_column_name,
                        tsds_one.time_series_id_column_names,
                        self.forecast_origin,
                        self.data_frequency)
                    if df_one_fixed.empty:
                        raise ForecastingDataException._with_error(
                            AzureMLError.create(
                                TimeseriesDfDatesOutOfPhase, target='X_pred',
                                reference_code=ReferenceCodes._TSDS_PRED_DATA_FREQ_OUT_OF_PHASE)
                        )
                    tsds_one = tsds_one.from_data_frame_and_metadata(df_one_fixed)
                    input_start_time = tsds_one.time_index[0]
                    tsds_one = tsds_one.fill_datetime_gap(freq=self.data_frequency, origin=expected_start)
                else:
                    raise

            # Mark observations with missing target values
            # for correct featurization e.g. with lag-by-occurrence
            tsds_one = ts_transformer._init_missing_y().fit_transform(tsds_one)

            yield tsid, input_start_time, tsds_one

    def _prepare_prediction_data_for_rolling_forecast(self,
                                                      Xy_pred: pd.DataFrame,
                                                      ignore_data_errors: bool = False,
                                                      deprecated_rolling_forecast: bool = False) -> pd.DataFrame:
        """
        Apply data preparation steps per-series that are necessary for rolling forecasts.

        This method operates on the initial prediction data frame produced by _prepare_prediction_input_common
        and does the following steps per-timeseries: run all per-series preparations from
        _iterate_common_prediction_data_preparation, check for gaps between the train (or train+valid) period
        and the test periods, and impute all missing target values in the prediction data.

        When there is a gap prior to the test set or there are missing, or non-contiguous, target values in the input,
        this method will either raise an exception or print a warning depending on the `ignore_data_errors` value.
        """
        is_reported = False
        df_pred_list: List[pd.DataFrame] = []
        for tsid, input_start_time, tsds_one in self._iterate_common_prediction_data_preparation(Xy_pred,
                                                                                                 ignore_data_errors):
            # Error or warn for missing target values
            expected_start = self.forecast_origin[tsid] + self.data_frequency
            has_gap = expected_start < input_start_time
            # Temporary hack for printing different gap error msgs for DNN and non-DNN model wrappers.
            # DNN Wrapper appends validation data in train-valid, while non-DNN does not.
            # This behavior should be reconciled, but in the meantime make sure we give informative errors.
            data_period = 'training + validation' if hasattr(self, '_data_for_inference') else 'training'
            if not deprecated_rolling_forecast and not is_reported and not self.is_grain_dropped(tsid):
                if has_gap:
                    self._warn_or_raise(TimeseriesNoDataContext,
                                        ReferenceCodes._ROLLING_FORECAST_TRAIN_TEST_GAP,
                                        ignore_data_errors, method='rolling_forecast()',
                                        data_period=data_period)
                    is_reported = True
                elif np.any(pd.isnull(tsds_one.data[tsds_one.target_column_name])):
                    self._warn_or_raise(RollingForecastMissingTargetValues,
                                        ReferenceCodes._ROLLING_FORECAST_TARGET_MISSING_VALUES,
                                        ignore_data_errors)
                    is_reported = True
            elif deprecated_rolling_forecast and not is_reported:
                if has_gap and self._lag_or_rw_enabled() and not self.is_grain_dropped(tsid):
                    self._warn_or_raise(TimeseriesNoDataContext,
                                        ReferenceCodes._ROLLING_EVALUATION_TRAIN_TEST_GAP,
                                        ignore_data_errors, method='rolling_evaluation()',
                                        data_period=data_period)
                    is_reported = True

            # Impute all missing target values
            tsds_one = self._get_y_imputer_for_tsid(tsid).transform(tsds_one)
            df_pred_list.append(tsds_one.data)

        Xy_pred_final = pd.concat(df_pred_list, sort=False)
        Xy_pred_final.reset_index(inplace=True)

        return Xy_pred_final

    def _apply_preprocessors(self, preprocessors: List[Any], X: pd.DataFrame,
                             select_latest_origin_times: bool = True) -> Tuple[Union[pd.DataFrame, np.ndarray],
                                                                               pd.DataFrame]:
        """
        Apply the given preprocessors in sequence to the input data.

        In case there are preprocessors in addition to a TimeSeriesTransformer, this method returns the output
        from all transforms, which may be a numpy array, and also the DataFrame output from the TimeSeriesTransformer
        so that the timeseries features can be used in downstream post-processing.
        """
        # Pre processing.
        X_ts_features = pd.DataFrame()
        y_known_series = pd.Series(dtype=np.float64)
        for preproc in preprocessors:
            # FIXME: Work item #400231
            if type(preproc).__name__ == 'TimeSeriesTransformer':
                X_ts_features = preproc.transform(X)
                # We do not need the target column now.
                # The target column is deleted by the rolling window during transform.
                # If there is no rolling window we need to make sure the column was dropped.
                # if preproc.target_column_name in test_feats.columns:
                Contract.assert_true(preproc.target_column_name in X_ts_features.columns,
                                     'Expected the target column in the transformed features', log_safe=True)
                # We want to store the y_known_series for future use.
                y_known_series = X_ts_features.pop(preproc.target_column_name)

                # If origin times are present, remove nans from look-back features and select the latest origins
                if preproc.origin_column_name in X_ts_features.index.names:
                    y = np.zeros(X_ts_features.shape[0])
                    X_ts_features, y = preproc._remove_nans_from_look_back_features(X_ts_features, y)
                    if select_latest_origin_times:
                        X_ts_features = preproc._select_latest_origin_dates(X_ts_features)
                X = X_ts_features.copy()
            else:
                X = preproc.transform(X)

        try:
            X_ts_features[self.target_column_name] = y_known_series
        except Exception as e:
            raise InvalidOperationException._with_error(
                AzureMLError.create(
                    AutoMLInternalLogSafe, error_message='Unable to append target column to input DataFrame.',
                    error_details=str(e),
                    inner_exception=e
                )
            )
        return X, X_ts_features

    def _pipeline_rolling_forecast_internal(
            self,
            Xy_pred_in: pd.DataFrame,
            step: int,
            preprocessors: List[Any],
            forecaster: Any,
            ignore_data_errors: bool
    ) -> pd.DataFrame:
        Xy_pred = self._prepare_prediction_data_for_rolling_forecast(Xy_pred_in, ignore_data_errors=ignore_data_errors)

        # Apply the TimeSeriesTransformer to generate features/impute missing feature values
        # Don't select origin times here as this is done within the rolling forecast loop instead
        _, Xy_ts_features = self._apply_preprocessors(
            preprocessors[:1], Xy_pred, select_latest_origin_times=False)

        # Call internal method for generating rolling forecasts; base classes must implement this method
        X_fcst = self._rolling_forecast_internal(
            preprocessors[1:], forecaster, Xy_ts_features, step, ignore_data_errors)

        expected_columns = set([self.time_column_name, self.forecast_origin_column_name,
                                self.forecast_column_name] + self.grain_column_list)
        Contract.assert_true(expected_columns == set(X_fcst.columns),
                             'Unexpected columns in rolling_forecasting_internal output', log_safe=True)

        # Post-process the rolling forecasts
        # Join with provided actuals
        Xy_pred_in.rename(columns={self.target_column_name: self.actual_column_name}, inplace=True)
        Xy_pred_in = Xy_pred_in[self.grain_column_list + [self.time_column_name, self.actual_column_name]]
        X_fcst = X_fcst.merge(Xy_pred_in, how='inner')

        return X_fcst

    def rolling_forecast(self, X_pred: pd.DataFrame, y_pred: np.ndarray, step: int = 1,
                         ignore_data_errors: bool = False) -> pd.DataFrame:
        """
        Produce forecasts on a rolling origin over a test set.

        Each iteration makes a forecast of maximum horizon periods ahead
        using information up to the current origin, then advances the origin by 'step' time periods.
        The prediction context for each forecast is set so
        that the forecaster uses the actual target values prior to the current
        origin time for constructing lookback features.

        This function returns a DataFrame of rolling forecasts joined
        with the actuals from the test set. The columns in the returned data frame are as follows:
        * Timeseries ID columns (Optional). When supplied by the user, the given column names will be used.
        * Forecast origin column giving the origin time for each row.
          Column name: stored as the object member variable forecast_origin_column_name.
        * Time column. The column name given by the user will be used.
        * Forecast values column. Column name: stored as the object member forecast_column_name
        * Actual values column. Column name: stored as the object member actual_column_name

        :param X_pred: Prediction data frame
        :type X_pred: pd.DataFrame
        :param y_pred: target values corresponding to rows in  X_pred
        :type y_pred: np.ndarray
        :param step: Number of periods to advance the forecasting window in each iteration.
        :type step: int
        :param ignore_data_errors: Ignore errors in user data.
        :type ignore_data_errors: bool

        :returns: Data frame of rolling forecasts
        :rtype: pd.DataFrame
        """
        Validation.validate_type(step, 'step', int)
        if step < 1 or step > self.max_horizon:
            raise ValidationException._with_error(
                AzureMLError.create(
                    ArgumentOutOfRange, argument_name='step', min=1, max=self.max_horizon,
                    target='rolling_forecast')
            )

        # Extract the preprocessors and estimator/forecaster from the internal pipeline
        preprocessors, forecaster = self._get_preprocessors_and_forecaster()

        # Ensure that the preproc list starts with a ts_transformer
        # This is/has always been the case
        preproc_check = len(preprocessors) > 0 and type(preprocessors[0]).__name__ == 'TimeSeriesTransformer'
        Contract.assert_true(preproc_check, 'Expected TimeseriesTransformer to be first in the preprocessor list.',
                             log_safe=True)

        # Initialize object parameters from the TimeSeriesTransformer preprocessor
        self._update_params(preprocessors[0])

        # Prepare input data
        self._check_data_rolling_evaluation(X_pred, y_pred, ignore_data_errors,
                                            ReferenceCodes._ROLLING_FORECAST_NO_Y)
        _, forecast_df = self._scenario_forecast(
            ForecastingPipelineWrapperBase._FORECAST_SCENARIO_ROLLING_FORECAST,
            X_pred, y_pred,
            forecast_destination=None, ignore_data_errors=ignore_data_errors, step=step,
            forecaster=forecaster, preprocessors=preprocessors
        )

        return forecast_df

    def rolling_evaluation(self,
                           X_pred: pd.DataFrame,
                           y_pred: Union[pd.DataFrame,
                                         np.ndarray],
                           ignore_data_errors: bool = False) -> Tuple[np.ndarray, pd.DataFrame]:
        """"
        Produce forecasts on a rolling origin over the given test set.

        Each iteration makes a forecast for the next 'max_horizon' periods
        with respect to the current origin, then advances the origin by the
        horizon time duration. The prediction context for each forecast is set so
        that the forecaster uses the actual target values prior to the current
        origin time for constructing lag features.

        This function returns a concatenated DataFrame of rolling forecasts joined
        with the actuals from the test set.

        *This method is deprecated and will be removed in a future release. Please use rolling_forecast() instead.*

        :param X_pred: the prediction dataframe combining X_past and X_future in a time-contiguous manner.
                       Empty values in X_pred will be imputed.
        :param y_pred: the target value corresponding to X_pred.
        :param ignore_data_errors: Ignore errors in user data.

        :returns: Y_pred, with the subframe corresponding to Y_future filled in with the respective forecasts.
                  Any missing values in Y_past will be filled by imputer.
        :rtype: tuple
        """
        msg = 'rolling_evaluation() is deprecated and will be removed in a future release. ' \
              'Please use rolling_forecast() instead.'
        warnings.warn(msg, DeprecationWarning)

        # check data satisfying the requiring information. If not, raise relevant error messages.
        self._check_data(X_pred, y_pred, None)
        self._check_data_rolling_evaluation(X_pred, y_pred, ignore_data_errors,
                                            ReferenceCodes._ROLLING_EVALUATION_NO_Y)

        # Extract the preprocessors and estimator/forecaster from the internal pipeline
        preprocessors, forecaster = self._get_preprocessors_and_forecaster()

        # create and prepare the prediction data frame
        X_pred = self._convert_time_column_name_safe(X_pred, ReferenceCodes._FORECASTING_CONVERT_INVALID_VALUE_EV)
        X_pred, y_pred = self.preaggregate_data_set(X_pred, y_pred)
        Xy_pred = self._create_prediction_data_frame(X_pred, y_pred, None, ignore_data_errors)
        Xy_pred = self._prepare_prediction_data_for_rolling_forecast(Xy_pred,
                                                                     ignore_data_errors=ignore_data_errors,
                                                                     deprecated_rolling_forecast=True)
        X_rlt = []
        for grain_one, df_one in Xy_pred.groupby(self.grain_column_names):
            if self.is_grain_dropped(grain_one):
                continue
            if pd.isna(df_one[self.target_column_name]).any():
                df_one = self._infer_y(df_one, grain_one)
            y_pred_one = df_one[self.target_column_name].copy()
            df_one[self.target_column_name] = np.nan
            X_tmp = self._rolling_evaluation_one_grain(preprocessors, forecaster,
                                                       df_one, y_pred_one, ignore_data_errors, grain_one)
            if not X_tmp.empty:
                X_rlt.append(X_tmp)
        Contract.assert_non_empty(X_rlt, 'X_rlt')
        test_feats = pd.concat(X_rlt, sort=False)
        test_feats = self.align_output_to_input(X_pred, test_feats)
        y_pred = test_feats[TimeSeriesInternal.DUMMY_TARGET_COLUMN].values

        if self._y_transformer is not None:
            y_pred = self._y_transformer.inverse_transform(y_pred)
            y_pred = self._convert_target_type_maybe(y_pred)
            test_feats[TimeSeriesInternal.DUMMY_TARGET_COLUMN] = y_pred

        return y_pred, test_feats

    def _rolling_evaluation_one_grain(self, preprocessors: List[Any], forecaster: Any,
                                      df_pred: pd.DataFrame,
                                      y_pred: pd.Series,
                                      ignore_data_errors: bool,
                                      grain_name: GrainType) -> pd.DataFrame:
        """"
        Implement rolling_evaluation for each grain.

        :param df_pred: the prediction dataframe generated from _create_prediction_data_frame.
        :param y_pred: the target value corresponding to X_pred.
        :param ignore_data_errors: Ignore errors in user data.
        :param grain_name: The name of the grain to evaluate.
        :returns: Y_pred, with the subframe corresponding to Y_future filled in with the respective forecasts.
                  Any missing values in Y_past will be filled by imputer.
        :rtype: pandas.DataFrame
        """
        df_list = []
        X_trans = pd.DataFrame()
        start_time = df_pred[self.time_column_name].min()
        origin_time = start_time
        current_forecaster = forecaster
        while origin_time <= df_pred[self.time_column_name].max():
            # Set the horizon time - end date of the forecast
            next_valid_point = df_pred[df_pred[self.time_column_name] >= origin_time][self.time_column_name].min()
            horizon_time = next_valid_point + self.max_horizon * self.data_frequency
            # Extract test data from an expanding window up-to the horizon
            expand_wind = (df_pred[self.time_column_name] < horizon_time)
            df_pred_expand = df_pred[expand_wind]
            if origin_time != start_time:
                # Set the context by including actuals up-to the origin time
                test_context_expand_wind = (df_pred[self.time_column_name] < origin_time)
                context_expand_wind = (df_pred_expand[self.time_column_name] < origin_time)
                # add the y_pred information into the df_pred_expand dataframe.
                y_tmp = X_trans.reset_index()[TimeSeriesInternal.DUMMY_TARGET_COLUMN]
                df_pred_expand[self.target_column_name][context_expand_wind] = y_pred[
                    test_context_expand_wind].combine_first(y_tmp)
                if horizon_time != origin_time:
                    # We will include first valid test point to the gapped part to fill the
                    # datetime gap. We will infer y and remove this data point.
                    X_gap = df_pred_expand[df_pred_expand[self.time_column_name] <= next_valid_point]
                    # The part, where we do not need to infer.
                    X_nogap = df_pred_expand[df_pred_expand[self.time_column_name] >= next_valid_point]
                    X_gap = self._infer_y(X_gap, grain_name, fill_datetime_gap=True)
                    # Remove the last data point
                    X_gap = X_gap[X_gap[self.time_column_name] < next_valid_point]
                    # Glue the imputed data to the existing data frame.
                    df_pred_expand = pd.concat([X_gap, X_nogap], sort=False, ignore_index=True)

                # extend the forecaster on the current context
                X_known = df_pred_expand[df_pred_expand[self.time_column_name] < origin_time]
                current_forecaster = self._extend_internal(preprocessors, forecaster, X_known,
                                                           ignore_data_errors=ignore_data_errors)

            # Make a forecast out to the maximum horizon
            X_trans = self._forecast_internal(preprocessors, current_forecaster, df_pred_expand, ignore_data_errors)
            if not X_trans.empty:
                trans_tindex = X_trans.index.get_level_values(self.time_column_name)
                trans_roll_wind = (trans_tindex >= origin_time) & (trans_tindex < horizon_time)
                X_fcst = X_trans[trans_roll_wind]
                if not X_fcst.empty:
                    df_list.append(X_fcst)
            # Advance the origin time
            origin_time = horizon_time
        return pd.concat(df_list, sort=False) if len(df_list) > 0 else pd.DataFrame()

    def align_output_to_input(self, X_input: pd.DataFrame, transformed: pd.DataFrame) -> pd.DataFrame:
        """
        Align the transformed output data frame to the input data frame.

        *Note:* transformed will be modified by reference, no copy is being created.
        :param X_input: The input data frame.
        :param transformed: The data frame after transformation.
        :returns: The transfotmed data frame with its original index, but sorted as in X_input.
        """
        index = transformed.index.names
        # Before dropping index, we need to make sure that
        # we do not have features named as index columns.
        # we will temporary rename them.
        dict_rename = {}
        dict_rename_back = {}
        for ix_name in transformed.index.names:
            if ix_name in transformed.columns:
                temp_name = 'temp_{}'.format(uuid.uuid4())
                dict_rename[ix_name] = temp_name
                dict_rename_back[temp_name] = ix_name
        if len(dict_rename) > 0:
            transformed.rename(dict_rename, axis=1, inplace=True)
        transformed.reset_index(drop=False, inplace=True)
        merge_ix = [self.time_column_name]
        # We add grain column to index only if it is non dummy.
        if self.grain_column_list != [TimeSeriesInternal.DUMMY_GRAIN_COLUMN]:
            merge_ix += self.grain_column_list
        X_merge = X_input[merge_ix]
        # filter out unique target columns
        ts_transformer = self._get_not_none_ts_transformer()
        if ts_transformer.has_unique_target_grains_dropper:
            X_merge = ts_transformer.unique_target_grain_dropper.get_non_unique_grain(
                X_merge, self.grain_column_list
            )
        # Make sure, we have a correct dtype.
        for col in X_merge.columns:
            X_merge[col] = X_merge[col].astype(transformed[col].dtype)
        transformed = X_merge.merge(transformed, how='left', on=merge_ix)
        # return old index back
        transformed.set_index(index, inplace=True, drop=True)
        # If we have renamed any columns, we need to set it back.
        if len(dict_rename_back) > 0:
            transformed.rename(dict_rename_back, axis=1, inplace=True)
        return transformed

    def _infer_y(self,
                 X: pd.DataFrame,
                 grain: GrainType,
                 fill_datetime_gap: bool = False) -> pd.DataFrame:
        """
        The convenience method to call the imputer on target column.

        **Note:** This method is not grain-aware.
        :param X: One grain of the data frame.
        :param grain: The grain key.
        :param fill_datetime_gap: To we need to call fill_datetime_gap on data set.
        :return: The data frame with imputed values.
        """
        ts_transformer = self._get_not_none_ts_transformer()
        y_imputer = ts_transformer.y_imputers[grain]
        tsds_X = TimeSeriesDataSet(
            X,
            time_column_name=ts_transformer.time_column_name,
            time_series_id_column_names=ts_transformer.grain_column_names,
            target_column_name=ts_transformer.target_column_name)
        if fill_datetime_gap:
            tsds_X = tsds_X.fill_datetime_gap(freq=self.data_frequency)
        X = y_imputer.transform(tsds_X).data
        X.reset_index(inplace=True, drop=False)
        return X

    def _check_data_rolling_evaluation(self,
                                       X_pred: pd.DataFrame,
                                       y_pred: Union[pd.DataFrame,
                                                     np.ndarray],
                                       ignore_data_errors: bool,
                                       reference_code: str) -> None:
        """
        Check the inputs for rolling evaluation function.
        Rolling evaluation is invoked when all the entries of y_pred are definite, look_back features are enabled
        and the test length is greater than the max horizon.

        :param X_pred: the prediction dataframe combining X_past and X_future in a time-contiguous manner.
                       Empty values in X_pred will be imputed.
        :param y_pred: the target value corresponding to X_pred.
        :param ignore_data_errors: Ignore errors in user data.
        :raises: DataException
        """
        # Check basic type for X
        if not isinstance(X_pred, pd.DataFrame):
            raise DataException._with_error(
                AzureMLError.create(
                    InvalidArgumentType, target="X_pred",
                    argument='X_pred', actual_type=type(X_pred),
                    expected_types=pd.DataFrame)
            )

        # if none of y value is definite, raise errors.
        if y_pred is None:
            y_pred_unknown = True
        elif isinstance(y_pred, np.ndarray):
            y_pred_unknown = pd.isna(y_pred).all()
        else:
            y_pred_unknown = y_pred.isnull().values.all()
        if y_pred_unknown:
            # this is a fatal error, hence not ignoring data errors
            self._warn_or_raise(TimeseriesMissingValuesInY,
                                reference_code,
                                ignore_data_errors=False)

    def _warn_or_raise(
            self,
            error_definition_class: 'ErrorDefinition',
            ref_code: str,
            ignore_data_errors: bool,
            **kwargs: Any) -> None:
        """
        Raise DataException if the ignore_data_errors is False.

        :param warning_text: The text of error or warning.
        :param ignore_data_errors: if True raise the error, warn otherwise.
        """
        # All error definitions currently being passed to this function don't need any message_params.
        # Pass in error message_parameters via kwargs on `_warn_or_raise` and plumb them below, should we need to
        # create errors below with message_parameters
        error = AzureMLError.create(error_definition_class,
                                    reference_code=ref_code, **kwargs)
        if ignore_data_errors:
            warnings.warn(error.error_message)
        else:
            raise DataException._with_error(error)

    def preaggregate_data_set(
            self,
            df: pd.DataFrame,
            y: Optional[np.ndarray] = None,
            is_training_set: bool = False) -> Tuple[pd.DataFrame, Optional[np.ndarray]]:
        """
        Aggregate the prediction data set.

        **Note:** This method does not guarantee that the data set will be aggregated.
        This will happen only if the data set contains the duplicated time stamps or out of grid dates.
        :param df: The data set to be aggregated.
        :patam y: The target values.
        :param is_training_set: If true, the data represent training set.
        :return: The aggregated or intact data set if no aggregation is required.
        """
        return ForecastingPipelineWrapperBase.static_preaggregate_data_set(
            self._get_not_none_ts_transformer(),
            self.time_column_name,
            self.grain_column_list,
            df, y, is_training_set)

    @staticmethod
    def static_preaggregate_data_set(
            ts_transformer: 'TimeSeriesTransformer',
            time_column_name: str,
            grain_column_names: List[str],
            df: pd.DataFrame,
            y: Optional[np.ndarray] = None,
            is_training_set: bool = False) -> Tuple[pd.DataFrame, Optional[np.ndarray]]:
        """
        Aggregate the prediction data set.

        **Note:** This method does not guarantee that the data set will be aggregated.
        This will happen only if the data set contains the duplicated time stamps or out of grid dates.
        :param ts_transformer: The timeseries tranformer used for training.
        :param time_column_name: name of the time column.
        :param grain_column_names: List of grain column names.
        :param df: The data set to be aggregated.
        :patam y: The target values.
        :param is_training_set: If true, the data represent training set.
        :return: The aggregated or intact data set if no aggregation is required.
        """
        agg_fun = ts_transformer.parameters.get(TimeSeries.TARGET_AGG_FUN)
        set_columns = set(ts_transformer.columns) if ts_transformer.columns is not None else set()
        ext_resgressors = set(df.columns)
        ext_resgressors.discard(time_column_name)
        for grain in grain_column_names:
            ext_resgressors.discard(grain)
        diff_col = set_columns.symmetric_difference(set(df.columns))
        # We  do not have the TimeSeriesInternal.DUMMY_ORDER_COLUMN during inference time.
        diff_col.discard(TimeSeriesInternal.DUMMY_ORDER_COLUMN)
        diff_col.discard(TimeSeriesInternal.DUMMY_GRAIN_COLUMN)
        detected_types = None
        if agg_fun and ts_transformer.parameters.get(
                TimeSeries.FREQUENCY) is not None and (
                diff_col or (
                not diff_col and not ext_resgressors)):
            # If we have all the data for aggregation and input data set contains columns different
            # from the transformer was fit on, we need to check if the input data set needs to be aggregated.
            detected_types = _freq_aggregator.get_column_types(
                columns_train=list(ts_transformer.columns) if ts_transformer.columns is not None else [],
                columns_test=list(df.columns),
                time_column_name=time_column_name,
                grain_column_names=grain_column_names)

        if detected_types is None or detected_types.detection_failed:
            return df, y

        ts_data = TimeSeriesDataConfig(
            df, y, time_column_name=time_column_name,
            time_series_id_column_names=grain_column_names,
            freq=ts_transformer.freq_offset, target_aggregation_function=agg_fun,
            featurization_config=ts_transformer._featurization_config)
        # At this point we do not detect the data set frequency
        # and set it to None to perform the aggregation anyways.
        # If numeric columns are not empty we have to aggregate as
        # the training data have different columns then testing data.
        # If there is no numeric columns, we will aggregate only if
        # the data do not fit into the grid.
        # In the forecast time we also have to assume that the data frequency is the same
        # as forecast frequency.
        df_fixed, y_pred = _freq_aggregator.aggregate_dataset(
            ts_data, dataset_freq=ts_transformer.freq_offset,
            force_aggregation=ext_resgressors != set(),
            start_times=None if is_training_set else ts_transformer.dict_latest_date,
            column_types=detected_types)
        if df_fixed.shape[0] == 0:
            raise DataException._with_error(
                AzureMLError.create(
                    ForecastingEmptyDataAfterAggregation, target="X_pred",
                    reference_code=ReferenceCodes._FORECASTING_EMPTY_AGGREGATION
                )
            )
        return df_fixed, y_pred

    def _check_convert_grain_types(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Check that the grains have the correct type.

        :param X: The test data frame.
        :return: The same data frame with grain columns converted.
        """
        tst = self._get_not_none_ts_transformer()
        effective_grain = self._get_effective_time_series_ids(X)
        # Try to convert the grain type if TS transformer has learned it first.
        X = tst._convert_grain_type_safe(X)
        X, _ = convert_check_grain_value_types(
            X, None, effective_grain, tst._featurization_config.__dict__,
            ReferenceCodes._TS_VALIDATION_GRAIN_TYPE_INFERENCE)
        return X

    def _convert_time_column_name_safe(self, X: pd.DataFrame, reference_code: str) -> pd.DataFrame:
        """
        Convert the time column name to date time.

        :param X: The prediction data frame.
        :param reference_code: The reference code to be given to error.
        :return: The modified data frame.
        :raises: DataException
        """
        try:
            X[self.time_column_name] = pd.to_datetime(X[self.time_column_name])
        except Exception as e:
            raise DataException._with_error(
                AzureMLError.create(PandasDatetimeConversion, column=self.time_column_name,
                                    column_type=X[self.time_column_name].dtype,
                                    target=TimeSeries.TIME_COLUMN_NAME,
                                    reference_code=reference_code),
                inner_exception=e
            ) from e
        return X

    def _get_effective_time_series_ids(self, X_pred: pd.DataFrame) -> Optional[List[Any]]:
        """Get the list of user provided time series ID column names if they exist; otherwise, return None."""
        effective_tsids: Optional[List[Any]] = self.grain_column_list
        if self.grain_column_list[0] == TimeSeriesInternal.DUMMY_GRAIN_COLUMN and \
                self.grain_column_list[0] not in X_pred.columns:
            effective_tsids = None

        return effective_tsids

    def _create_prediction_data_frame(self,
                                      X_pred: pd.DataFrame,
                                      y_pred: Union[pd.DataFrame, np.ndarray],
                                      forecast_destination: pd.Timestamp,
                                      ignore_data_errors: bool) -> pd.DataFrame:
        """
        Create the data frame which will be used for prediction purposes.

        :param X_pred: the prediction dataframe combining X_past and X_future in a time-contiguous manner.
                       Empty values in X_pred will be imputed.
        :param y_pred: the target value combining definite values for y_past and missing values for Y_future.
        :param forecast_destination: Forecast_destination: a time-stamp value.
                                     Forecasts will be made all the way to the forecast_destination time,
                                     for all grains. Dictionary input { grain -> timestamp } will not be accepted.
                                     If forecast_destination is not given, it will be imputed as the last time
                                     occurring in X_pred for every grain.
        :param ignore_data_errors: Ignore errors in user data.
        :returns: The clean data frame.
        :raises: DataException

        """
        ts_transformer = self._get_not_none_ts_transformer()
        if X_pred is not None:
            X_copy = X_pred.copy()
            X_copy.reset_index(inplace=True, drop=True)
            if self._get_effective_time_series_ids(X_copy) is None:
                # If time series ids aren't set, processing requires a "dummy" column/id
                X_copy[TimeSeriesInternal.DUMMY_GRAIN_COLUMN] = TimeSeriesInternal.DUMMY_GRAIN_COLUMN
            # Remember the forecast origins for each grain.
            # We will trim the data frame by these values at the end.
            # Also do the sanity check if there is at least one known grain.
            has_known_grain = False
            for grain, df_one in X_copy.groupby(self.grain_column_list):
                has_known_grain = has_known_grain or grain in self.forecast_origin
            if not has_known_grain:
                raise ForecastingDataException._with_error(
                    AzureMLError.create(TimeseriesNoUsableGrains,
                                        target='X_test',
                                        reference_code=ReferenceCodes._TS_NO_USABLE_GRAINS))
            special_columns = self.grain_column_list.copy()
            special_columns.append(ts_transformer.time_column_name)
            if self.origin_col_name in X_copy.columns:
                special_columns.append(self.origin_col_name)
            if ts_transformer.group_column in X_copy.columns:
                special_columns.append(ts_transformer.group_column)
            if ts_transformer.drop_column_names:
                dropping_columns = ts_transformer.drop_column_names
            else:
                dropping_columns = []
            categorical_columns = []
            dtypes_transformer = forecasting_utilities.get_pipeline_step(
                ts_transformer.pipeline, TimeSeriesInternal.RESTORE_DTYPES)
            if dtypes_transformer is not None:
                categorical_columns = dtypes_transformer.get_non_numeric_columns()
            for column in X_copy.columns:
                if column not in special_columns and \
                        column not in dropping_columns and \
                        column not in categorical_columns and \
                        column in X_copy.select_dtypes(include=[np.number]).columns and \
                        all(np.isnan(float(var)) for var in X_copy[column].values):
                    self._warn_or_raise(TimeseriesDfContainsNaN,
                                        ReferenceCodes._FORECASTING_COLUMN_IS_NAN,
                                        ignore_data_errors)
                    break

            if y_pred is None:
                y_pred = np.repeat(np.NaN, len(X_pred))
            if y_pred.shape[0] != X_pred.shape[0]:
                # May be we need to revisit this assertion.
                raise ForecastingDataException._with_error(
                    AzureMLError.create(
                        TimeseriesWrongShapeDataSizeMismatch,
                        target='y_pred.shape[0] != X_pred.shape[0]',
                        reference_code=ReferenceCodes._TS_WRONG_SHAPE_CREATE_PRED_DF,
                        var1_name='X_pred',
                        var1_len=X_pred.shape[0],
                        var2_name='y_pred',
                        var2_len=y_pred.shape[0]
                    )
                )
            if isinstance(y_pred, pd.DataFrame):
                if ts_transformer.target_column_name not in y_pred.columns:
                    raise ForecastingConfigException._with_error(
                        AzureMLError.create(
                            MissingColumnsInData,
                            target='y_pred',
                            reference_code=ReferenceCodes._TSDF_INVALID_ARG_FC_PIPELINE_NO_TARGET_IN_Y_DF,
                            columns='target value column',
                            data_object_name='y_pred'
                        )
                    )
                X_copy = pd.merge(
                    left=X_copy,
                    right=y_pred,
                    how='left',
                    left_index=True,
                    right_index=True)
                if X_copy.shape[0] != X_pred.shape[0]:
                    raise ForecastingDataException._with_error(
                        AzureMLError.create(
                            TimeseriesWrongShapeDataSizeMismatch,
                            target='X_copy.shape[0] != X_pred.shape[0]',
                            reference_code=ReferenceCodes._TS_WRONG_SHAPE_CREATE_PRED_DF_XCPY_XPRED,
                            var1_name='X_copy',
                            var1_len=X_copy.shape[0],
                            var2_name='X_pred',
                            var2_len=X_pred.shape[0]
                        )
                    )
            elif isinstance(y_pred, np.ndarray) and X_copy.shape[0] == y_pred.shape[0]:
                X_copy[ts_transformer.target_column_name] = y_pred
            # y_pred may be pd.DataFrame or np.ndarray only, we are checking it in _check_data.
            # At that point we have generated the data frame which contains Target value column
            # filled with y_pred. The part which will need to be should be
            # filled with np.NaNs.
        else:
            # Create the empty data frame from the last date in the training set for each grain
            # and fill it with NaNs. Impute these data.
            if self.forecast_origin == {}:
                raise ForecastingDataException._with_error(
                    AzureMLError.create(TimeseriesGrainAbsentNoLastDate,
                                        target='forecast_origin',
                                        reference_code=ReferenceCodes._TS_GRAIN_ABSENT_MDL_WRP_NO_LAST_DATE)
                )
            dfs = []
            for grain_tuple in self.forecast_origin:
                if pd.Timestamp(forecast_destination) <= self.forecast_origin[grain_tuple]:
                    raise ForecastingDataException._with_error(
                        AzureMLError.create(
                            TimeseriesWrongShapeDataEarlyDest,
                            target='forecast_destination',
                            reference_code=ReferenceCodes._TS_WRONG_SHAPE_FATAL_EARLY_DESTINATION
                        )
                    )
                # Start with the next date after the last seen date.
                start_date = self.forecast_origin[grain_tuple] + self.data_frequency
                df_dict = {
                    self._time_col_name: pd.date_range(
                        start=start_date,
                        end=forecast_destination,
                        freq=ts_transformer.freq)}
                if not isinstance(grain_tuple, tuple):
                    df_dict[self.grain_column_list[0]] = grain_tuple
                else:
                    for i in range(len(self.grain_column_list)):
                        df_dict[self.grain_column_list[i]] = grain_tuple[i]
                for col in cast(List[Any], ts_transformer.columns):
                    if col not in df_dict.keys():
                        df_dict[col] = np.NaN
                # target_column_name is not in the data frame columns by
                # default.
                df_dict[ts_transformer.target_column_name] = np.NaN
                dfs.append(pd.DataFrame(df_dict))
            X_copy = pd.concat(dfs, sort=False)
            # At that point we have generated the data frame which contains target value column.
            # The data frame is filled with imputed data. Only target column is filled with np.NaNs,
            # because all gap between training data and forecast_destination
            # should be predicted.
        return X_copy

    def _get_not_none_ts_transformer(self) -> 'TimeSeriesTransformer':
        """Get the TimeSeriesTransformer from the internal pipeline or raise exception if it is missing."""
        if self._ts_transformer is None:
            raise ValidationException._with_error(AzureMLError.create(
                AutoMLInternalLogSafe, target="ForecastingPipelineWrapper",
                error_details=f'Failed to initialize ForecastingPipelineWrapper: {self.FATAL_NO_TS_TRANSFORM}')
            )
        return self._ts_transformer

    @property
    def grain_column_list(self) -> List[str]:
        if self.grain_column_names is None:
            return []
        elif isinstance(self.grain_column_names, str):
            return [self.grain_column_names]
        elif isinstance(self.grain_column_names, tuple):
            return [g for g in self.grain_column_names]
        else:
            return self.grain_column_names

    def preprocess_pred_X_y(
            self,
            X_pred: Optional[pd.DataFrame] = None,
            y_pred: Optional[Union[pd.DataFrame, np.ndarray]] = None,
            forecast_destination: Optional[pd.Timestamp] = None
    ) -> Tuple[pd.DataFrame, Union[pd.DataFrame, np.ndarray], Dict[str, Any]]:
        """Preprocess prediction X and y."""
        # Check that the grains have correct types.
        if X_pred is not None:
            X_pred = self._check_convert_grain_types(X_pred)
        # Handle the case where both an index and column have the same name. Merge/groupby both
        # cannot handle cases where column name is also in index above version 0.23. In addition,
        # index is only accepted as a kwarg in versions >= 0.24
        dict_rename = {}
        dict_rename_back = {}
        pd_compatible = pd.__version__ >= '0.24.0'
        if pd_compatible and X_pred is not None:
            for ix_name in X_pred.index.names:
                if ix_name in X_pred.columns:
                    temp_name = 'temp_{}'.format(uuid.uuid4())
                    dict_rename[ix_name] = temp_name
                    dict_rename_back[temp_name] = ix_name
            if len(dict_rename) > 0:
                X_pred.rename_axis(index=dict_rename, inplace=True)
        # If the data had to be aggregated, we have to do it here.
        if X_pred is not None:
            X_pred = self._convert_time_column_name_safe(X_pred, ReferenceCodes._FORECASTING_CONVERT_INVALID_VALUE)
            X_pred, y_pred = self.preaggregate_data_set(X_pred, y_pred)

        return X_pred, y_pred, dict_rename_back

    def _prepare_prediction_data_for_forecast(self,
                                              Xy_pred: pd.DataFrame,
                                              ignore_data_errors: bool = False) -> Tuple[pd.DataFrame,
                                                                                         pd.DataFrame,
                                                                                         bool]:
        """
        Apply data preparation steps per-series that are necessary for forecasting.

        This method operates on the initial prediction data frame produced by _prepare_prediction_input_common
        and does the following steps per-timeseries: run all per-series preparations from
        _iterate_common_prediction_data_preparation, find the latest times with known target values in case the
        user has supplied context data, check for time gaps between the training and testing periods,
        mark prediction data rows in the forecasting period as not imputed since they will be forecasted by the model,
        impute any missing target values in the context, and check if the length of the forecasting periods is longer
        than the forecaster's maximum horizon.

        A tuple is returned containing the full, prepared data, the context portion of the full data, and a boolean
        indicating if the model's maximum horizon is exceeded.
        """

        df_pred_list: List[pd.DataFrame] = []
        df_context_list: List[pd.DataFrame] = []
        max_horizon_exceeded = False
        insufficient_context_reported = False
        ts_transformer = self._get_not_none_ts_transformer()
        for tsid, input_start_time, tsds_one in self._iterate_common_prediction_data_preparation(Xy_pred,
                                                                                                 ignore_data_errors):
            pred_horizon = tsds_one.data.shape[0]
            last_known_y_date = self._get_last_y_one_grain(tsds_one.data.reset_index(), tsid,
                                                           ignore_data_errors, is_sorted=True)
            if last_known_y_date is None:
                # No context data - forecast period is defined by the input
                forecast_first_irow = tsds_one.time_index.get_loc(input_start_time)
            else:
                forecast_first_irow = tsds_one.time_index.get_loc(last_known_y_date) + 1

            # Mark targets with dates in the prediction range as not-missing
            not_imputed_val = ts_transformer._init_missing_y().MARKER_VALUE_NOT_MISSING
            missing_target_column_name = ts_transformer.target_imputation_marker_column_name
            missing_target_icol = tsds_one.data.columns.get_loc(missing_target_column_name)
            tsds_one.data.iloc[forecast_first_irow:, missing_target_icol] = not_imputed_val

            df_context_one = tsds_one.data.iloc[:forecast_first_irow]
            if not df_context_one.empty:
                # Check if user provided enough context
                expected_start = self.forecast_origin[tsid] + self.data_frequency
                has_gap = expected_start < input_start_time
                if has_gap and not insufficient_context_reported and self._lag_or_rw_enabled() and \
                        not self.is_grain_dropped(tsid):
                    lookback_horizon = max([max(self.target_lags), self.target_rolling_window_size])
                    context_missing_tail = \
                        df_context_one[missing_target_column_name].iloc[-lookback_horizon:].to_numpy()
                    if np.any(context_missing_tail != not_imputed_val):
                        self._warn_or_raise(TimeseriesNoDataContext,
                                            ReferenceCodes._FORECASTING_NO_DATA_CONTEXT,
                                            ignore_data_errors, method='forecast()',
                                            data_period='training')
                        insufficient_context_reported = True

                # Impute target values on the context data, but not in the forecast period
                df_fcst_one = tsds_one.data.iloc[forecast_first_irow:]
                tsds_context_one = tsds_one.from_data_frame_and_metadata(df_context_one)
                df_context_one = self._get_y_imputer_for_tsid(tsid).transform(tsds_context_one).data
                pred_horizon -= df_context_one.shape[0]
                df_context_list.append(df_context_one)
                df_pred_one = pd.concat([df_context_one, df_fcst_one], sort=False)
            else:
                df_pred_one = tsds_one.data
            df_pred_list.append(df_pred_one)
            max_horizon_exceeded = max_horizon_exceeded or pred_horizon > self.max_horizon

        Contract.assert_non_empty(df_pred_list, 'df_pred_list', log_safe=True)
        Xy_pred_final = pd.concat(df_pred_list, sort=False)
        Xy_pred_final.reset_index(inplace=True)
        Xy_context = pd.DataFrame()
        if len(df_context_list) > 0:
            Xy_context = pd.concat(df_context_list, sort=False)
            Xy_context.reset_index(inplace=True)
        return Xy_pred_final, Xy_context, max_horizon_exceeded

    def _get_last_y_one_grain(
            self,
            df_grain: pd.DataFrame,
            grain: GrainType,
            ignore_data_errors: bool,
            ignore_errors_and_warnings: bool = False,
            is_sorted: bool = False) -> Optional[pd.Timestamp]:
        """
        Get the date for the last known y.

        This y will be used in transformation, but will not be used
        in prediction (the data frame will be trimmed).
        :param df_grain: The data frame corresponding to single grain.
        :param ignore_data_errors: Ignore errors in user data.
        :param ignore_errors_and_warnings : Ignore the y-related errors and warnings.
        :param is_sorted: Indicates if the input DataFrame is sorted by time or not.
        :returns: The date corresponding to the last known y or None.
        """
        # We do not want to show errors for the grains which will be dropped.
        is_absent_grain = self.short_grain_handling() and grain not in self.forecast_origin.keys()
        # Make sure that frame is sorted by the time index.
        if not is_sorted:
            df_grain.sort_values(by=[self._time_col_name], inplace=True)
        y = df_grain[TimeSeriesInternal.DUMMY_TARGET_COLUMN].values
        sel_null_y = pd.isnull(y)
        num_null_y = sel_null_y.sum()
        if num_null_y == 0:
            # All y are known - nothing to forecast
            if not is_absent_grain and not ignore_errors_and_warnings:
                self._warn_or_raise(TimeseriesNothingToPredict,
                                    ReferenceCodes._FORECASTING_NOTHING_TO_PREDICT,
                                    ignore_data_errors)
            return df_grain[self._time_col_name].max()
        elif num_null_y == y.shape[0]:
            # We do not have any known y
            return None
        elif not sel_null_y[-1]:
            # There is context at the end of the y vector.
            # This could lead to unexpected behavior, so consider that this case means there is nothing to forecast
            if not is_absent_grain and not ignore_errors_and_warnings:
                self._warn_or_raise(TimeseriesContextAtEndOfY,
                                    ReferenceCodes._FORECASTING_CONTEXT_AT_END_OF_Y,
                                    ignore_data_errors)

        # Some y are known, some are not.
        # Are the data continguous - i.e. are there gaps in the context?
        non_nan_indices = np.flatnonzero(~sel_null_y)
        if not is_absent_grain and not ignore_errors_and_warnings \
           and not np.array_equiv(np.diff(non_nan_indices), 1):
            self._warn_or_raise(TimeseriesNonContiguousTargetColumn,
                                ReferenceCodes._FORECASTING_DATA_NOT_CONTIGUOUS,
                                ignore_data_errors)
        last_date = df_grain[self._time_col_name].iloc[non_nan_indices.max()]

        return pd.Timestamp(last_date)

    def _extend_transformed(self, forecaster: Any,
                            X_known_transformed: pd.DataFrame, y_known_transformed: np.ndarray) -> None:
        """
        Extend the forecaster on the tranformed known data.

        This method extends the input forecaster in-place.
        """
        if isinstance(forecaster, _MultiGrainForecastBase):
            forecaster.extend(X_known_transformed, y_known_transformed)
        elif isinstance(forecaster, (PreFittedSoftVotingRegressor, StackEnsembleRegressor)):
            self._extend_ensemble(forecaster, X_known_transformed, y_known_transformed)

    def _extend_ensemble(self, model_obj: Any, X_context: pd.DataFrame, y_context: np.ndarray) -> None:
        """Extend an ensemble model that contains a least one extendable model."""
        Contract.assert_type(model_obj, 'model_obj', (PreFittedSoftVotingRegressor, StackEnsembleRegressor))
        for forecaster in self._get_estimators_in_ensemble(model_obj):
            if isinstance(forecaster, _MultiGrainForecastBase):
                forecaster.extend(X_context, y_context)

    def _get_estimators_in_ensemble(self, model_obj: Any) -> List[Any]:
        """Get a list of estimator objects in a Voting or Stack Ensemble."""
        Contract.assert_type(model_obj, 'model_obj', (PreFittedSoftVotingRegressor, StackEnsembleRegressor))
        estimator_list: List[Any] = []
        if isinstance(model_obj, PreFittedSoftVotingRegressor):
            pline_tuple_list = model_obj._wrappedEnsemble.estimators
        else:
            pline_tuple_list = model_obj._base_learners
        for _, pline in pline_tuple_list:
            Contract.assert_type(pline, 'pipeline', SKPipeline)
            estimator_list.append(pline.steps[-1][1])
        return estimator_list

    def _model_is_extendable(self, model_obj: Any) -> bool:
        """Determine if a given model can be extended."""
        if isinstance(model_obj, (PreFittedSoftVotingRegressor, StackEnsembleRegressor)):
            return any(isinstance(forecaster, _MultiGrainForecastBase)
                       for forecaster in self._get_estimators_in_ensemble(model_obj))
        else:
            return isinstance(model_obj, _MultiGrainForecastBase)

    # region Naive Forecaster related methods.
    def _fit_naive(self, on_validation_data: bool = False) -> 'ForecastingPipelineWrapperBase':
        """
        Fit the result on the naive part.

        :param on_validation_data: The test predictions will come from the latest observations in the validation set.
        """
        ts_transformer = self._get_not_none_ts_transformer()
        if self._naive_model is None:
            self._naive_model = Naive(ts_transformer.parameters, ts_transformer.freq, allow_extend_missing_X=True)
        if on_validation_data and ts_transformer.unique_target_grain_dropper.last_validation_X_y[0] is not None:
            last_X, last_y = ts_transformer.unique_target_grain_dropper.last_validation_X_y
        else:
            last_X, last_y = ts_transformer.unique_target_grain_dropper.last_X_y
        Contract.assert_non_empty(last_X, "last_X")
        Contract.assert_non_empty(last_y, "last_y")
        last_X = cast(pd.DataFrame, last_X)
        last_y = cast(np.ndarray, last_y)
        self._update_forecast_origin(last_X)
        self._naive_model.fit(last_X, last_y)
        return self

    def _forecast_naive(
            self,
            Xy_pred_in: pd.DataFrame,
            ignore_data_errors: bool,
            dict_rename_back: Optional[Dict[str, Any]] = None
    ) -> Optional[pd.DataFrame]:
        """Get the forecast result using naive forecaster."""
        if self._naive_model is None:
            self._fit_naive(True)
        self._naive_model = cast(Naive, self._naive_model)

        # No unique target grains passed in.
        if Xy_pred_in.empty:
            return None
        Xy_pred, Xy_known, _ = self._prepare_prediction_data_for_forecast(
            Xy_pred_in, ignore_data_errors=ignore_data_errors)
        if not Xy_known.empty:
            X_context = Xy_known.copy()
            y_context = X_context.pop(TimeSeriesInternal.DUMMY_TARGET_COLUMN)
            self._naive_model.extend(X_context, y_context)

        # If all the input Xy are known.
        if Xy_pred.empty:
            return None

        predict = self._naive_model.predict(Xy_pred)
        Xy_pred[TimeSeriesInternal.DUMMY_TARGET_COLUMN] = predict

        if dict_rename_back:
            Xy_pred.rename_axis(index=dict_rename_back, inplace=True)

        return Xy_pred

    def _forecast_quantile_naive(
            self,
            pred: np.ndarray,
            transformed_data: pd.DataFrame
    ) -> pd.DataFrame:
        """Get the forecast quantile results from naive forecaster."""
        ts_transformer = self._get_not_none_ts_transformer()
        if not ts_transformer.has_unique_target_grains_dropper:
            return pd.DataFrame()
        df, pred = ts_transformer.unique_target_grain_dropper.get_target_X_y(
            transformed_data, pred, self.grain_column_list, is_unique_target=True
        )
        for col in self._quantiles:
            df[col] = pred
        df.reset_index(inplace=True)
        return df

    def _rolling_forecast_naive(
            self,
            Xy_pred_in: pd.DataFrame,
            step: int,
            ignore_data_errors: bool
    ) -> pd.DataFrame:
        index_cols = [self.time_column_name]
        index_cols.extend(self.grain_column_list)
        Xy_pred_in.set_index(index_cols, inplace=True, drop=True)

        return self._forecaster_rolling_forecast([], self._naive_model, Xy_pred_in, step)

    def _convert_target_type_maybe(self, y: np.ndarray) -> np.ndarray:
        """
        Convert the target type transform .

        :param y: The target to undergo type transform.
        :return: The modified target.
        """
        if self._y_transformer is None:
            return y
        if isinstance(self._y_transformer, SKPipeline) and self._y_transformer.pipeline is not None:
            target_type_transformer = forecasting_utilities.get_pipeline_step(
                self._y_transformer.pipeline,
                TimeSeriesInternal.TARGET_TYPE_TRANSFORMER_NAME
            )
        else:
            # In this case, _y_transformer is not a SKPipeline, it is TargetTypeTransformer.
            target_type_transformer = self._y_transformer
        if target_type_transformer is not None:
            y = target_type_transformer.inverse_transform(y, convert_type=True)
        return y

    @staticmethod
    def _adjust_forecast(test_feats: pd.DataFrame,
                         adjust_dict: Dict[str, List[Any]],
                         target_column: str,
                         time_column_name: str,
                         grain_names: Optional[List[str]] = None,
                         first_horizon_end_date: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """Adjust the forecast result based on the adjustment dictionary"""

        # If the adjustment dictionary is empty, return the original forecast result.
        if not adjust_dict:
            return test_feats

        adjust_df = pd.DataFrame(data=adjust_dict[TimeSeriesInternal.GRAIN_VALUE_LIST],
                                 columns=adjust_dict[TimeSeriesInternal.GRAIN_NAME])
        adjust_df[TimeSeriesInternal.ADJUSTMENT] = adjust_dict[TimeSeriesInternal.ADJUSTMENT]

        for grain_col in adjust_dict[TimeSeriesInternal.GRAIN_NAME]:
            Contract.assert_true(grain_col in adjust_df.columns, "Grain column missing",
                                 reference_code=ReferenceCodes._TS_GRAIN_ABSENT_ADJUSTMENT)
            Contract.assert_true(grain_col in test_feats.reset_index().columns, "Grain column missing",
                                 reference_code=ReferenceCodes._TS_GRAIN_ABSENT_FORECAST)
            try:
                if grain_col in test_feats.index.names:
                    adjust_df[grain_col] = adjust_df[grain_col].astype(
                        test_feats.index.get_level_values(grain_col).dtype)
                else:
                    adjust_df[grain_col] = adjust_df[grain_col].astype(test_feats.dtypes[grain_col])
            except BaseException:
                raise ForecastingDataException._with_error(
                      AzureMLError.create(TimeseriesCustomFeatureTypeConversion,
                                          target="ForecastingPipelineWrapper",
                                          error_details=f'Failed type convertion ForecastingPipelineWrapper:\
                                          {adjust_df[grain_col]}'))
        test_feats_adjusted = pd.merge(test_feats.reset_index(),
                                       adjust_df,
                                       on=adjust_dict[TimeSeriesInternal.GRAIN_NAME],
                                       how='left')
        # For rolling forecast, adjustment is only applied to the first horizon
        if first_horizon_end_date is not None:
            test_feats_adjusted = pd.merge(test_feats_adjusted, first_horizon_end_date,
                                           on=adjust_dict[TimeSeriesInternal.GRAIN_NAME],
                                           how="left")
            is_beyond_first_horizon = test_feats_adjusted[time_column_name] > \
                test_feats_adjusted[TimeSeriesInternal.HORIZON_ONE_END_DATE]
            test_feats_adjusted[TimeSeriesInternal.ADJUSTMENT] = np.where(
                is_beyond_first_horizon, 0, test_feats_adjusted[TimeSeriesInternal.ADJUSTMENT])
        test_feats_adjusted[TimeSeriesInternal.ADJUSTMENT].fillna(0, inplace=True)
        adjustment = test_feats_adjusted[TimeSeriesInternal.ADJUSTMENT].to_numpy()
        # Updating the target with the adjustment factor
        if any(adjustment):
            adjusted_fcst = test_feats_adjusted[target_column] - test_feats_adjusted[TimeSeriesInternal.ADJUSTMENT]
            test_feats[target_column] = adjusted_fcst.to_numpy()
        return test_feats

    @staticmethod
    def _adjust_forecast_rolling(df_fcst_list: list,
                                 adj_dict: Dict[GrainType, float],
                                 forecast_column_name: str,
                                 grain_names: list,
                                 time_column_name: str) -> list:
        """ Adjusts the forecast of the first horizon for rolling forecasts.

        :param df_fcst_list: The list of forecast dataframes.
        :param adj_dict: The adjustment dictionary.
        :param forecast_column_name: The forecast column name.
        :param grain_names: The grain names.
        :param time_column_name: The time column name.
        """
        if len(df_fcst_list) > 0:
            first_horizon_end_dt = df_fcst_list[0].groupby(grain_names)[time_column_name].max().reset_index()
            first_horizon_end_dt.rename(columns={time_column_name: TimeSeriesInternal.HORIZON_ONE_END_DATE},
                                        inplace=True)
            for itr in range(len(df_fcst_list)):
                df_fcst_list[itr] = ForecastingPipelineWrapperBase._adjust_forecast(df_fcst_list[itr],
                                                                                    adj_dict,
                                                                                    forecast_column_name,
                                                                                    time_column_name,
                                                                                    grain_names,
                                                                                    first_horizon_end_dt)
        return df_fcst_list

    @property
    def y_min_dict(self) -> Dict[str, float]:
        """Return the dictionary with minimal target values by time series ID"""
        return self._ts_transformer.y_min_dict

    @property
    def y_max_dict(self) -> Dict[str, float]:
        """Return the dictionary with maximal target values by time series ID"""
        return self._ts_transformer.y_max_dict

    # end region

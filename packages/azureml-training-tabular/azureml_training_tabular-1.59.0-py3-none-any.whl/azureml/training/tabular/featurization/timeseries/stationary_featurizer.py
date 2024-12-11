# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
Differencing the data.
"""

from typing import Optional, List, Dict, Union
import numpy as np
import pandas as pd
import logging

from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared import logging_utilities as log_utils
from azureml.automl.core.shared.constants import TelemetryConstants
from azureml.automl.core.shared.logging_utilities import function_debug_log_wrapped
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    TimeseriesFeaturizerFitNotCalled,
    TimeseriesInputIsNotTimeseriesDs,
    TimeSeriesUnsupportedTimeSequenceForStationaryFeaturizer)
from azureml.automl.core.shared.types import GrainType
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.shared.exceptions import DataException, ClientException
from azureml.automl.core.shared.forecasting_exception import ForecastingDataException

from ._grain_based_stateful_transformer import _GrainBasedStatefulTransformer
from .missingdummies_transformer import MissingDummiesTransformer
from .._azureml_transformer import AzureMLTransformer
from ..._constants import TimeSeriesInternal
from ...timeseries._time_series_data_set import TimeSeriesDataSet

logger = logging.getLogger(__name__)


class StationaryFeaturizer(AzureMLTransformer, _GrainBasedStatefulTransformer):
    """Make non-stationary data to stationary."""

    def __init__(self,
                 non_stationary_time_series_ids: List[GrainType],
                 columns_to_be_processed: List[Optional[str]],
                 max_horizon: int = 0,
                 lagging_length: int = 0,
                 ) -> None:
        """
        Constructor for StationaryFeaturizer.

        :param non_stationary_time_series_ids: list of non-stationary time series ids to be made stationary
        :type non_stationary_time_series_ids: list
        :param columns_to_be_processed: list of names of columns to be made stationary
        :type columns_to_be_processed: list
        :param max_horizon: number of horizon
        :type max_horizon: integer
        :param lagging_length: number of lagging length
        :type lagging_length: integer
        """

        super().__init__()
        self.non_stationary_time_series_ids = non_stationary_time_series_ids
        self.columns_to_be_processed = columns_to_be_processed
        # Start dates of fitted data for per grain.
        self.start_values = {}  # type: Dict[GrainType, List[pd.DataFrame]]
        # Last dates of fitted data for per grain.
        self.last_values = {}  # type: Dict[GrainType, pd.DataFrame]
        self._is_fit = False
        self._imputation_target_marker = MissingDummiesTransformer.get_column_name(
            TimeSeriesInternal.DUMMY_TARGET_COLUMN)
        self._do_stationarization = True
        self._lagging_length = lagging_length  # type: int
        self.max_horizon = max_horizon

    @property
    def do_stationarization(self) -> bool:
        """Return if we have to do stationarization."""
        return self._do_stationarization

    @property
    def lagging_length(self) -> int:
        """Return lagging length."""
        return self._lagging_length

    def _get_date(
        self,
        grain: GrainType,
        data: Union[Dict[GrainType, pd.Series], Dict[GrainType, List[pd.Series]]],
        time_col_name: str,
        is_last_dates: bool = False
    ) -> Optional[pd.Timestamp]:

        df = data.get(grain)
        if df is None:
            return None
        if is_last_dates and isinstance(df, pd.Series):
            return df[time_col_name]
        else:
            return df[0][time_col_name]

    def get_last_dates(self, grain: GrainType, time_col_name: str) -> Optional[pd.Timestamp]:
        return self._get_date(grain, self.last_values, time_col_name, True)

    def get_start_dates(self, grain: GrainType, time_col_name: str) -> Optional[pd.Timestamp]:
        return self._get_date(grain, self.start_values, time_col_name)

    @function_debug_log_wrapped(logging.INFO)
    def fit(self,
            x: TimeSeriesDataSet,
            y: Optional[np.ndarray] = None) -> 'StationaryFeaturizer':
        """
        Fit function for StationaryFeaturizer.

        :param x: Input data.
        :type x: azureml.automl.runtime._time_series_data_set.TimeSeriesDataSet object.
        :param y: Unused.
        :type y: numpy.ndarray
        :return: Class object itself.
        """
        with log_utils.log_activity(logger, activity_name=TelemetryConstants.RUN_STATIONARY_FEATURIZER_FIT_NAME):

            # making sure x is a tsds
            if not isinstance(x, TimeSeriesDataSet):
                raise ForecastingDataException._with_error(
                    AzureMLError.create(
                        TimeseriesInputIsNotTimeseriesDs,
                        target="X",
                        reference_code=ReferenceCodes._TS_INPUT_IS_NOT_TSDF_TM_IDX_STATIONARY_FEATURIZER)
                )

            # If missing values exists, we disable processing non-stationary data to stationary data.
            if self._imputation_target_marker in x.data.columns and x.data[self._imputation_target_marker].sum() > 0:
                logger.info("Stationary Featurizer is disabled since data has missing values.")
                self._do_stationarization = False

            if len(self.non_stationary_time_series_ids) == 0:
                self._do_stationarization = False

            if self._do_stationarization:
                logger.info("Stationary featurizer is triggered.")
                # Storing data of minimum and maximum timestamps to
                # re-differencing/conversion of differences to levels for each grain.
                self.freq = x.infer_freq()
                for grain, df_grain in x.groupby_time_series_id():
                    if grain in self.non_stationary_time_series_ids:
                        if self.start_values is None or grain not in self.start_values:
                            df_grain.reset_index(inplace=True)
                            df_grain.sort_values(by=[x.time_column_name], inplace=True)
                            self.start_values[grain] = []
                            self.last_values[grain] = df_grain.iloc[-1]
                            if self._lagging_length != 0:
                                self.start_values[grain].append(df_grain.iloc[0])
                                for horizon in range(1, self.max_horizon + 1):
                                    self.start_values[grain].append(df_grain.iloc[horizon + self._lagging_length - 2])
                            else:
                                self.start_values[grain].append(df_grain.iloc[0])

                self._is_fit = True
            else:
                logger.info("Stationary featurizer is not triggered.")

            return self

    @function_debug_log_wrapped(logging.INFO)
    def transform(self,
                  x: TimeSeriesDataSet) -> TimeSeriesDataSet:
        """
        Transform the data frame.

        :param x: Input data.
        :type x: azureml.automl.runtime._time_series_data_set.TimeSeriesDataSet object.
        :return: The TimeSeriesDataSet object, after stationary_featurizer transform.
        """
        with log_utils.log_activity(logger,
                                    activity_name=TelemetryConstants.RUN_STATIONARY_FEATURIZER_TRANSFORM_NAME):
            # checking that stationary_featurizer already fitted before transform.
            if self._do_stationarization and not self._is_fit:
                raise ClientException._with_error(
                    AzureMLError.create(
                        TimeseriesFeaturizerFitNotCalled, target='fit',
                        reference_code=ReferenceCodes._TS_STATIONARY_FEATURIZER_NO_FIT_TRANS))

            if self.columns_to_be_processed is None or not self._do_stationarization:
                return x

            for grain, df_grain in x.groupby_time_series_id():
                if grain in self.non_stationary_time_series_ids:
                    for col in self.columns_to_be_processed:
                        # It is checked that if df_grain is the continuation of the time series or not.
                        # If df_grain_start_index > last_date, the df_grain is
                        # the continuation of time series and ref value will be last_date.
                        # else df_grain_start_index is the start of the time series,
                        # differencing is based on 0 and ref value is 0.
                        last_date = self.get_last_dates(grain, x.time_column_name)
                        grain_index = df_grain.index
                        df_grain.reset_index(inplace=True)
                        df_grain_start_index = df_grain[x.time_column_name].min()
                        if (self.start_values is not None
                                and (grain in self.start_values)
                                and (df_grain_start_index > last_date)):
                            reference_value = self.last_values[grain][col]
                            x.data.loc[grain_index, col] = np.diff(df_grain[col],
                                                                   n=TimeSeriesInternal.DIFFERENCING_ORDER,
                                                                   prepend=reference_value)
                        elif df_grain_start_index == self.get_start_dates(grain, x.time_column_name):
                            diffed_col = np.diff(df_grain[col], n=TimeSeriesInternal.DIFFERENCING_ORDER)
                            # Padding values after processing diff with 0 to keep same sample number in data.
                            x.data.loc[grain_index, col] = np.insert(diffed_col, 0, 0)
                        else:
                            # This condition is for unsupported time series data.
                            raise DataException._with_error(AzureMLError.create(
                                TimeSeriesUnsupportedTimeSequenceForStationaryFeaturizer, target="X",
                                reference_code=ReferenceCodes._TS_STATIONARY_FEATURIZER_UNSUPPORTED_TIME_SEQUENCE)
                            )

            return x

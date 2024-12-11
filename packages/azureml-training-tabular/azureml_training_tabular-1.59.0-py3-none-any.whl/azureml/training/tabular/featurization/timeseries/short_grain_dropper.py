# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Drop grains from dataset."""
from typing import Any, List, Optional
import pandas as pd

from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared.exceptions import DataException

from ..._constants import TimeSeriesInternal
from ..._diagnostics.error_definitions import (
    TimeseriesInsufficientData,
)
from ..._diagnostics.reference_codes import ReferenceCodes
from ..._types import GrainType
from ...timeseries._time_series_data_set import TimeSeriesDataSet
from .grain_dropper import GrainDropper


class ShortGrainDropper(GrainDropper):
    """Drop short series, or series not found in training set."""

    def __init__(self,
                 target_rolling_window_size: int = 0,
                 target_lags: Optional[List[int]] = None,
                 n_cross_validations: Optional[int] = None,
                 cv_step_size: Optional[int] = None,
                 max_horizon: int = TimeSeriesInternal.MAX_HORIZON_DEFAULT,
                 **kwargs: Any) -> None:
        """
        Constructor.

        :param target_rolling_window_size: The size of a target rolling window.
        :param target_lags: The size of a lag of a lag operator.
        :param n_cross_validations: The number of cross validations.
        :param cv_step_size: The number of steps to move validation set.
        :param max_horizon: The maximal horizon.
        :raises: ConfigException
        """
        super().__init__(target_rolling_window_size, target_lags, n_cross_validations, cv_step_size, max_horizon)
        self._has_short_grains = False
        self._short_grains_in_train = 0

    def _fit(self, X: TimeSeriesDataSet, y: Any = None) -> 'ShortGrainDropper':
        """
        Define the grains to be stored.

        If all the grains should be dropped, raises DataExceptions.
        :param X: The time series data frame to fit on.
        :param y: Ignored
        :raises: DataException
        """
        self._short_grains_in_train_names = []
        self._has_short_grains = False
        self._short_grains_in_train = 0
        self._grains_to_keep = set()
        for grain, df in X.groupby_time_series_id():
            # To mark grain as short we need to use TimeSeriesInternal.DUMMY_ORDER_COLUMN value or
            # if it is not present, the shape of a data frame. The rows where TimeSeriesInternal.DUMMY_ORDER_COLUMN
            # is NaN were not present in the original data set and finally will be removed, leading to error
            # during rolling origin cross validation.
            # UPDATE: Use the missing/row indicator to exclude imputed/filled rows
            keep_grain = self.is_df_long(df, X)

            # Mark the grain to keep or drop, depending on if it meets the length threshold
            if keep_grain:
                self._grains_to_keep.add(grain)
            else:
                self._short_grains_in_train_names.append(grain)
                self._has_short_grains = True

        self._short_grains_in_train = len(self._short_grains_in_train_names)

        if not self._grains_to_keep and self._grains_to_drop:
            raise DataException._with_error(AzureMLError.create(
                TimeseriesInsufficientData, target="X", grains=str(self._short_grains_in_train_names), num_cv=self._cv,
                max_horizon=self._max_horizon, lags=str(self._lags), window_size=self._window_size,
                cv_step_size=self._cv_step_size,
                reference_code=ReferenceCodes._TS_SHORT_GRAINS_ALL_SHORT_REFIT)
            )
        return self

    def _validate_transformed_data(self, df: pd.DataFrame, drop_grains: List[GrainType]) -> None:
        if df.shape[0] == 0:
            raise DataException._with_error(AzureMLError.create(
                TimeseriesInsufficientData, target="X", grains=str(list(drop_grains)), num_cv=self._cv,
                max_horizon=self._max_horizon, lags=str(self._lags), window_size=self._window_size,
                cv_step_size=self._cv_step_size,
                reference_code=ReferenceCodes._TS_SHORT_GRAINS_ALL_SHORT_TRANS)
            )

    @property
    def has_short_grains_in_train(self) -> bool:
        """Return true if there is no short grains in train set."""
        return self.has_grain_dropped

    @property
    def short_grains_in_train(self) -> int:
        """Return the number of short grains in train."""
        return self.number_of_grain_dropped

    # The properties under below this are kept for backward-compatibility.
    @property
    def _short_grains(self) -> List[str]:
        return self._grains_to_drop

    @_short_grains.setter
    def _short_grains(self, short_grains: List[str]) -> None:
        self._grains_to_drop = short_grains

    @property
    def _short_grains_in_train_names(self) -> List[str]:
        return self._grains_to_drop

    @_short_grains_in_train_names.setter
    def _short_grains_in_train_names(self, short_grains: List[str]) -> None:
        self._grains_to_keep = set(short_grains)

    @property
    def short_grains_in_train_names(self) -> List[str]:
        return self._grains_to_drop

# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Drop unique target value grains from dataset."""

from typing import Any, List, Optional, Set, Tuple
import logging
import numpy as np
import pandas as pd

from azureml._common._error_definition import AzureMLError

from azureml.automl.core.shared.forecasting_exception import ForecastingDataException

from ..._diagnostics.debug_logging import function_debug_log_wrapped
from ..._diagnostics.error_definitions import UniqueDataInValidation
from ..._diagnostics.reference_codes import ReferenceCodes
from ..._types import GrainType
from ...timeseries._time_series_data_set import TimeSeriesDataSet
from ..._constants import TimeSeriesInternal
from ...featurization.utilities import _get_num_unique
from .grain_dropper import GrainDropper
from .unique_target_grain_dropper_base import UniqueTargetGrainDropperBase


class UniqueTargetGrainDropper(GrainDropper, UniqueTargetGrainDropperBase):
    """Uniqe target grain dropper."""

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
        UniqueTargetGrainDropperBase.__init__(self)
        GrainDropper.__init__(
            self, target_rolling_window_size, target_lags, n_cross_validations, cv_step_size, max_horizon,
            drop_single_grain=False, drop_unknown=False)
        self._last_X = None  # type: Optional[pd.DataFrame]
        self._last_y = None  # type: Optional[np.ndarray]
        self._last_valid_X = None  # type: Optional[pd.DataFrame]
        self._last_valid_y = None  # type: Optional[np.ndarray]

    def _set_last_X_y(self, X: TimeSeriesDataSet, validation: bool = False) -> None:
        """
        Set last X and y for both training and validation data based on the validation parameter.

        :param X: TimeSeriesDataSet.
        :param validation: True if the data is validation data.
        """
        target_col = X.target_column_name

        dfs = []
        for grain, df in X.groupby_time_series_id():
            if not validation:  # only do keep grains / drop grains in training data
                # short grain and all missing value won't be handled by unique target grain dropper.
                n_unique = _get_num_unique(df[target_col], ignore_na=True)
                if n_unique != 1 or not self.is_df_long(df, X):
                    self._grains_to_keep.add(grain)
                else:
                    self._grains_to_drop.append(grain)
                    dfs.append(df.tail(1))
            else:
                dfs.append(df.tail(1))

        if dfs:
            if validation:
                self._last_valid_X = pd.concat(dfs, sort=False)
                self._last_valid_y = self._last_valid_X.pop(target_col).values
            else:
                self._last_X = pd.concat(dfs, sort=False)
                self._last_y = self._last_X.pop(target_col).values

    @function_debug_log_wrapped(logging.INFO)
    def _fit(self, X: TimeSeriesDataSet, y: Any = None) -> 'UniqueTargetGrainDropper':
        self._set_last_X_y(X)
        return self

    def _validate_transformed_data(self, df: TimeSeriesDataSet, dropped_grains: List[GrainType]) -> None:
        """Throw the error if all series appeared to be unique."""
        # We have to raise the exception here if all grains have to be dropped.
        # This may happen if target contain non unique values and passed the pre processing step,
        # but when the CV cross fold
        if not self.grains_to_keep:
            raise ForecastingDataException._with_error(
                AzureMLError.create(
                    UniqueDataInValidation, target='unique_target_gain_dropper_validation',
                    reference_code=ReferenceCodes._TS_UNIQUE_VALUE_CROSS_VALIDATION))

    def set_last_validation_data(self, validation_X: TimeSeriesDataSet) -> None:
        """Set last validation data."""
        self._set_last_X_y(validation_X, True)

    @property
    def last_validation_X_y(self) -> Tuple[Optional[pd.DataFrame], Optional[np.ndarray]]:
        """The last validation X"""
        return self._last_valid_X, self._last_valid_y

    @property
    def last_X_y(self) -> Tuple[Optional[pd.DataFrame], Optional[np.ndarray]]:
        """The last X and y observed during fit."""
        return self._last_X, self._last_y

    @property
    def unique_target_grains(self) -> Set[str]:
        """The unique target grains."""
        return set(self._grains_to_drop)

    @property
    def has_unique_target_grains(self) -> bool:
        """The flag that shows whether the transformer contains unique target grain or not."""
        total_grains = len(self._grains_to_keep) + len(self.unique_target_grains)
        if total_grains > 1:
            return len(self.unique_target_grains) > 0
        elif self.drop_single_grain:
            return len(self.unique_target_grains) > 0
        else:
            return False

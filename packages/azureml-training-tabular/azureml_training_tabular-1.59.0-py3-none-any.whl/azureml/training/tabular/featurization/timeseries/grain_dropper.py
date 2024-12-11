# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Drop grains from dataset."""
from typing import Any, List, Set, Optional
from abc import abstractmethod
import logging
import pandas as pd

from azureml._common._error_definition import AzureMLError

from azureml.automl.core.shared.exceptions import ClientException
from azureml.automl.core.shared.forecasting_exception import ForecastingDataException

from ..._constants import TimeSeriesInternal
from ..._diagnostics.debug_logging import function_debug_log_wrapped
from ..._diagnostics.error_definitions import (
    FitNotCalled,
    TimeseriesInputIsNotTimeseriesDs
)
from ..._diagnostics.reference_codes import ReferenceCodes
from ..._types import GrainType
from ...timeseries._time_series_data_set import TimeSeriesDataSet
from .._azureml_transformer import AzureMLTransformer
from ..utilities import get_min_points
from ._grain_based_stateful_transformer import _GrainBasedStatefulTransformer


class GrainDropper(AzureMLTransformer, _GrainBasedStatefulTransformer):
    def __init__(
            self,
            target_rolling_window_size: int = 0,
            target_lags: Optional[List[int]] = None,
            n_cross_validations: Optional[int] = None,
            cv_step_size: Optional[int] = None,
            max_horizon: int = TimeSeriesInternal.MAX_HORIZON_DEFAULT,
            drop_single_grain: bool = True,
            drop_unknown: bool = True,
            **kwargs: Any
    ) -> None:
        super().__init__()
        self._grains_to_keep = set()  # type: Set[str]
        self._grains_to_drop = []  # type: List[str]
        self._is_fit = False
        self._window_size = target_rolling_window_size  # type: int
        self._lags = target_lags if target_lags else [0]  # type: List[int]
        self._cv = n_cross_validations  # type: Optional[int]
        self._cv_step_size = cv_step_size  # type: Optional[int]
        self._max_horizon = max_horizon  # type: int
        self._min_points = get_min_points(
            self._window_size, self._lags, self._max_horizon, self._cv, self._cv_step_size)
        self.drop_single_grain = drop_single_grain
        self.drop_unknown = drop_unknown

        # feature flag for inclusion of order column in input dataframe
        # This flag is used to preserve compatibility between SDK versions
        self._no_original_order_column = True

    def _no_original_order_column_safe(self):
        return hasattr(self, '_no_original_order_column') and self._no_original_order_column

    @property
    def has_grain_dropped(self) -> bool:
        if not self._is_fit:
            raise ClientException._with_error(
                AzureMLError.create(
                    FitNotCalled, target='fit',
                    reference_code=ReferenceCodes._TS_SHORT_GRAINS_NO_FIT_HAS_GR))
        return len(self._grains_to_drop) > 0

    @property
    def number_of_grain_dropped(self) -> int:
        return len(self._grains_to_drop)

    @property
    def grains_to_keep(self) -> Set[str]:
        """Return the list of grains to keep."""
        if not self._is_fit:
            raise ClientException._with_error(
                AzureMLError.create(
                    FitNotCalled, target='fit',
                    reference_code=ReferenceCodes._TS_SHORT_GRAINS_NO_FIT_GR))
        return self._grains_to_keep

    @abstractmethod
    def _fit(self, X: TimeSeriesDataSet, y: Any = None) -> 'GrainDropper':
        raise NotImplementedError

    @abstractmethod
    def _validate_transformed_data(self, df: pd.DataFrame, dropped_grains: List[GrainType]) -> None:
        raise NotImplementedError

    @function_debug_log_wrapped(logging.INFO)
    def fit(self, X: TimeSeriesDataSet, y: Any = None) -> 'GrainDropper':
        self._validate_input_data(X, y)
        fitted_pipeline = self._fit(X, y)
        self._is_fit = True
        return fitted_pipeline

    @function_debug_log_wrapped(logging.INFO)
    def transform(self, X: TimeSeriesDataSet, y: Any = None) -> TimeSeriesDataSet:
        """
        Drop grains, which were not present in training set, or were removed.

        If all the grains should be dropped, raises DataExceptions.
        :param X: The time series data frame to check for grains to drop.
        :param y: Ignored
        :raises: ClientException, DataException
        """
        if not self._is_fit:
            raise ClientException._with_error(
                AzureMLError.create(
                    FitNotCalled, target='fit',
                    reference_code=ReferenceCodes._TS_SHORT_GRAINS_NO_FIT_TRANS))
        self._raise_wrong_type_maybe(X, ReferenceCodes._TS_INPUT_IS_NOT_TSDF_SHORT_GRAIN_TRANS)
        drop_grains = set()

        def do_keep_grain(df):
            """Do the filtering and add all values to set."""
            keep = df.name in self._grains_to_keep
            is_known = keep or df.name in self._grains_to_drop
            if not keep and len(self._grains_to_drop) + len(self._grains_to_keep) == 1 and not self.drop_single_grain:
                keep = True
            if not keep and not is_known:
                keep = not self.drop_unknown
            if not keep:
                drop_grains.add(df.name)
            return keep

        result = X.groupby_time_series_id().filter(lambda df: do_keep_grain(df))
        self._validate_transformed_data(result, list(drop_grains))
        return X.from_data_frame_and_metadata(result)

    def _raise_wrong_type_maybe(self, X: Any, reference_code: str) -> None:
        """Raise exception if X is not TimeSeriesDataSet."""
        if not isinstance(X, TimeSeriesDataSet):
            raise ForecastingDataException._with_error(
                AzureMLError.create(TimeseriesInputIsNotTimeseriesDs, target='X',
                                    reference_code=reference_code)
            )

    def _validate_input_data(self, X: TimeSeriesDataSet, y: Any = None) -> None:
        self._raise_wrong_type_maybe(X, ReferenceCodes._TS_INPUT_IS_NOT_TSDF_SHORT_GRAIN)

    def is_df_long(self, grain_df: pd.DataFrame, X_input: pd.DataFrame) -> bool:
        keep_grain = True
        row_imputed_name = TimeSeriesInternal.ROW_IMPUTED_COLUMN_NAME
        if self._no_original_order_column_safe() and (row_imputed_name in X_input.data.columns):
            keep_grain = grain_df[row_imputed_name].notnull().sum() >= self._min_points
        elif TimeSeriesInternal.DUMMY_ORDER_COLUMN in X_input.data.columns:
            keep_grain = grain_df[TimeSeriesInternal.DUMMY_ORDER_COLUMN].notnull().sum() >= self._min_points
        else:
            keep_grain = grain_df.shape[0] >= self._min_points
        return keep_grain

    @property
    def target_rolling_window_size(self) -> int:
        """Return target window size."""
        return self._window_size

    @property
    def target_lags(self) -> List[int]:
        """Return target lags."""
        return self._lags

    @property
    def n_cross_validations(self) -> Optional[int]:
        """Return number of cv steps."""
        return self._cv

    @property
    def cv_step_size(self) -> Optional[int]:
        """Return the cv step size."""
        return self._cv_step_size

    @property
    def max_horizon(self) -> int:
        """Return forecast horizon."""
        return self._max_horizon

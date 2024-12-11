# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Base class for unique target value grains dropper."""
from typing import Any, List, Optional, Tuple, Generator, Set, Union
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import uuid

from ...timeseries._time_series_data_set import TimeSeriesDataSet


class UniqueTargetGrainDropperBase(ABC):
    def __init__(self):
        self.drop_single_grain = False

    @property
    @abstractmethod
    def has_unique_target_grains(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def unique_target_grains(self) -> Set[str]:
        raise NotImplementedError

    @property
    @abstractmethod
    def grains_to_keep(self) -> Set[str]:
        raise NotImplementedError

    @abstractmethod
    def fit(self, X: TimeSeriesDataSet, y: Any = None) -> 'UniqueTargetGrainDropperBase':
        raise NotImplementedError

    def set_last_validation_data(self, validation_X: TimeSeriesDataSet) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def last_X_y(self) -> Tuple[Optional[pd.DataFrame], Optional[np.ndarray]]:
        raise NotImplementedError

    @property
    @abstractmethod
    def last_validation_X_y(self) -> Tuple[Optional[pd.DataFrame], Optional[np.ndarray]]:
        raise NotImplementedError

    def unique_grain_data_generator(
            self,
            df: pd.DataFrame,
            grain_column_names: List[str]
    ) -> Generator[Tuple[Any, pd.DataFrame], None, None]:
        """Generate the unique target grains which will drop after featurization."""
        return filter(lambda x: x[0] in self.unique_target_grains, df.groupby(grain_column_names))

    def non_unique_grain_data_generator(
            self,
            df: pd.DataFrame,
            grain_column_names: List[str]
    ) -> Generator[Tuple[Any, pd.DataFrame], None, None]:
        """Generate the unique target grains which will not drop after featurization."""
        return filter(lambda x: x[0] not in self.unique_target_grains, df.groupby(grain_column_names))

    def get_unique_grain(self, df: pd.DataFrame, grain_column_names: List[str]) -> pd.DataFrame:
        """Get the unique target grain."""
        dfs = []
        for _, df_one in self.unique_grain_data_generator(df, grain_column_names):
            dfs.append(df_one)
        return pd.concat(dfs, sort=False) if len(dfs) > 0 else pd.DataFrame()

    def get_non_unique_grain(self, df: pd.DataFrame, grain_column_names: List[str]) -> pd.DataFrame:
        """Get the non unique target grain."""
        dfs = []
        for _, df_one in self.non_unique_grain_data_generator(df, grain_column_names):
            dfs.append(df_one)
        return pd.concat(dfs, sort=False) if len(dfs) > 0 else pd.DataFrame()

    def get_target_X_y(
            self,
            X: pd.DataFrame,
            y: Union[pd.DataFrame, np.ndarray],
            grain_column_names: List[str],
            is_unique_target: bool
    ) -> Tuple[pd.DataFrame, np.array]:
        """Get the unique target grain with Xy input."""
        X_copy = X.copy()
        target_col = str(uuid.uuid4())
        X_copy[target_col] = y

        if is_unique_target:
            target_Xy = self.get_unique_grain(X_copy, grain_column_names)
        else:
            target_Xy = self.get_non_unique_grain(X_copy, grain_column_names)
        if not target_Xy.empty:
            y_unique = target_Xy.pop(target_col).values
        else:
            y_unique = None
        return target_Xy, y_unique

    def has_non_unique_data(self, df: pd.DataFrame, grain_column_names: List[str]) -> bool:
        """If any non unique target grain in the data."""
        return next(self.non_unique_grain_data_generator(df, grain_column_names), None) is not None

# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from dataclasses import dataclass
from typing import Sequence, Mapping, Any, Optional, Union
import pandas as pd
import numpy as np

from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared.constants import TimeSeriesInternal, MLTableDataLabel
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.runtime.featurizer.transformer.timeseries._distributed.distributed_timeseries_util import \
    convert_grain_dict_to_str
from azureml.dataprep import DataProfile


@dataclass
class TimeSeriesDataProfile:
    val_row_count: int
    train_row_count: int
    train_target_max: float
    train_target_min: float
    train_mean: Sequence[Optional[float]]
    train_std: Sequence[Optional[float]]
    train_end_date: pd.Timestamp
    val_start_date: pd.Timestamp


@dataclass
class AggregatedTimeSeriesDataProfile:
    columns: Sequence[str]
    column_order_in_timeseries_profile: Sequence[str]
    profile_mapping: Mapping[str, Optional[TimeSeriesDataProfile]]

    def get_row_count(self, grain: Mapping[str, Any], dataset_type: MLTableDataLabel) -> int:
        """
        Get the count of rows in a grain in a dataset.

        :param grain: The grain for which we need the row count.
        :param dataset_type: The dataset type for which we need the row count.

        :return: The row count for the grain the the dataset.
        """
        Contract.assert_true(
            dataset_type is MLTableDataLabel.TrainData or MLTableDataLabel.ValidData,
            "Timeseries data profile contains row count for training and validation datasets only",
            reference_code=ReferenceCodes._TS_DATASET_TYPE_ABSENT_IN_DATA_PROFILE,
            target="timeseries data profile"
        )
        grain_profile = self.get_profile_for_grain(grain)
        if dataset_type is MLTableDataLabel.TrainData:
            return grain_profile.train_row_count
        return grain_profile.val_row_count

    def get_column_names(self) -> Sequence[str]:
        """Get the column names (in order) in the dataset."""
        return self.columns

    def get_train_end_date(self, grain: Mapping[str, Any]) -> pd.Timestamp:
        """
        Get the end date for a grain in the training dataset.

        :param grain: The grain for which we need the end date in the training dataset.

        :return: The end date for the grain in the training dataset.
        """
        grain_profile = self.get_profile_for_grain(grain)
        return grain_profile.train_end_date

    def get_val_start_date(self, grain: Mapping[str, Any]) -> pd.Timestamp:
        """
        Get the start date for a grain in the validation dataset.

        :param grain: The grain for which we need the start date in the validation dataset.

        :return: The start date for the grain in the validation dataset.
        """
        grain_profile = self.get_profile_for_grain(grain)
        return grain_profile.val_start_date

    def get_train_mean(
        self,
        grain: Mapping[str, Any],
        columns: Union[str, Sequence[str]]
    ) -> Union[str, Sequence[str]]:
        """
        Get the mean for column/columns in a grain in the training dataset.

        :param grain: The grain for which we need the means.
        :param columns: The column/columns for which we need the means.

        :return: A float (if a column is provided) or a list of float (if a list of columns)
                are provided.
        """
        grain_profile = self.get_profile_for_grain(grain)
        if isinstance(columns, str):
            column = columns
            return grain_profile.train_mean[self._get_column_index(column)]
        return [grain_profile.train_mean[self._get_column_index(column)] for column in columns]

    def get_train_std(
        self,
        grain: Mapping[str, Any],
        columns: Union[str, Sequence[str]]
    ) -> Union[str, Sequence[str]]:
        """
        Get the std for column/columns in a grain in the training dataset.

        :param grain: The grain for which we need the means.
        :param columns: The column/columns for which we need the std.

        :return: A float (if a column is provided) or a list of float (if a list of columns)
                are provided.
        """
        grain_profile = self.get_profile_for_grain(grain)
        if isinstance(columns, str):
            column = columns
            return grain_profile.train_std[self._get_column_index(column)]
        return [grain_profile.train_std[self._get_column_index(column)] for column in columns]

    def get_train_y_min(self, grain: Mapping[str, Any]) -> float:
        """
        Get the y min for a grain in the training dataset.

        :param grain: The grain for which the y min is needed.

        :return: The y min for the grain in the training dataset.
        """
        grain_data_profile = self.get_profile_for_grain(grain)
        return grain_data_profile.train_target_min

    def get_train_y_max(self, grain: Mapping[str, Any]) -> float:
        """
        Get the y max for a grain in the training dataset.

        :param grain: The grain for which the y max is needed.

        :return: The y max for the grain in the training dataset.
        """
        grain_data_profile = self.get_profile_for_grain(grain)
        return grain_data_profile.train_target_max

    def get_profile_for_grain(self, grain: Mapping[str, Any]) -> TimeSeriesDataProfile:
        """
        Get the data profile for a grain. If the grain is not found, an error is thrown.

        :param grain: The grain for which the data profile is needed.

        :return: The data profile for the grain.
        """
        grain_str = convert_grain_dict_to_str(grain)
        Contract.assert_true(
            grain_str in self.profile_mapping,
            "Grain is not in the timeseries data profile.",
            reference_code=ReferenceCodes._TS_GRAIN_ABSENT_IN_TS_DATA_PROFILE,
            target="timeseries data profile"
        )
        return self.profile_mapping[grain_str]

    def _get_column_index(self, column: str) -> int:
        """
        Get the index of the column in the individual grain profile lists.

        :param column: column for which the index is needed.

        :return: The index of the colum in the individual grain profile lists.
        """
        Contract.assert_true(
            column in self.column_order_in_timeseries_profile,
            "Column is not in the data profile.",
            reference_code=ReferenceCodes._TS_DIST_DATASET_CONFIG_COL_NOT_IN_PROFILE,
            target="timeseries data profile"
        )
        return self.column_order_in_timeseries_profile.index(column)


def ts_dataprofile_from_dprep_dataprofile(
    train_data_profile: DataProfile,
    val_data_profile: DataProfile,
    time_column_name: str,
) -> TimeSeriesDataProfile:
    """
    Get the time series data profile from the data prep profiles.

    :param train_data_profile: dprep profile for the grain in the training dataset.
    :param val_data_profile: dprep profile for the grain in the validatio ndataset.
    :param time_column_name: the time column name.

    :return: The timeseries data profile for the grain.
    """
    columns = sorted(list(train_data_profile.columns))
    # Calculate row counts
    val_row_count = val_data_profile.shape[0]
    train_row_count = train_data_profile.shape[0]
    # Calculate target min/max
    train_target_max = train_data_profile.columns[TimeSeriesInternal.DUMMY_TARGET_COLUMN].max
    train_target_min = train_data_profile.columns[TimeSeriesInternal.DUMMY_TARGET_COLUMN].min
    # Calculate mean/std
    train_mean = [train_data_profile.columns[col].mean for col in columns]
    train_std = [_calculate_std(train_data_profile, col) for col in columns]
    # Calculate start/end dates
    train_end_date = train_data_profile.columns[time_column_name].max
    val_start_date = val_data_profile.columns[time_column_name].min
    return TimeSeriesDataProfile(
        val_row_count=val_row_count,
        train_row_count=train_row_count,
        train_target_max=train_target_max,
        train_target_min=train_target_min,
        train_mean=train_mean,
        train_std=train_std,
        train_end_date=train_end_date,
        val_start_date=val_start_date
    )


def _calculate_std(profile: DataProfile, col: str) -> float:
    """
    Calculate the standard deviation of a column from the dprep data profile.

    :param profile: The dprep data profile.
    :param col: name of the column for which std has to be calculated.

    :return: The standard deviation if the column is numeric, else None
    """
    std = profile.columns[col].std
    if std is None:
        return None
    size = profile.shape[0]
    safe_scale = np.sqrt((size - 1) * (std ** 2) / size)
    if safe_scale < 10 * np.finfo(safe_scale.dtype).eps:
        safe_scale = 1
    return float(safe_scale)

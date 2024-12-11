# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, Dict, List
import pandas as pd

from ..featurization.timeseries.timeseries_transformer import TimeSeriesTransformer


class _ForecastScenarioData:
    """Internal class for filtering forecast data based on different scenarios."""
    _DATA_SCENARIO_UNIQUE = 'unique_target'
    _DATA_SCENARIO_AUTOML = 'automl'
    _DATA_SCENARIO = [_DATA_SCENARIO_AUTOML, _DATA_SCENARIO_UNIQUE]

    def __init__(self, data_scenario: Dict[str, pd.DataFrame], dict_rename_back: Dict[str, Any]):
        self._data_scenario = data_scenario
        self._dict_rename_back = dict_rename_back

    @property
    def data_scenario(self) -> Dict[str, pd.DataFrame]:
        return self._data_scenario

    @property
    def dict_rename_back(self) -> Dict[str, Any]:
        return self._dict_rename_back

    def get_scenario_data(self, scenario: str) -> pd.DataFrame:
        return self.data_scenario.get(scenario, pd.DataFrame())

    @staticmethod
    def from_prepared_input_data(
            Xy_pred_in: pd.DataFrame,
            ts_transformer: TimeSeriesTransformer,
            grain_column_list: List[str],
            dict_rename_back: Dict[str, Any]
    ) -> "_ForecastScenarioData":
        data_scenario = {
            scenario: _ForecastScenarioData._data_filter(scenario, Xy_pred_in, ts_transformer, grain_column_list)
            for scenario in _ForecastScenarioData._DATA_SCENARIO
        }
        return _ForecastScenarioData(data_scenario, dict_rename_back)

    @staticmethod
    def _data_filter(
            scenario: str,
            df: pd.DataFrame,
            ts_transformer: TimeSeriesTransformer,
            grain_column_list: List[str]
    ) -> pd.DataFrame:
        output_df = pd.DataFrame()
        if scenario == _ForecastScenarioData._DATA_SCENARIO_UNIQUE:
            if ts_transformer.has_unique_target_grains_dropper:
                output_df = ts_transformer.unique_target_grain_dropper.get_unique_grain(df, grain_column_list)
        elif scenario == _ForecastScenarioData._DATA_SCENARIO_AUTOML:
            if ts_transformer.has_unique_target_grains_dropper:
                output_df = ts_transformer.unique_target_grain_dropper.get_non_unique_grain(
                    df, grain_column_list)
            else:
                # backward compatibility to return all data
                output_df = df
        else:
            # default scenario, return all data.
            output_df = df
        return output_df

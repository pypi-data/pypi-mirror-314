# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, Dict, List, Mapping

import copy

from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    NonBooleanValueInIndicatorColDictionary)
from azureml.automl.core.shared.exceptions import ClientException
from azureml.automl.core.shared.reference_codes import ReferenceCodes


def convert_grain_dict_to_str(grain_dict: Mapping[str, Any]) -> str:
    """
    Convert dictionary of grains to string.

    Dictionary of the form {key1: value1, key2: value2} will be converted to string
    key1_value1_key2_value2. Additionally string will always be returns in sorted order.
    """
    return "_".join("{}_{}".format(k, v) for k, v in sorted(grain_dict.items(), key=lambda x: str(x[0])))


def collate_indicator_column_data_dictionaries(
        indicator_columns_data_list: List[Dict[str, bool]]) -> Dict[str, bool]:
    """
    Go over all columns in dictionaries and set if the column contains only zeroes and ones.

    If at least one grain contains different value in this column, do not mark it as indicator.
    :param indicator_columns_data_list: The dictionaries with columns marked as indicator
                                        or non indicator.
    :raises: Client exception if the dictionary contains non boolean value
    :return: The dictionary with columns marked as indicator or non indicator.
    """
    if len(indicator_columns_data_list) == 0:
        return {}

    # Validate that we have only boolean values in the dictionary.
    for dt in indicator_columns_data_list:
        for v in dt.values():
            if not isinstance(v, bool):
                raise ClientException._with_error(
                    AzureMLError.create(
                        NonBooleanValueInIndicatorColDictionary, target='indicator_column',
                        reference_code=ReferenceCodes._FORECASTING_DISTRIBUTED_WRONG_INDICATOR_TYPE))

    dt_result = copy.deepcopy(indicator_columns_data_list[0])
    if len(indicator_columns_data_list) == 1:
        return dt_result

    for dt in indicator_columns_data_list[1:]:
        for k, v in dt.items():
            if k not in dt_result or dt_result[k]:
                dt_result[k] = v
    return dt_result

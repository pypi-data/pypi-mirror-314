# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Drop unique target value grains for distributed tasks."""
from typing import Mapping, Optional, Set, Tuple, Generator
import numpy as np
import pandas as pd
import itertools

from azureml.automl.core.shared import constants

from ..unique_target_grain_dropper import UniqueTargetGrainDropper
from ..unique_target_grain_dropper_base import UniqueTargetGrainDropperBase
from .aggregated_grain_dropper import AggregatedGrainDropper


class AggregatedUniqueTargetGrainDropper(AggregatedGrainDropper, UniqueTargetGrainDropperBase):
    """Aggregated unique target grain dropper for distributed forecasting tasks."""
    def __init__(self, mapping: Mapping[str, UniqueTargetGrainDropper]) -> None:
        AggregatedGrainDropper.__init__(self, mapping)
        UniqueTargetGrainDropperBase.__init__(self)
        self._allow_empty_output = True
        for dropper in mapping.values():
            dropper.drop_single_grain = True

    def _unique_target_grains_dropper_generator(self) -> Generator[UniqueTargetGrainDropper, None, None]:
        return filter(lambda x: x.has_unique_target_grains, self.mapping.values())

    @property
    def has_unique_target_grains(self) -> bool:
        return next(self._unique_target_grains_dropper_generator(), None) is not None

    @property
    def unique_target_grains(self) -> Set[str]:
        return set(itertools.chain.from_iterable(
            map(lambda x: x.unique_target_grains, self._unique_target_grains_dropper_generator())))

    def _get_last_X_y(self, validation: bool = False) -> Tuple[Optional[pd.DataFrame], Optional[np.ndarray]]:
        """
        Returns last X and y in the fit data for training and validation based on the validation flag.

        :param validation: True if required last X and y in the validation data, False otherwise.
        """
        dfs = []
        last_X = None
        last_y = None
        for dropper in self._unique_target_grains_dropper_generator():
            if validation:
                last_X, last_y = dropper.last_validation_X_y
            else:
                last_X, last_y = dropper.last_X_y
            if last_X is not None:
                last_X[constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN] = last_y
                dfs.append(last_X)

        if dfs:
            last_X = pd.concat(dfs, sort=False)
            last_y = last_X.pop(constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN).values
        return last_X, last_y

    @property
    def last_X_y(self) -> Tuple[Optional[pd.DataFrame], Optional[np.ndarray]]:
        """Last X and y in the fit data."""
        return self._get_last_X_y()

    @property
    def last_validation_X_y(self) -> Tuple[Optional[pd.DataFrame], Optional[np.ndarray]]:
        """Last X and y in the validation data."""
        return self._get_last_X_y(validation=True)

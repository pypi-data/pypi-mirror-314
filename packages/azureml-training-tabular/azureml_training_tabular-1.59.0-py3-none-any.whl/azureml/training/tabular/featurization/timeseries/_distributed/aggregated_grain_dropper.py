# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Aggregated grain dropper for distributed tasks."""
from typing import Mapping, Set
import itertools

from azureml.training.tabular.featurization._azureml_transformer import AzureMLTransformer
from ..grain_dropper import GrainDropper
from .aggregate_transformer import AutoMLAggregateTransformer


class AggregatedGrainDropper(AutoMLAggregateTransformer):
    """Aggregated grain dropper for distributed tasks."""
    def __init__(self, mapping: Mapping[str, GrainDropper]) -> None:
        AutoMLAggregateTransformer.__init__(self, mapping)
        # Short grain droppers are not fit when a grain has unique target.
        # Hence, we use x._is_fit to check it is fit before trying to get
        # grains_to_keep property.
        # We check if x has grains_to_keep property because in some tests, we do not
        # pass a GrainDropper as mapped values.
        grains_to_keep_transforms = filter(
            self._is_transform_fitted_grain_dropper, self._mapping.values()
        )
        grains_to_keep = map(lambda x: x.grains_to_keep, grains_to_keep_transforms)
        self._grains_to_keep = set(itertools.chain.from_iterable(grains_to_keep))

    @property
    def grains_to_keep(self) -> Set[str]:
        return self._grains_to_keep

    def _is_transform_fitted_grain_dropper(self, transform: AzureMLTransformer):
        """Check if a transform has been fit and has grains_to_keep property"""
        return getattr(transform, "_is_fit", False) and isinstance(transform, GrainDropper)

# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Mapping
from ..unique_target_grain_dropper import UniqueTargetGrainDropper
from ..short_grain_dropper import ShortGrainDropper
from .._grain_based_stateful_transformer import _GrainBasedStatefulTransformer
from .aggregate_transformer import AutoMLAggregateTransformer
from .aggregated_unique_target_grain_dropper import AggregatedUniqueTargetGrainDropper
from .aggregated_grain_dropper import AggregatedGrainDropper


class AggregatedTransformerFactory:
    """Factory for creating AutoML aggregate transformer."""
    @staticmethod
    def create_aggregated_transformer(
            mapping: Mapping[str, _GrainBasedStatefulTransformer]
    ) -> AutoMLAggregateTransformer:
        """
        Factory method of creating aggregated transformer for distributed runs.

        :param mapping: The grain-transformer key value pairs.
        """
        if any([isinstance(t, UniqueTargetGrainDropper) for t in mapping.values()]):
            return AggregatedUniqueTargetGrainDropper(mapping)
        if any([isinstance(t, ShortGrainDropper) for t in mapping.values()]):
            return AggregatedGrainDropper(mapping)
        else:
            return AutoMLAggregateTransformer(mapping)

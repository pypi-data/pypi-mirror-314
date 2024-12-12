from __future__ import annotations

from typing import Annotated

import nshconfig as C
from typing_extensions import TypeAliasType

from .base import LRSchedulerConfigBase as LRSchedulerConfigBase
from .base import LRSchedulerMetadata as LRSchedulerMetadata
from .linear_warmup_cosine import (
    LinearWarmupCosineAnnealingLR as LinearWarmupCosineAnnealingLR,
)
from .linear_warmup_cosine import (
    LinearWarmupCosineDecayLRSchedulerConfig as LinearWarmupCosineDecayLRSchedulerConfig,
)
from .reduce_lr_on_plateau import ReduceLROnPlateau as ReduceLROnPlateau
from .reduce_lr_on_plateau import ReduceLROnPlateauConfig as ReduceLROnPlateauConfig

LRSchedulerConfig = TypeAliasType(
    "LRSchedulerConfig",
    Annotated[
        LinearWarmupCosineDecayLRSchedulerConfig | ReduceLROnPlateauConfig,
        C.Field(discriminator="name"),
    ],
)

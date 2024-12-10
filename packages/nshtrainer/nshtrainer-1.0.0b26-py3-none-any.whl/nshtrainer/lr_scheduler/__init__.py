from __future__ import annotations

from typing import Annotated, TypeAlias

import nshconfig as C

from ._base import LRSchedulerConfigBase as LRSchedulerConfigBase
from ._base import LRSchedulerMetadata as LRSchedulerMetadata
from .linear_warmup_cosine import (
    LinearWarmupCosineAnnealingLR as LinearWarmupCosineAnnealingLR,
)
from .linear_warmup_cosine import (
    LinearWarmupCosineDecayLRSchedulerConfig as LinearWarmupCosineDecayLRSchedulerConfig,
)
from .reduce_lr_on_plateau import ReduceLROnPlateau as ReduceLROnPlateau
from .reduce_lr_on_plateau import ReduceLROnPlateauConfig as ReduceLROnPlateauConfig

LRSchedulerConfig: TypeAlias = Annotated[
    LinearWarmupCosineDecayLRSchedulerConfig | ReduceLROnPlateauConfig,
    C.Field(discriminator="name"),
]

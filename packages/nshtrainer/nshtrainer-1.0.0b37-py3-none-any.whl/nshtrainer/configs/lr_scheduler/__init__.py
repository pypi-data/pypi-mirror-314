from __future__ import annotations

__codegen__ = True

from nshtrainer.lr_scheduler import (
    LinearWarmupCosineDecayLRSchedulerConfig as LinearWarmupCosineDecayLRSchedulerConfig,
)
from nshtrainer.lr_scheduler import LRSchedulerConfig as LRSchedulerConfig
from nshtrainer.lr_scheduler import LRSchedulerConfigBase as LRSchedulerConfigBase
from nshtrainer.lr_scheduler import ReduceLROnPlateauConfig as ReduceLROnPlateauConfig
from nshtrainer.lr_scheduler.base import lr_scheduler_registry as lr_scheduler_registry
from nshtrainer.lr_scheduler.linear_warmup_cosine import (
    DurationConfig as DurationConfig,
)
from nshtrainer.lr_scheduler.reduce_lr_on_plateau import MetricConfig as MetricConfig

from . import base as base
from . import linear_warmup_cosine as linear_warmup_cosine
from . import reduce_lr_on_plateau as reduce_lr_on_plateau

__all__ = [
    "DurationConfig",
    "LRSchedulerConfig",
    "LRSchedulerConfigBase",
    "LinearWarmupCosineDecayLRSchedulerConfig",
    "MetricConfig",
    "ReduceLROnPlateauConfig",
    "base",
    "linear_warmup_cosine",
    "lr_scheduler_registry",
    "reduce_lr_on_plateau",
]

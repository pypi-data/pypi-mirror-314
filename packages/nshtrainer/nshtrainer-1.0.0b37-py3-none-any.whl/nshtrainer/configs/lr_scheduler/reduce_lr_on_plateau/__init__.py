from __future__ import annotations

__codegen__ = True

from nshtrainer.lr_scheduler.reduce_lr_on_plateau import (
    LRSchedulerConfigBase as LRSchedulerConfigBase,
)
from nshtrainer.lr_scheduler.reduce_lr_on_plateau import MetricConfig as MetricConfig
from nshtrainer.lr_scheduler.reduce_lr_on_plateau import (
    ReduceLROnPlateauConfig as ReduceLROnPlateauConfig,
)
from nshtrainer.lr_scheduler.reduce_lr_on_plateau import (
    lr_scheduler_registry as lr_scheduler_registry,
)

__all__ = [
    "LRSchedulerConfigBase",
    "MetricConfig",
    "ReduceLROnPlateauConfig",
    "lr_scheduler_registry",
]

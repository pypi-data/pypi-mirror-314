from __future__ import annotations

__codegen__ = True

from nshtrainer.lr_scheduler.base import LRSchedulerConfigBase as LRSchedulerConfigBase
from nshtrainer.lr_scheduler.base import lr_scheduler_registry as lr_scheduler_registry

__all__ = [
    "LRSchedulerConfigBase",
    "lr_scheduler_registry",
]

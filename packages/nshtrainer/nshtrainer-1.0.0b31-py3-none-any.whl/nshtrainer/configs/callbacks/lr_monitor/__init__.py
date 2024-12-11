from __future__ import annotations

__codegen__ = True

from nshtrainer.callbacks.lr_monitor import CallbackConfigBase as CallbackConfigBase
from nshtrainer.callbacks.lr_monitor import (
    LearningRateMonitorConfig as LearningRateMonitorConfig,
)

__all__ = [
    "CallbackConfigBase",
    "LearningRateMonitorConfig",
]

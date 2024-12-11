from __future__ import annotations

__codegen__ = True

from nshtrainer.callbacks.timer import CallbackConfigBase as CallbackConfigBase
from nshtrainer.callbacks.timer import (
    EpochTimerCallbackConfig as EpochTimerCallbackConfig,
)

__all__ = [
    "CallbackConfigBase",
    "EpochTimerCallbackConfig",
]

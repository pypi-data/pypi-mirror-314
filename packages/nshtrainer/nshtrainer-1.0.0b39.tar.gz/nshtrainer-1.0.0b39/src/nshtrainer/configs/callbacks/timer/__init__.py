from __future__ import annotations

__codegen__ = True

from nshtrainer.callbacks.timer import CallbackConfigBase as CallbackConfigBase
from nshtrainer.callbacks.timer import (
    EpochTimerCallbackConfig as EpochTimerCallbackConfig,
)
from nshtrainer.callbacks.timer import callback_registry as callback_registry

__all__ = [
    "CallbackConfigBase",
    "EpochTimerCallbackConfig",
    "callback_registry",
]

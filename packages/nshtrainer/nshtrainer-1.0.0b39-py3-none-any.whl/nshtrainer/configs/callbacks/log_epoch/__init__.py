from __future__ import annotations

__codegen__ = True

from nshtrainer.callbacks.log_epoch import CallbackConfigBase as CallbackConfigBase
from nshtrainer.callbacks.log_epoch import (
    LogEpochCallbackConfig as LogEpochCallbackConfig,
)
from nshtrainer.callbacks.log_epoch import callback_registry as callback_registry

__all__ = [
    "CallbackConfigBase",
    "LogEpochCallbackConfig",
    "callback_registry",
]

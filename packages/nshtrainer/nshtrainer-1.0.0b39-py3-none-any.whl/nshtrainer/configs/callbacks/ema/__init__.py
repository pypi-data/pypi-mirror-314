from __future__ import annotations

__codegen__ = True

from nshtrainer.callbacks.ema import CallbackConfigBase as CallbackConfigBase
from nshtrainer.callbacks.ema import EMACallbackConfig as EMACallbackConfig
from nshtrainer.callbacks.ema import callback_registry as callback_registry

__all__ = [
    "CallbackConfigBase",
    "EMACallbackConfig",
    "callback_registry",
]

from __future__ import annotations

__codegen__ = True

from nshtrainer.callbacks.debug_flag import CallbackConfigBase as CallbackConfigBase
from nshtrainer.callbacks.debug_flag import (
    DebugFlagCallbackConfig as DebugFlagCallbackConfig,
)
from nshtrainer.callbacks.debug_flag import callback_registry as callback_registry

__all__ = [
    "CallbackConfigBase",
    "DebugFlagCallbackConfig",
    "callback_registry",
]

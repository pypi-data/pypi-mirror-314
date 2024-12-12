from __future__ import annotations

__codegen__ = True

from nshtrainer.callbacks.norm_logging import CallbackConfigBase as CallbackConfigBase
from nshtrainer.callbacks.norm_logging import (
    NormLoggingCallbackConfig as NormLoggingCallbackConfig,
)
from nshtrainer.callbacks.norm_logging import callback_registry as callback_registry

__all__ = [
    "CallbackConfigBase",
    "NormLoggingCallbackConfig",
    "callback_registry",
]

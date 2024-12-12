from __future__ import annotations

__codegen__ = True

from nshtrainer.callbacks.base import CallbackConfigBase as CallbackConfigBase
from nshtrainer.callbacks.base import callback_registry as callback_registry

__all__ = [
    "CallbackConfigBase",
    "callback_registry",
]

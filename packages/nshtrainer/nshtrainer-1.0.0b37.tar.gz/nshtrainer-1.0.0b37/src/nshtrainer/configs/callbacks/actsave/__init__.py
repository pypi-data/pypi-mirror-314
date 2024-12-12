from __future__ import annotations

__codegen__ = True

from nshtrainer.callbacks.actsave import ActSaveConfig as ActSaveConfig
from nshtrainer.callbacks.actsave import CallbackConfigBase as CallbackConfigBase
from nshtrainer.callbacks.actsave import callback_registry as callback_registry

__all__ = [
    "ActSaveConfig",
    "CallbackConfigBase",
    "callback_registry",
]

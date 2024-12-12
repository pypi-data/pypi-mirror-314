from __future__ import annotations

__codegen__ = True

from nshtrainer.callbacks.directory_setup import (
    CallbackConfigBase as CallbackConfigBase,
)
from nshtrainer.callbacks.directory_setup import (
    DirectorySetupCallbackConfig as DirectorySetupCallbackConfig,
)
from nshtrainer.callbacks.directory_setup import callback_registry as callback_registry

__all__ = [
    "CallbackConfigBase",
    "DirectorySetupCallbackConfig",
    "callback_registry",
]

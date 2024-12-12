from __future__ import annotations

__codegen__ = True

from nshtrainer.callbacks.shared_parameters import (
    CallbackConfigBase as CallbackConfigBase,
)
from nshtrainer.callbacks.shared_parameters import (
    SharedParametersCallbackConfig as SharedParametersCallbackConfig,
)
from nshtrainer.callbacks.shared_parameters import (
    callback_registry as callback_registry,
)

__all__ = [
    "CallbackConfigBase",
    "SharedParametersCallbackConfig",
    "callback_registry",
]

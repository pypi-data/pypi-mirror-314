from __future__ import annotations

__codegen__ = True

from nshtrainer.callbacks.wandb_upload_code import (
    CallbackConfigBase as CallbackConfigBase,
)
from nshtrainer.callbacks.wandb_upload_code import (
    WandbUploadCodeCallbackConfig as WandbUploadCodeCallbackConfig,
)
from nshtrainer.callbacks.wandb_upload_code import (
    callback_registry as callback_registry,
)

__all__ = [
    "CallbackConfigBase",
    "WandbUploadCodeCallbackConfig",
    "callback_registry",
]

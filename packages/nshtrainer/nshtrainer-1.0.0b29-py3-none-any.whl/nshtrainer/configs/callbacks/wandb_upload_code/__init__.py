from __future__ import annotations

__codegen__ = True

from nshtrainer.callbacks.wandb_upload_code import (
    CallbackConfigBase as CallbackConfigBase,
)
from nshtrainer.callbacks.wandb_upload_code import (
    WandbUploadCodeCallbackConfig as WandbUploadCodeCallbackConfig,
)

__all__ = [
    "CallbackConfigBase",
    "WandbUploadCodeCallbackConfig",
]

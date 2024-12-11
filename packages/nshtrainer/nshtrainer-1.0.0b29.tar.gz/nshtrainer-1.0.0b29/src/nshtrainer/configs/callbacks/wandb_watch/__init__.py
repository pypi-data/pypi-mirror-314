from __future__ import annotations

__codegen__ = True

from nshtrainer.callbacks.wandb_watch import CallbackConfigBase as CallbackConfigBase
from nshtrainer.callbacks.wandb_watch import (
    WandbWatchCallbackConfig as WandbWatchCallbackConfig,
)

__all__ = [
    "CallbackConfigBase",
    "WandbWatchCallbackConfig",
]

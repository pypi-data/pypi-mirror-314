from __future__ import annotations

__codegen__ = True

from nshtrainer.loggers.wandb import BaseLoggerConfig as BaseLoggerConfig
from nshtrainer.loggers.wandb import CallbackConfigBase as CallbackConfigBase
from nshtrainer.loggers.wandb import WandbLoggerConfig as WandbLoggerConfig
from nshtrainer.loggers.wandb import (
    WandbUploadCodeCallbackConfig as WandbUploadCodeCallbackConfig,
)
from nshtrainer.loggers.wandb import (
    WandbWatchCallbackConfig as WandbWatchCallbackConfig,
)

__all__ = [
    "BaseLoggerConfig",
    "CallbackConfigBase",
    "WandbLoggerConfig",
    "WandbUploadCodeCallbackConfig",
    "WandbWatchCallbackConfig",
]

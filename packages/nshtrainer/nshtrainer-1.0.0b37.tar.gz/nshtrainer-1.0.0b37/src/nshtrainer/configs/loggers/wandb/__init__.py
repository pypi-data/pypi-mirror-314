from __future__ import annotations

__codegen__ = True

from nshtrainer.loggers.wandb import CallbackConfigBase as CallbackConfigBase
from nshtrainer.loggers.wandb import LoggerConfigBase as LoggerConfigBase
from nshtrainer.loggers.wandb import WandbLoggerConfig as WandbLoggerConfig
from nshtrainer.loggers.wandb import (
    WandbUploadCodeCallbackConfig as WandbUploadCodeCallbackConfig,
)
from nshtrainer.loggers.wandb import (
    WandbWatchCallbackConfig as WandbWatchCallbackConfig,
)
from nshtrainer.loggers.wandb import logger_registry as logger_registry

__all__ = [
    "CallbackConfigBase",
    "LoggerConfigBase",
    "WandbLoggerConfig",
    "WandbUploadCodeCallbackConfig",
    "WandbWatchCallbackConfig",
    "logger_registry",
]

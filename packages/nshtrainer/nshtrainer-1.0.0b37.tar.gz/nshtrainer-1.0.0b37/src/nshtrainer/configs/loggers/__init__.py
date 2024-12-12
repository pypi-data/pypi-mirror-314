from __future__ import annotations

__codegen__ = True

from nshtrainer.loggers import ActSaveLoggerConfig as ActSaveLoggerConfig
from nshtrainer.loggers import CSVLoggerConfig as CSVLoggerConfig
from nshtrainer.loggers import LoggerConfig as LoggerConfig
from nshtrainer.loggers import LoggerConfigBase as LoggerConfigBase
from nshtrainer.loggers import TensorboardLoggerConfig as TensorboardLoggerConfig
from nshtrainer.loggers import WandbLoggerConfig as WandbLoggerConfig
from nshtrainer.loggers import logger_registry as logger_registry
from nshtrainer.loggers.wandb import CallbackConfigBase as CallbackConfigBase
from nshtrainer.loggers.wandb import (
    WandbUploadCodeCallbackConfig as WandbUploadCodeCallbackConfig,
)
from nshtrainer.loggers.wandb import (
    WandbWatchCallbackConfig as WandbWatchCallbackConfig,
)

from . import actsave as actsave
from . import base as base
from . import csv as csv
from . import tensorboard as tensorboard
from . import wandb as wandb

__all__ = [
    "ActSaveLoggerConfig",
    "CSVLoggerConfig",
    "CallbackConfigBase",
    "LoggerConfig",
    "LoggerConfigBase",
    "TensorboardLoggerConfig",
    "WandbLoggerConfig",
    "WandbUploadCodeCallbackConfig",
    "WandbWatchCallbackConfig",
    "actsave",
    "base",
    "csv",
    "logger_registry",
    "tensorboard",
    "wandb",
]

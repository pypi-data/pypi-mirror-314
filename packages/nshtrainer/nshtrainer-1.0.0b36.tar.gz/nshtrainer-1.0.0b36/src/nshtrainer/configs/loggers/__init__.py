from __future__ import annotations

__codegen__ = True

from nshtrainer.loggers import ActSaveLoggerConfig as ActSaveLoggerConfig
from nshtrainer.loggers import BaseLoggerConfig as BaseLoggerConfig
from nshtrainer.loggers import CSVLoggerConfig as CSVLoggerConfig
from nshtrainer.loggers import LoggerConfig as LoggerConfig
from nshtrainer.loggers import TensorboardLoggerConfig as TensorboardLoggerConfig
from nshtrainer.loggers import WandbLoggerConfig as WandbLoggerConfig
from nshtrainer.loggers.wandb import CallbackConfigBase as CallbackConfigBase
from nshtrainer.loggers.wandb import (
    WandbUploadCodeCallbackConfig as WandbUploadCodeCallbackConfig,
)
from nshtrainer.loggers.wandb import (
    WandbWatchCallbackConfig as WandbWatchCallbackConfig,
)

from . import _base as _base
from . import actsave as actsave
from . import csv as csv
from . import tensorboard as tensorboard
from . import wandb as wandb

__all__ = [
    "ActSaveLoggerConfig",
    "BaseLoggerConfig",
    "CSVLoggerConfig",
    "CallbackConfigBase",
    "LoggerConfig",
    "TensorboardLoggerConfig",
    "WandbLoggerConfig",
    "WandbUploadCodeCallbackConfig",
    "WandbWatchCallbackConfig",
    "_base",
    "actsave",
    "csv",
    "tensorboard",
    "wandb",
]

from __future__ import annotations

__codegen__ = True

from nshtrainer.loggers.tensorboard import LoggerConfigBase as LoggerConfigBase
from nshtrainer.loggers.tensorboard import (
    TensorboardLoggerConfig as TensorboardLoggerConfig,
)
from nshtrainer.loggers.tensorboard import logger_registry as logger_registry

__all__ = [
    "LoggerConfigBase",
    "TensorboardLoggerConfig",
    "logger_registry",
]

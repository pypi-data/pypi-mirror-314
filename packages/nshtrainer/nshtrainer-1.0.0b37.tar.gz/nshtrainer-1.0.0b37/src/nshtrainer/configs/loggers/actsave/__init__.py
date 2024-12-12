from __future__ import annotations

__codegen__ = True

from nshtrainer.loggers.actsave import ActSaveLoggerConfig as ActSaveLoggerConfig
from nshtrainer.loggers.actsave import LoggerConfigBase as LoggerConfigBase
from nshtrainer.loggers.actsave import logger_registry as logger_registry

__all__ = [
    "ActSaveLoggerConfig",
    "LoggerConfigBase",
    "logger_registry",
]

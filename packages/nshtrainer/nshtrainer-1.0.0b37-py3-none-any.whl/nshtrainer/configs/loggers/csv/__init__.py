from __future__ import annotations

__codegen__ = True

from nshtrainer.loggers.csv import CSVLoggerConfig as CSVLoggerConfig
from nshtrainer.loggers.csv import LoggerConfigBase as LoggerConfigBase
from nshtrainer.loggers.csv import logger_registry as logger_registry

__all__ = [
    "CSVLoggerConfig",
    "LoggerConfigBase",
    "logger_registry",
]

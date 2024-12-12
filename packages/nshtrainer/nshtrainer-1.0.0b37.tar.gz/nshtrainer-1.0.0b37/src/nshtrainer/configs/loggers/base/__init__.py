from __future__ import annotations

__codegen__ = True

from nshtrainer.loggers.base import LoggerConfigBase as LoggerConfigBase
from nshtrainer.loggers.base import logger_registry as logger_registry

__all__ = [
    "LoggerConfigBase",
    "logger_registry",
]

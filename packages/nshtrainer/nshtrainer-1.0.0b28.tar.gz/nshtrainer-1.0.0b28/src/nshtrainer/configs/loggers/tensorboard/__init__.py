from __future__ import annotations

__codegen__ = True

from nshtrainer.loggers.tensorboard import BaseLoggerConfig as BaseLoggerConfig
from nshtrainer.loggers.tensorboard import (
    TensorboardLoggerConfig as TensorboardLoggerConfig,
)

__all__ = [
    "BaseLoggerConfig",
    "TensorboardLoggerConfig",
]

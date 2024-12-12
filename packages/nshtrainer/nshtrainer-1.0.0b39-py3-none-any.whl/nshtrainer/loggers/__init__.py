from __future__ import annotations

from typing import Annotated

import nshconfig as C
from typing_extensions import TypeAliasType

from .actsave import ActSaveLoggerConfig as ActSaveLoggerConfig
from .base import LoggerConfigBase as LoggerConfigBase
from .base import logger_registry as logger_registry
from .csv import CSVLoggerConfig as CSVLoggerConfig
from .tensorboard import TensorboardLoggerConfig as TensorboardLoggerConfig
from .wandb import WandbLoggerConfig as WandbLoggerConfig

LoggerConfig = TypeAliasType(
    "LoggerConfig",
    Annotated[LoggerConfigBase, logger_registry.DynamicResolution()],
)

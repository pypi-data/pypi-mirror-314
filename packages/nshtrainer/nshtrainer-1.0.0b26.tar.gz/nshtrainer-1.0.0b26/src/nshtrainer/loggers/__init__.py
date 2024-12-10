from __future__ import annotations

from typing import Annotated, TypeAlias

import nshconfig as C

from ._base import BaseLoggerConfig as BaseLoggerConfig
from .actsave import ActSaveLoggerConfig as ActSaveLoggerConfig
from .csv import CSVLoggerConfig as CSVLoggerConfig
from .tensorboard import TensorboardLoggerConfig as TensorboardLoggerConfig
from .wandb import WandbLoggerConfig as WandbLoggerConfig

LoggerConfig: TypeAlias = Annotated[
    CSVLoggerConfig | TensorboardLoggerConfig | WandbLoggerConfig | ActSaveLoggerConfig,
    C.Field(discriminator="name"),
]

from __future__ import annotations

from typing import Annotated

import nshconfig as C
from typing_extensions import TypeAliasType

from ._base import BaseLoggerConfig as BaseLoggerConfig
from .actsave import ActSaveLoggerConfig as ActSaveLoggerConfig
from .csv import CSVLoggerConfig as CSVLoggerConfig
from .tensorboard import TensorboardLoggerConfig as TensorboardLoggerConfig
from .wandb import WandbLoggerConfig as WandbLoggerConfig

LoggerConfig = TypeAliasType(
    "LoggerConfig",
    Annotated[
        CSVLoggerConfig
        | TensorboardLoggerConfig
        | WandbLoggerConfig
        | ActSaveLoggerConfig,
        C.Field(discriminator="name"),
    ],
)

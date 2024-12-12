from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import nshconfig as C
from lightning.pytorch.loggers import Logger

if TYPE_CHECKING:
    from ..trainer._config import TrainerConfig


class LoggerConfigBase(C.Config, ABC):
    enabled: bool = True
    """Enable this logger."""

    priority: int = 0
    """Priority of the logger. Higher priority loggers are created first."""

    log_dir: C.DirectoryPath | None = None
    """Directory to save the logs to. If None, will use the default log directory for the trainer."""

    @abstractmethod
    def create_logger(self, trainer_config: TrainerConfig) -> Logger | None: ...

    def disable_(self):
        self.enabled = False
        return self

    def __bool__(self):
        return self.enabled

    def resolve_logger_dirname(self) -> str:
        if not (name := getattr(self, "name", None)):
            raise ValueError(
                "Logger must have a name attribute to resolve the directory name.\n"
                "Otherwise, you must override `resolve_logger_dirname`."
            )

        return name


logger_registry = C.Registry(LoggerConfigBase, discriminator="name")

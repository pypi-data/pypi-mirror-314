from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

import nshconfig as C
from lightning.pytorch.profilers import Profiler

if TYPE_CHECKING:
    from ..trainer._config import TrainerConfig

log = logging.getLogger(__name__)


class BaseProfilerConfig(C.Config, ABC):
    dirpath: str | Path | None = None
    """
    Directory path for the ``filename``. If ``dirpath`` is ``None`` but ``filename`` is present, the
        ``trainer.log_dir`` (from :class:`~lightning.pytorch.loggers.tensorboard.TensorBoardLogger`)
        will be used.
    """
    filename: str | None = None
    """
    If present, filename where the profiler results will be saved instead of printing to stdout.
        The ``.txt`` extension will be used automatically.
    """

    @abstractmethod
    def create_profiler(self, trainer_config: TrainerConfig) -> Profiler | None: ...

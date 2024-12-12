from __future__ import annotations

from argparse import Namespace
from typing import Any, Literal

import numpy as np
from lightning.pytorch.loggers import Logger
from typing_extensions import final

from .base import LoggerConfigBase, logger_registry


@final
@logger_registry.register
class ActSaveLoggerConfig(LoggerConfigBase):
    name: Literal["actsave"] = "actsave"

    def create_logger(self, trainer_config):
        if not self.enabled:
            return None

        return ActSaveLogger()


class ActSaveLogger(Logger):
    @property
    def name(self):
        return None

    @property
    def version(self):
        from nshutils import ActSave

        if ActSave._saver is None:
            return None

        return ActSave._saver._id

    @property
    def save_dir(self):
        from nshutils import ActSave

        if ActSave._saver is None:
            return None

        return str(ActSave._saver._save_dir)

    def log_hyperparams(
        self,
        params: dict[str, Any] | Namespace,
        *args: Any,
        **kwargs: Any,
    ):
        from nshutils import ActSave

        # Wrap the hparams as a object-dtype np array
        return ActSave.save({"hyperparameters": np.array(params, dtype=object)})

    def log_metrics(self, metrics: dict[str, float], step: int | None = None) -> None:
        from nshutils import ActSave

        ActSave.save({**metrics})

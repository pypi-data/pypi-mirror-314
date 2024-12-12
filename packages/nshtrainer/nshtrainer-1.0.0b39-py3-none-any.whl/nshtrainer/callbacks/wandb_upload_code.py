from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Literal, cast

from lightning.pytorch import LightningModule, Trainer
from lightning.pytorch.callbacks.callback import Callback
from lightning.pytorch.loggers import WandbLogger
from nshrunner._env import SNAPSHOT_DIR
from typing_extensions import final, override

from .base import CallbackConfigBase, callback_registry

log = logging.getLogger(__name__)


@final
@callback_registry.register
class WandbUploadCodeCallbackConfig(CallbackConfigBase):
    name: Literal["wandb_upload_code"] = "wandb_upload_code"

    enabled: bool = True
    """Enable uploading the code to wandb."""

    def __bool__(self):
        return self.enabled

    @override
    def create_callbacks(self, trainer_config):
        if not self:
            return

        yield WandbUploadCodeCallback(self)


class WandbUploadCodeCallback(Callback):
    def __init__(self, config: WandbUploadCodeCallbackConfig):
        super().__init__()

        self.config = config

    @override
    def setup(self, trainer: Trainer, pl_module: LightningModule, stage: str):
        if not self.config:
            return

        if not trainer.is_global_zero:
            return

        if (
            logger := next(
                (
                    logger
                    for logger in trainer.loggers
                    if isinstance(logger, WandbLogger)
                ),
                None,
            )
        ) is None:
            log.warning("Wandb logger not found. Skipping code upload.")
            return

        from wandb.wandb_run import Run

        run = cast(Run, logger.experiment)

        # If a snapshot has been taken (which can be detected using the SNAPSHOT_DIR env),
        # then upload all contents within the snapshot directory to the repository.
        if not (snapshot_dir := os.environ.get(SNAPSHOT_DIR)):
            log.debug("No snapshot directory found. Skipping upload.")
            return

        snapshot_dir = Path(snapshot_dir)
        if not snapshot_dir.exists() or not snapshot_dir.is_dir():
            log.warning(
                f"Snapshot directory '{snapshot_dir}' does not exist or is not a directory."
            )
            return

        log.info(f"Uploading code from snapshot directory '{snapshot_dir}'")
        run.log_code(str(snapshot_dir.absolute()))

from __future__ import annotations

import logging
from typing import Literal

from lightning.pytorch import LightningModule, Trainer
from typing_extensions import final, override

from ..._checkpoint.metadata import CheckpointMetadata
from ._base import BaseCheckpointCallbackConfig, CheckpointBase

log = logging.getLogger(__name__)


@final
class LastCheckpointCallbackConfig(BaseCheckpointCallbackConfig):
    name: Literal["last_checkpoint"] = "last_checkpoint"

    @override
    def create_checkpoint(self, trainer_config, dirpath):
        return LastCheckpointCallback(self, dirpath)


@final
class LastCheckpointCallback(CheckpointBase[LastCheckpointCallbackConfig]):
    @override
    def name(self):
        return "last"

    @override
    def default_filename(self):
        return "epoch{epoch}-step{step}"

    @override
    def topk_sort_key(self, metadata: CheckpointMetadata):
        return metadata.checkpoint_timestamp

    @override
    def topk_sort_reverse(self):
        return True

    @override
    def on_validation_epoch_end(self, trainer: Trainer, pl_module: LightningModule):
        self.save_checkpoints(trainer)

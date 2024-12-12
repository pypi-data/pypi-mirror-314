from __future__ import annotations

import logging
import time
from datetime import timedelta
from pathlib import Path
from typing import Any, Literal

from lightning.pytorch import LightningModule, Trainer
from typing_extensions import final, override

from ..._checkpoint.metadata import CheckpointMetadata
from ..base import callback_registry
from ._base import BaseCheckpointCallbackConfig, CheckpointBase

log = logging.getLogger(__name__)


@final
@callback_registry.register
class LastCheckpointCallbackConfig(BaseCheckpointCallbackConfig):
    name: Literal["last_checkpoint"] = "last_checkpoint"

    save_on_time_interval: timedelta | None = None
    """Save a checkpoint every `save_on_time_interval` seconds. If `None`, this feature is disabled."""

    @override
    def create_checkpoint(self, trainer_config, dirpath):
        return LastCheckpointCallback(self, dirpath)


@final
class LastCheckpointCallback(CheckpointBase[LastCheckpointCallbackConfig]):
    def __init__(self, config: LastCheckpointCallbackConfig, dirpath: Path):
        super().__init__(config, dirpath)
        self.start_time = time.time()
        self.last_checkpoint_time = self.start_time

    @override
    def name(self):
        return "last"

    @override
    def default_filename(self):
        return "epoch{epoch}-step{step}-duration{train_duration}"

    @override
    def topk_sort_key(self, metadata: CheckpointMetadata):
        return metadata.checkpoint_timestamp

    @override
    def topk_sort_reverse(self):
        return True

    def _local_should_checkpoint(self) -> bool:
        if (interval := self.config.save_on_time_interval) is None:
            return False

        current_time = time.time()
        elapsed_time = current_time - self.last_checkpoint_time
        return elapsed_time >= interval.total_seconds()

    def _should_checkpoint(self, trainer: Trainer):
        if self.config.save_on_time_interval is None:
            return False
        return trainer.strategy.broadcast(self._local_should_checkpoint(), src=0)

    def _format_duration(self, seconds: float) -> str:
        """Format duration in seconds to a human-readable string."""
        td = timedelta(seconds=int(seconds))
        days = td.days
        hours, remainder = divmod(td.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        if seconds > 0 or not parts:
            parts.append(f"{seconds}s")

        return "_".join(parts)

    @override
    def current_metrics(self, trainer: Trainer) -> dict[str, Any]:
        metrics = super().current_metrics(trainer)
        train_duration = time.time() - self.start_time
        metrics["train_duration"] = self._format_duration(train_duration)
        return metrics

    @override
    def on_train_batch_end(
        self,
        trainer: Trainer,
        pl_module: LightningModule,
        *args,
        **kwargs,
    ):
        if not self._should_checkpoint(trainer):
            return
        self.save_checkpoints(trainer)

    @override
    def on_validation_epoch_end(self, trainer: Trainer, pl_module: LightningModule):
        self.save_checkpoints(trainer)

    @override
    def save_checkpoints(self, trainer):
        super().save_checkpoints(trainer)

        if self.config.save_on_time_interval is not None:
            self.last_checkpoint_time = time.time()

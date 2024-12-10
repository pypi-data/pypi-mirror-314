from __future__ import annotations

import logging
import time
from datetime import timedelta
from pathlib import Path
from typing import Any, Literal

from lightning.pytorch import LightningModule, Trainer
from typing_extensions import final, override

from nshtrainer._checkpoint.metadata import CheckpointMetadata

from ._base import BaseCheckpointCallbackConfig, CheckpointBase

log = logging.getLogger(__name__)


@final
class TimeCheckpointCallbackConfig(BaseCheckpointCallbackConfig):
    name: Literal["time_checkpoint"] = "time_checkpoint"

    interval: timedelta = timedelta(hours=12)
    """Time interval between checkpoints."""

    @override
    def create_checkpoint(self, trainer_config, dirpath):
        return TimeCheckpointCallback(self, dirpath)


@final
class TimeCheckpointCallback(CheckpointBase[TimeCheckpointCallbackConfig]):
    def __init__(self, config: TimeCheckpointCallbackConfig, dirpath: Path):
        super().__init__(config, dirpath)
        self.start_time = time.time()
        self.last_checkpoint_time = self.start_time
        self.interval_seconds = config.interval.total_seconds()

    @override
    def name(self):
        return "time"

    @override
    def default_filename(self):
        return "epoch{epoch}-step{step}-duration{train_duration}"

    @override
    def topk_sort_key(self, metadata: CheckpointMetadata):
        return metadata.checkpoint_timestamp

    @override
    def topk_sort_reverse(self):
        return True

    def _should_checkpoint(self) -> bool:
        current_time = time.time()
        elapsed_time = current_time - self.last_checkpoint_time
        return elapsed_time >= self.interval_seconds

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
        self, trainer: Trainer, pl_module: LightningModule, *args, **kwargs
    ):
        if self._should_checkpoint():
            self.save_checkpoints(trainer)
            self.last_checkpoint_time = time.time()

    @override
    def state_dict(self) -> dict[str, Any]:
        """Save the timer state for checkpoint resumption.

        Returns:
            Dictionary containing the start time and last checkpoint time.
        """
        return {
            "start_time": self.start_time,
            "last_checkpoint_time": self.last_checkpoint_time,
        }

    @override
    def load_state_dict(self, state_dict: dict[str, Any]) -> None:
        """Restore the timer state when resuming from a checkpoint.

        Args:
            state_dict: Dictionary containing the previously saved timer state.
        """
        self.start_time = state_dict["start_time"]
        self.last_checkpoint_time = state_dict["last_checkpoint_time"]

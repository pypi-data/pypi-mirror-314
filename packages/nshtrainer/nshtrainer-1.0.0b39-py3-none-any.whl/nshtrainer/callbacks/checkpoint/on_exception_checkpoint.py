from __future__ import annotations

import contextlib
import datetime
import logging
import os
from pathlib import Path
from typing import Any, Literal

from lightning.pytorch import Trainer as LightningTrainer
from lightning.pytorch.callbacks import OnExceptionCheckpoint as _OnExceptionCheckpoint
from typing_extensions import final, override

from ..base import CallbackConfigBase, callback_registry

log = logging.getLogger(__name__)


@contextlib.contextmanager
def _monkey_patch_disable_barrier(trainer: LightningTrainer):
    """
    Monkey-patch the strategy instance to make the barrier operation a no-op.

    We do this because `save_checkpoint` calls `barrier`. This is okay in most
    cases, but when we want to save a checkpoint in the case of an exception,
    `barrier` causes a deadlock. So we monkey-patch the strategy instance to
    make the barrier operation a no-op.
    """

    # We monkey-patch the barrier method to do nothing.
    original_barrier = trainer.strategy.barrier

    def new_barrier(*args, **kwargs):
        log.warning("Monkey-patched no-op barrier.")
        pass

    trainer.strategy.barrier = new_barrier
    log.warning("Monkey-patched barrier to no-op.")

    try:
        yield
    finally:
        trainer.strategy.barrier = original_barrier
        log.warning("Reverted monkey-patched barrier.")


@final
@callback_registry.register
class OnExceptionCheckpointCallbackConfig(CallbackConfigBase):
    name: Literal["on_exception_checkpoint"] = "on_exception_checkpoint"

    dirpath: str | Path | None = None
    """Directory path to save the checkpoint file."""

    filename: str | None = None
    """Checkpoint filename. This must not include the extension. If `None`, `on_exception_{id}_{timestamp}` is used."""

    @override
    def create_callbacks(self, trainer_config):
        dirpath = self.dirpath or trainer_config.directory.resolve_subdirectory(
            trainer_config.id, "checkpoint"
        )

        if not (filename := self.filename):
            filename = f"on_exception_{trainer_config.id}"
        yield OnExceptionCheckpointCallback(
            self, dirpath=Path(dirpath), filename=filename
        )


class OnExceptionCheckpointCallback(_OnExceptionCheckpoint):
    @override
    def __init__(
        self,
        config: OnExceptionCheckpointCallbackConfig,
        dirpath: Path,
        filename: str,
    ):
        self.config = config
        del config

        dirpath = dirpath / "on_exception"
        dirpath.mkdir(parents=True, exist_ok=True)

        super().__init__(dirpath, filename)

    @property
    @override
    def ckpt_path(self) -> str:
        ckpt_path = super().ckpt_path

        # Remve the extension and add the current timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        ckpt_path, ext = os.path.splitext(ckpt_path)
        return f"{ckpt_path}_{timestamp}{ext}"

    @override
    def on_exception(self, trainer: LightningTrainer, *args: Any, **kwargs: Any):
        # Monkey-patch the strategy instance to make the barrier operation a no-op.
        # We do this because `save_checkpoint` calls `barrier`. This is okay in most
        #   cases, but when we want to save a checkpoint in the case of an exception,
        #   `barrier` causes a deadlock. So we monkey-patch the strategy instance to
        #   make the barrier operation a no-op.
        with _monkey_patch_disable_barrier(trainer):
            return super().on_exception(trainer, *args, **kwargs)

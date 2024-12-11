from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import torch
from lightning.pytorch.callbacks import Callback as _LightningCallback
from lightning.pytorch.utilities.types import STEP_OUTPUT
from torch.optim import Optimizer

if TYPE_CHECKING:
    from .model import LightningModuleBase
    from .trainer import Trainer


class NTCallbackBase(_LightningCallback):
    def setup(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, trainer: Trainer, pl_module: LightningModuleBase, stage: str
    ) -> None:
        """Called when fit, validate, test, predict, or tune begins."""

    def teardown(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, trainer: Trainer, pl_module: LightningModuleBase, stage: str
    ) -> None:
        """Called when fit, validate, test, predict, or tune ends."""

    def on_fit_start(self, trainer: Trainer, pl_module: LightningModuleBase) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        """Called when fit begins."""

    def on_fit_end(self, trainer: Trainer, pl_module: LightningModuleBase) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        """Called when fit ends."""

    def on_sanity_check_start(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, trainer: Trainer, pl_module: LightningModuleBase
    ) -> None:
        """Called when the validation sanity check starts."""

    def on_sanity_check_end(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, trainer: Trainer, pl_module: LightningModuleBase
    ) -> None:
        """Called when the validation sanity check ends."""

    def on_train_batch_start(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        trainer: Trainer,
        pl_module: LightningModuleBase,
        batch: Any,
        batch_idx: int,
    ) -> None:
        """Called when the train batch begins."""

    def on_train_batch_end(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        trainer: Trainer,
        pl_module: LightningModuleBase,
        outputs: STEP_OUTPUT,
        batch: Any,
        batch_idx: int,
    ) -> None:
        """Called when the train batch ends.

        Note:
            The value ``outputs["loss"]`` here will be the normalized value w.r.t ``accumulate_grad_batches`` of the
            loss returned from ``training_step``.

        """

    def on_train_epoch_start(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, trainer: Trainer, pl_module: LightningModuleBase
    ) -> None:
        """Called when the train epoch begins."""

    def on_train_epoch_end(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, trainer: Trainer, pl_module: LightningModuleBase
    ) -> None:
        """Called when the train epoch ends.

        To access all batch outputs at the end of the epoch, you can cache step outputs as an attribute of the
        :class:`lightning.pytorch.core.LightningModule` and access them in this hook:

        .. code-block:: python

            class MyLightningModule(L.LightningModule):
                 def __init__(self):
                    super().__init__() # pyright: ignore[reportIncompatibleMethodOverride]
                    self.training_step_outputs = []

                 def training_step(self):
                    loss = ... # pyright: ignore[reportIncompatibleMethodOverride]
                    self.training_step_outputs.append(loss)
                    return loss


            class MyCallback(L.Callback):
                 def on_train_epoch_end(self, trainer, pl_module):
                    # do something with all training_step outputs, for example: # pyright: ignore[reportIncompatibleMethodOverride]
                    epoch_mean = torch.stack(pl_module.training_step_outputs).mean()
                    pl_module.log("training_epoch_mean", epoch_mean)
                    # free up the memory
                    pl_module.training_step_outputs.clear()

        """

    def on_validation_epoch_start(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, trainer: Trainer, pl_module: LightningModuleBase
    ) -> None:
        """Called when the val epoch begins."""

    def on_validation_epoch_end(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, trainer: Trainer, pl_module: LightningModuleBase
    ) -> None:
        """Called when the val epoch ends."""

    def on_test_epoch_start(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, trainer: Trainer, pl_module: LightningModuleBase
    ) -> None:
        """Called when the test epoch begins."""

    def on_test_epoch_end(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, trainer: Trainer, pl_module: LightningModuleBase
    ) -> None:
        """Called when the test epoch ends."""

    def on_predict_epoch_start(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, trainer: Trainer, pl_module: LightningModuleBase
    ) -> None:
        """Called when the predict epoch begins."""

    def on_predict_epoch_end(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, trainer: Trainer, pl_module: LightningModuleBase
    ) -> None:
        """Called when the predict epoch ends."""

    def on_validation_batch_start(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        trainer: Trainer,
        pl_module: LightningModuleBase,
        batch: Any,
        batch_idx: int,
        dataloader_idx: int = 0,
    ) -> None:
        """Called when the validation batch begins."""

    def on_validation_batch_end(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        trainer: Trainer,
        pl_module: LightningModuleBase,
        outputs: STEP_OUTPUT,
        batch: Any,
        batch_idx: int,
        dataloader_idx: int = 0,
    ) -> None:
        """Called when the validation batch ends."""

    def on_test_batch_start(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        trainer: Trainer,
        pl_module: LightningModuleBase,
        batch: Any,
        batch_idx: int,
        dataloader_idx: int = 0,
    ) -> None:
        """Called when the test batch begins."""

    def on_test_batch_end(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        trainer: Trainer,
        pl_module: LightningModuleBase,
        outputs: STEP_OUTPUT,
        batch: Any,
        batch_idx: int,
        dataloader_idx: int = 0,
    ) -> None:
        """Called when the test batch ends."""

    def on_predict_batch_start(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        trainer: Trainer,
        pl_module: LightningModuleBase,
        batch: Any,
        batch_idx: int,
        dataloader_idx: int = 0,
    ) -> None:
        """Called when the predict batch begins."""

    def on_predict_batch_end(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        trainer: Trainer,
        pl_module: LightningModuleBase,
        outputs: Any,
        batch: Any,
        batch_idx: int,
        dataloader_idx: int = 0,
    ) -> None:
        """Called when the predict batch ends."""

    def on_train_start(self, trainer: Trainer, pl_module: LightningModuleBase) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        """Called when the train begins."""

    def on_train_end(self, trainer: Trainer, pl_module: LightningModuleBase) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        """Called when the train ends."""

    def on_validation_start(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, trainer: Trainer, pl_module: LightningModuleBase
    ) -> None:
        """Called when the validation loop begins."""

    def on_validation_end(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, trainer: Trainer, pl_module: LightningModuleBase
    ) -> None:
        """Called when the validation loop ends."""

    def on_test_start(self, trainer: Trainer, pl_module: LightningModuleBase) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        """Called when the test begins."""

    def on_test_end(self, trainer: Trainer, pl_module: LightningModuleBase) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        """Called when the test ends."""

    def on_predict_start(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, trainer: Trainer, pl_module: LightningModuleBase
    ) -> None:
        """Called when the predict begins."""

    def on_predict_end(self, trainer: Trainer, pl_module: LightningModuleBase) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        """Called when predict ends."""

    def on_exception(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        trainer: Trainer,
        pl_module: LightningModuleBase,
        exception: BaseException,
    ) -> None:
        """Called when any trainer execution is interrupted by an exception."""

    def state_dict(self) -> dict[str, Any]:  # pyright: ignore[reportIncompatibleMethodOverride]
        """Called when saving a checkpoint, implement to generate callback's ``state_dict``.

        Returns:
            A dictionary containing callback state.

        """
        return {}

    def load_state_dict(self, state_dict: dict[str, Any]) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        """Called when loading a checkpoint, implement to reload callback state given callback's ``state_dict``.

        Args:
            state_dict: the callback state returned by ``state_dict``.

        """
        pass

    def on_save_checkpoint(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        trainer: Trainer,
        pl_module: LightningModuleBase,
        checkpoint: dict[str, Any],
    ) -> None:
        r"""Called when saving a checkpoint to give you a chance to store anything else you might want to save.

        Args:
            trainer: the current :class:`~lightning.pytorch.trainer.trainer.Trainer` instance.
            pl_module: the current :class:`~lightning.pytorch.core.LightningModule` instance.
            checkpoint: the checkpoint dictionary that will be saved.

        """

    def on_load_checkpoint(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        trainer: Trainer,
        pl_module: LightningModuleBase,
        checkpoint: dict[str, Any],
    ) -> None:
        r"""Called when loading a model checkpoint, use to reload state.

        Args:
            trainer: the current :class:`~lightning.pytorch.trainer.trainer.Trainer` instance.
            pl_module: the current :class:`~lightning.pytorch.core.LightningModule` instance.
            checkpoint: the full checkpoint dictionary that got loaded by the Trainer.

        """

    def on_before_backward(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, trainer: Trainer, pl_module: LightningModuleBase, loss: torch.Tensor
    ) -> None:
        """Called before ``loss.backward()``."""

    def on_after_backward(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, trainer: Trainer, pl_module: LightningModuleBase
    ) -> None:
        """Called after ``loss.backward()`` and before optimizers are stepped."""

    def on_before_optimizer_step(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        trainer: Trainer,
        pl_module: LightningModuleBase,
        optimizer: Optimizer,
    ) -> None:
        """Called before ``optimizer.step()``."""

    def on_before_zero_grad(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        trainer: Trainer,
        pl_module: LightningModuleBase,
        optimizer: Optimizer,
    ) -> None:
        """Called before ``optimizer.zero_grad()``."""

    def on_checkpoint_saved(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        ckpt_path: Path,
        metadata_path: Path | None,
        trainer: "Trainer",
        pl_module: "LightningModuleBase",
    ) -> None:
        """Called after a checkpoint is saved."""
        pass


def _call_on_checkpoint_saved(
    trainer: "Trainer",
    ckpt_path: str | Path,
    metadata_path: str | Path | None,
):
    ckpt_path = Path(ckpt_path)
    metadata_path = Path(metadata_path) if metadata_path else None

    for callback in trainer.callbacks:
        if not isinstance(callback, NTCallbackBase):
            continue

        callback.on_checkpoint_saved(
            ckpt_path,
            metadata_path,
            trainer,
            trainer._base_module,
        )

from __future__ import annotations

from typing import Literal

from lightning.pytorch.plugins.io import CheckpointIO
from typing_extensions import override

from .base import PluginConfig, PluginConfigBase, plugin_registry


@plugin_registry.register
class AsyncCheckpointIOPlugin(PluginConfigBase):
    name: Literal["async_checkpoint"] = "async_checkpoint"

    """Enables saving the checkpoints asynchronously in a thread.

    .. warning::  This is an experimental feature.
    """

    checkpoint_io: PluginConfig | None = None
    """A checkpoint IO plugin that is used as the basis for async checkpointing."""

    @override
    def create_plugin(self, trainer_config) -> CheckpointIO:
        from lightning.pytorch.plugins.io.async_plugin import AsyncCheckpointIO

        base_io = (
            self.checkpoint_io.create_plugin(trainer_config)
            if self.checkpoint_io
            else None
        )
        if base_io is not None and not isinstance(base_io, CheckpointIO):
            raise TypeError(
                f"Expected `checkpoint_io` to be a `CheckpointIO` instance, but got {type(base_io)}."
            )
        return AsyncCheckpointIO(checkpoint_io=base_io)


@plugin_registry.register
class TorchCheckpointIOPlugin(PluginConfigBase):
    name: Literal["torch_checkpoint"] = "torch_checkpoint"

    """CheckpointIO that utilizes torch.save and torch.load to save and load checkpoints respectively."""

    @override
    def create_plugin(self, trainer_config) -> CheckpointIO:
        from lightning.fabric.plugins.io.torch_io import TorchCheckpointIO

        return TorchCheckpointIO()


@plugin_registry.register
class XLACheckpointIOPlugin(PluginConfigBase):
    name: Literal["xla_checkpoint"] = "xla_checkpoint"

    """CheckpointIO that utilizes xm.save to save checkpoints for TPU training strategies."""

    @override
    def create_plugin(self, trainer_config) -> CheckpointIO:
        from lightning.fabric.plugins.io.xla import XLACheckpointIO

        return XLACheckpointIO()

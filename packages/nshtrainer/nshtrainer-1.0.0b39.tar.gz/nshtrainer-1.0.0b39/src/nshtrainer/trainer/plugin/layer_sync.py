from __future__ import annotations

from typing import Literal

from lightning.pytorch.plugins.layer_sync import LayerSync
from typing_extensions import override

from .base import PluginConfigBase, plugin_registry


@plugin_registry.register
class TorchSyncBatchNormPlugin(PluginConfigBase):
    name: Literal["torch_sync_batchnorm"] = "torch_sync_batchnorm"

    """A plugin that wraps all batch normalization layers of a model with synchronization
    logic for multiprocessing.

    This plugin has no effect in single-device operation.
    """

    @override
    def create_plugin(self, trainer_config) -> LayerSync:
        from lightning.pytorch.plugins.layer_sync import TorchSyncBatchNorm

        return TorchSyncBatchNorm()

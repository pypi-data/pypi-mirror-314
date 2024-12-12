from __future__ import annotations

__codegen__ = True

from nshtrainer.trainer.plugin.layer_sync import PluginConfigBase as PluginConfigBase
from nshtrainer.trainer.plugin.layer_sync import (
    TorchSyncBatchNormPlugin as TorchSyncBatchNormPlugin,
)
from nshtrainer.trainer.plugin.layer_sync import plugin_registry as plugin_registry

__all__ = [
    "PluginConfigBase",
    "TorchSyncBatchNormPlugin",
    "plugin_registry",
]

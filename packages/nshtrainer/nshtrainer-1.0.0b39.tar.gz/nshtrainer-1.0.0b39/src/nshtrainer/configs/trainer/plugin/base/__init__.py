from __future__ import annotations

__codegen__ = True

from nshtrainer.trainer.plugin.base import PluginConfig as PluginConfig
from nshtrainer.trainer.plugin.base import PluginConfigBase as PluginConfigBase
from nshtrainer.trainer.plugin.base import plugin_registry as plugin_registry

__all__ = [
    "PluginConfig",
    "PluginConfigBase",
    "plugin_registry",
]

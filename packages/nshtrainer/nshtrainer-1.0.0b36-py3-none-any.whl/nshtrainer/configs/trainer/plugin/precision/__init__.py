from __future__ import annotations

__codegen__ = True

from nshtrainer.trainer.plugin.precision import (
    BitsandbytesPluginConfig as BitsandbytesPluginConfig,
)
from nshtrainer.trainer.plugin.precision import (
    DeepSpeedPluginConfig as DeepSpeedPluginConfig,
)
from nshtrainer.trainer.plugin.precision import (
    DoublePrecisionPluginConfig as DoublePrecisionPluginConfig,
)
from nshtrainer.trainer.plugin.precision import DTypeConfig as DTypeConfig
from nshtrainer.trainer.plugin.precision import (
    FSDPPrecisionPluginConfig as FSDPPrecisionPluginConfig,
)
from nshtrainer.trainer.plugin.precision import (
    HalfPrecisionPluginConfig as HalfPrecisionPluginConfig,
)
from nshtrainer.trainer.plugin.precision import (
    MixedPrecisionPluginConfig as MixedPrecisionPluginConfig,
)
from nshtrainer.trainer.plugin.precision import PluginConfigBase as PluginConfigBase
from nshtrainer.trainer.plugin.precision import (
    TransformerEnginePluginConfig as TransformerEnginePluginConfig,
)
from nshtrainer.trainer.plugin.precision import XLAPluginConfig as XLAPluginConfig
from nshtrainer.trainer.plugin.precision import plugin_registry as plugin_registry

__all__ = [
    "BitsandbytesPluginConfig",
    "DTypeConfig",
    "DeepSpeedPluginConfig",
    "DoublePrecisionPluginConfig",
    "FSDPPrecisionPluginConfig",
    "HalfPrecisionPluginConfig",
    "MixedPrecisionPluginConfig",
    "PluginConfigBase",
    "TransformerEnginePluginConfig",
    "XLAPluginConfig",
    "plugin_registry",
]

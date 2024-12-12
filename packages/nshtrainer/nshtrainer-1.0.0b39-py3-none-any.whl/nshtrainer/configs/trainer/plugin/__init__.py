from __future__ import annotations

__codegen__ = True

from nshtrainer.trainer.plugin import PluginConfig as PluginConfig
from nshtrainer.trainer.plugin import PluginConfigBase as PluginConfigBase
from nshtrainer.trainer.plugin import plugin_registry as plugin_registry
from nshtrainer.trainer.plugin.environment import (
    KubeflowEnvironmentPlugin as KubeflowEnvironmentPlugin,
)
from nshtrainer.trainer.plugin.environment import (
    LightningEnvironmentPlugin as LightningEnvironmentPlugin,
)
from nshtrainer.trainer.plugin.environment import (
    LSFEnvironmentPlugin as LSFEnvironmentPlugin,
)
from nshtrainer.trainer.plugin.environment import (
    MPIEnvironmentPlugin as MPIEnvironmentPlugin,
)
from nshtrainer.trainer.plugin.environment import (
    SLURMEnvironmentPlugin as SLURMEnvironmentPlugin,
)
from nshtrainer.trainer.plugin.environment import (
    TorchElasticEnvironmentPlugin as TorchElasticEnvironmentPlugin,
)
from nshtrainer.trainer.plugin.environment import (
    XLAEnvironmentPlugin as XLAEnvironmentPlugin,
)
from nshtrainer.trainer.plugin.io import (
    AsyncCheckpointIOPlugin as AsyncCheckpointIOPlugin,
)
from nshtrainer.trainer.plugin.io import (
    TorchCheckpointIOPlugin as TorchCheckpointIOPlugin,
)
from nshtrainer.trainer.plugin.io import XLACheckpointIOPlugin as XLACheckpointIOPlugin
from nshtrainer.trainer.plugin.layer_sync import (
    TorchSyncBatchNormPlugin as TorchSyncBatchNormPlugin,
)
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
from nshtrainer.trainer.plugin.precision import (
    TransformerEnginePluginConfig as TransformerEnginePluginConfig,
)
from nshtrainer.trainer.plugin.precision import XLAPluginConfig as XLAPluginConfig

from . import base as base
from . import environment as environment
from . import io as io
from . import layer_sync as layer_sync
from . import precision as precision

__all__ = [
    "AsyncCheckpointIOPlugin",
    "BitsandbytesPluginConfig",
    "DTypeConfig",
    "DeepSpeedPluginConfig",
    "DoublePrecisionPluginConfig",
    "FSDPPrecisionPluginConfig",
    "HalfPrecisionPluginConfig",
    "KubeflowEnvironmentPlugin",
    "LSFEnvironmentPlugin",
    "LightningEnvironmentPlugin",
    "MPIEnvironmentPlugin",
    "MixedPrecisionPluginConfig",
    "PluginConfig",
    "PluginConfigBase",
    "SLURMEnvironmentPlugin",
    "TorchCheckpointIOPlugin",
    "TorchElasticEnvironmentPlugin",
    "TorchSyncBatchNormPlugin",
    "TransformerEnginePluginConfig",
    "XLACheckpointIOPlugin",
    "XLAEnvironmentPlugin",
    "XLAPluginConfig",
    "base",
    "environment",
    "io",
    "layer_sync",
    "plugin_registry",
    "precision",
]

from __future__ import annotations

__codegen__ = True

from nshtrainer.trainer.plugin.environment import DTypeConfig as DTypeConfig
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
from nshtrainer.trainer.plugin.environment import PluginConfigBase as PluginConfigBase
from nshtrainer.trainer.plugin.environment import (
    SLURMEnvironmentPlugin as SLURMEnvironmentPlugin,
)
from nshtrainer.trainer.plugin.environment import (
    TorchElasticEnvironmentPlugin as TorchElasticEnvironmentPlugin,
)
from nshtrainer.trainer.plugin.environment import (
    XLAEnvironmentPlugin as XLAEnvironmentPlugin,
)
from nshtrainer.trainer.plugin.environment import plugin_registry as plugin_registry

__all__ = [
    "DTypeConfig",
    "KubeflowEnvironmentPlugin",
    "LSFEnvironmentPlugin",
    "LightningEnvironmentPlugin",
    "MPIEnvironmentPlugin",
    "PluginConfigBase",
    "SLURMEnvironmentPlugin",
    "TorchElasticEnvironmentPlugin",
    "XLAEnvironmentPlugin",
    "plugin_registry",
]

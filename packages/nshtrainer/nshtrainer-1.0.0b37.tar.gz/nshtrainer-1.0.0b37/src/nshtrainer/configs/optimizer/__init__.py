from __future__ import annotations

__codegen__ = True

from nshtrainer.optimizer import AdamWConfig as AdamWConfig
from nshtrainer.optimizer import OptimizerConfig as OptimizerConfig
from nshtrainer.optimizer import OptimizerConfigBase as OptimizerConfigBase
from nshtrainer.optimizer import optimizer_registry as optimizer_registry

__all__ = [
    "AdamWConfig",
    "OptimizerConfig",
    "OptimizerConfigBase",
    "optimizer_registry",
]

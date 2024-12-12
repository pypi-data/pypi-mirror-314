from __future__ import annotations

__codegen__ = True

from nshtrainer.nn.mlp import MLPConfig as MLPConfig
from nshtrainer.nn.mlp import NonlinearityConfig as NonlinearityConfig
from nshtrainer.nn.mlp import NonlinearityConfigBase as NonlinearityConfigBase

__all__ = [
    "MLPConfig",
    "NonlinearityConfig",
    "NonlinearityConfigBase",
]

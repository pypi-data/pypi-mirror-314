from __future__ import annotations

__codegen__ = True

from nshtrainer.nn import ELUNonlinearityConfig as ELUNonlinearityConfig
from nshtrainer.nn import GELUNonlinearityConfig as GELUNonlinearityConfig
from nshtrainer.nn import LeakyReLUNonlinearityConfig as LeakyReLUNonlinearityConfig
from nshtrainer.nn import MishNonlinearityConfig as MishNonlinearityConfig
from nshtrainer.nn import MLPConfig as MLPConfig
from nshtrainer.nn import NonlinearityConfig as NonlinearityConfig
from nshtrainer.nn import NonlinearityConfigBase as NonlinearityConfigBase
from nshtrainer.nn import PReLUConfig as PReLUConfig
from nshtrainer.nn import ReLUNonlinearityConfig as ReLUNonlinearityConfig
from nshtrainer.nn import SigmoidNonlinearityConfig as SigmoidNonlinearityConfig
from nshtrainer.nn import SiLUNonlinearityConfig as SiLUNonlinearityConfig
from nshtrainer.nn import SoftmaxNonlinearityConfig as SoftmaxNonlinearityConfig
from nshtrainer.nn import SoftplusNonlinearityConfig as SoftplusNonlinearityConfig
from nshtrainer.nn import SoftsignNonlinearityConfig as SoftsignNonlinearityConfig
from nshtrainer.nn import SwishNonlinearityConfig as SwishNonlinearityConfig
from nshtrainer.nn import TanhNonlinearityConfig as TanhNonlinearityConfig
from nshtrainer.nn.nonlinearity import (
    SwiGLUNonlinearityConfig as SwiGLUNonlinearityConfig,
)
from nshtrainer.nn.nonlinearity import nonlinearity_registry as nonlinearity_registry

from . import mlp as mlp
from . import nonlinearity as nonlinearity

__all__ = [
    "ELUNonlinearityConfig",
    "GELUNonlinearityConfig",
    "LeakyReLUNonlinearityConfig",
    "MLPConfig",
    "MishNonlinearityConfig",
    "NonlinearityConfig",
    "NonlinearityConfigBase",
    "PReLUConfig",
    "ReLUNonlinearityConfig",
    "SiLUNonlinearityConfig",
    "SigmoidNonlinearityConfig",
    "SoftmaxNonlinearityConfig",
    "SoftplusNonlinearityConfig",
    "SoftsignNonlinearityConfig",
    "SwiGLUNonlinearityConfig",
    "SwishNonlinearityConfig",
    "TanhNonlinearityConfig",
    "mlp",
    "nonlinearity",
    "nonlinearity_registry",
]

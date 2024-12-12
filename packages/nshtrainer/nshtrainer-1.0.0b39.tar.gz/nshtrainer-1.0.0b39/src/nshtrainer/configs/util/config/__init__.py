from __future__ import annotations

__codegen__ = True

from nshtrainer.util.config import DTypeConfig as DTypeConfig
from nshtrainer.util.config import DurationConfig as DurationConfig
from nshtrainer.util.config import EpochsConfig as EpochsConfig
from nshtrainer.util.config import StepsConfig as StepsConfig

from . import dtype as dtype
from . import duration as duration

__all__ = [
    "DTypeConfig",
    "DurationConfig",
    "EpochsConfig",
    "StepsConfig",
    "dtype",
    "duration",
]

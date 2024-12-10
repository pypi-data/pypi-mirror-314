from __future__ import annotations

from typing import Annotated, TypeAlias

import nshconfig as C

from ._base import BaseProfilerConfig as BaseProfilerConfig
from .advanced import AdvancedProfilerConfig as AdvancedProfilerConfig
from .pytorch import PyTorchProfilerConfig as PyTorchProfilerConfig
from .simple import SimpleProfilerConfig as SimpleProfilerConfig

ProfilerConfig: TypeAlias = Annotated[
    SimpleProfilerConfig | AdvancedProfilerConfig | PyTorchProfilerConfig,
    C.Field(discriminator="name"),
]

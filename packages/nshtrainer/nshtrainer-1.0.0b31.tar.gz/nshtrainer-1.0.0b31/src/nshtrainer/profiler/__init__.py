from __future__ import annotations

from typing import Annotated

import nshconfig as C
from typing_extensions import TypeAliasType

from ._base import BaseProfilerConfig as BaseProfilerConfig
from .advanced import AdvancedProfilerConfig as AdvancedProfilerConfig
from .pytorch import PyTorchProfilerConfig as PyTorchProfilerConfig
from .simple import SimpleProfilerConfig as SimpleProfilerConfig

ProfilerConfig = TypeAliasType(
    "ProfilerConfig",
    Annotated[
        SimpleProfilerConfig | AdvancedProfilerConfig | PyTorchProfilerConfig,
        C.Field(discriminator="name"),
    ],
)

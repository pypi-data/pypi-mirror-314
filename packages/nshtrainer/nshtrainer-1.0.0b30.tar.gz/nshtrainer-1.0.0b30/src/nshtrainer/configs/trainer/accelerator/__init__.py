from __future__ import annotations

__codegen__ = True

from nshtrainer.trainer.accelerator import AcceleratorConfig as AcceleratorConfig
from nshtrainer.trainer.accelerator import (
    AcceleratorConfigBase as AcceleratorConfigBase,
)
from nshtrainer.trainer.accelerator import CPUAcceleratorConfig as CPUAcceleratorConfig
from nshtrainer.trainer.accelerator import (
    CUDAAcceleratorConfig as CUDAAcceleratorConfig,
)
from nshtrainer.trainer.accelerator import MPSAcceleratorConfig as MPSAcceleratorConfig
from nshtrainer.trainer.accelerator import XLAAcceleratorConfig as XLAAcceleratorConfig
from nshtrainer.trainer.accelerator import accelerator_registry as accelerator_registry

__all__ = [
    "AcceleratorConfig",
    "AcceleratorConfigBase",
    "CPUAcceleratorConfig",
    "CUDAAcceleratorConfig",
    "MPSAcceleratorConfig",
    "XLAAcceleratorConfig",
    "accelerator_registry",
]

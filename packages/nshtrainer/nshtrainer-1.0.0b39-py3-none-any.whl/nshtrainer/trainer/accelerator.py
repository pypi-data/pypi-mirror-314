from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Annotated, Literal

import nshconfig as C
from lightning.pytorch.accelerators import Accelerator
from typing_extensions import TypeAliasType, override

if TYPE_CHECKING:
    from ._config import TrainerConfig

AcceleratorLiteral = TypeAliasType(
    "AcceleratorLiteral", Literal["cpu", "gpu", "tpu", "ipu", "hpu", "mps", "auto"]
)


class AcceleratorConfigBase(C.Config, ABC):
    @abstractmethod
    def create_accelerator(self, trainer_config: "TrainerConfig") -> Accelerator: ...


accelerator_registry = C.Registry(AcceleratorConfigBase, discriminator="name")

AcceleratorConfig = TypeAliasType(
    "AcceleratorConfig",
    Annotated[AcceleratorConfigBase, accelerator_registry.DynamicResolution()],
)


@accelerator_registry.register
class CPUAcceleratorConfig(AcceleratorConfigBase):
    name: Literal["cpu"] = "cpu"

    """Accelerator for CPU devices."""

    @override
    def create_accelerator(self, trainer_config) -> Accelerator:
        from lightning.pytorch.accelerators.cpu import CPUAccelerator

        return CPUAccelerator()


@accelerator_registry.register
class CUDAAcceleratorConfig(AcceleratorConfigBase):
    name: Literal["gpu"] = "gpu"

    """Accelerator for NVIDIA CUDA devices."""

    @override
    def create_accelerator(self, trainer_config) -> Accelerator:
        from lightning.pytorch.accelerators.cuda import CUDAAccelerator

        return CUDAAccelerator()


@accelerator_registry.register
class MPSAcceleratorConfig(AcceleratorConfigBase):
    name: Literal["mps"] = "mps"

    """Accelerator for Metal Apple Silicon GPU devices.

    .. warning::  Use of this accelerator beyond import and instantiation is experimental.
    """

    @override
    def create_accelerator(self, trainer_config) -> Accelerator:
        from lightning.pytorch.accelerators.mps import MPSAccelerator

        return MPSAccelerator()


@accelerator_registry.register
class XLAAcceleratorConfig(AcceleratorConfigBase):
    name: Literal["tpu"] = "tpu"

    """Accelerator for XLA devices, normally TPUs.

    .. warning::  Use of this accelerator beyond import and instantiation is experimental.
    """

    @override
    def create_accelerator(self, trainer_config) -> Accelerator:
        from lightning.pytorch.accelerators.xla import XLAAccelerator

        return XLAAccelerator()

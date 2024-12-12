from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Annotated, Literal

import nshconfig as C
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing_extensions import TypeAliasType, final, override


class NonlinearityConfigBase(C.Config, ABC):
    @abstractmethod
    def create_module(self) -> nn.Module: ...

    @abstractmethod
    def __call__(self, x: torch.Tensor) -> torch.Tensor: ...


nonlinearity_registry = C.Registry(NonlinearityConfigBase, discriminator="name")


@final
@nonlinearity_registry.register
class ReLUNonlinearityConfig(NonlinearityConfigBase):
    name: Literal["relu"] = "relu"

    @override
    def create_module(self) -> nn.Module:
        return nn.ReLU()

    def __call__(self, x: torch.Tensor) -> torch.Tensor:
        return F.relu(x)


@final
@nonlinearity_registry.register
class SigmoidNonlinearityConfig(NonlinearityConfigBase):
    name: Literal["sigmoid"] = "sigmoid"

    @override
    def create_module(self) -> nn.Module:
        return nn.Sigmoid()

    def __call__(self, x: torch.Tensor) -> torch.Tensor:
        return torch.sigmoid(x)


@final
@nonlinearity_registry.register
class TanhNonlinearityConfig(NonlinearityConfigBase):
    name: Literal["tanh"] = "tanh"

    @override
    def create_module(self) -> nn.Module:
        return nn.Tanh()

    def __call__(self, x: torch.Tensor) -> torch.Tensor:
        return torch.tanh(x)


@final
@nonlinearity_registry.register
class SoftmaxNonlinearityConfig(NonlinearityConfigBase):
    name: Literal["softmax"] = "softmax"

    dim: int = -1
    """The dimension to apply the softmax function."""

    @override
    def create_module(self) -> nn.Module:
        return nn.Softmax(dim=self.dim)

    def __call__(self, x: torch.Tensor) -> torch.Tensor:
        return torch.softmax(x, dim=self.dim)


@final
@nonlinearity_registry.register
class SoftplusNonlinearityConfig(NonlinearityConfigBase):
    name: Literal["softplus"] = "softplus"

    beta: float = 1.0
    """The beta parameter in the softplus function."""

    threshold: float = 20.0
    """Values above this revert to a linear function."""

    @override
    def create_module(self) -> nn.Module:
        return nn.Softplus(beta=self.beta, threshold=self.threshold)

    def __call__(self, x: torch.Tensor) -> torch.Tensor:
        return F.softplus(x, beta=self.beta, threshold=self.threshold)


@final
@nonlinearity_registry.register
class SoftsignNonlinearityConfig(NonlinearityConfigBase):
    name: Literal["softsign"] = "softsign"

    @override
    def create_module(self) -> nn.Module:
        return nn.Softsign()

    def __call__(self, x: torch.Tensor) -> torch.Tensor:
        return F.softsign(x)


@final
@nonlinearity_registry.register
class ELUNonlinearityConfig(NonlinearityConfigBase):
    name: Literal["elu"] = "elu"

    alpha: float = 1.0
    """The alpha parameter in the ELU function."""

    @override
    def create_module(self) -> nn.Module:
        return nn.ELU()

    def __call__(self, x: torch.Tensor) -> torch.Tensor:
        return F.elu(x, alpha=self.alpha)


@final
@nonlinearity_registry.register
class LeakyReLUNonlinearityConfig(NonlinearityConfigBase):
    name: Literal["leaky_relu"] = "leaky_relu"

    negative_slope: float = 1.0e-2
    """The negative slope of the leaky ReLU function."""

    @override
    def create_module(self) -> nn.Module:
        return nn.LeakyReLU(negative_slope=self.negative_slope)

    def __call__(self, x: torch.Tensor) -> torch.Tensor:
        return F.leaky_relu(x, negative_slope=self.negative_slope)


@final
@nonlinearity_registry.register
class PReLUConfig(NonlinearityConfigBase):
    name: Literal["prelu"] = "prelu"

    num_parameters: int = 1
    """The number of :math:`a` to learn.
    Although it takes an int as input, there is only two values are legitimate:
    1, or the number of channels at input."""

    init: float = 0.25
    """The initial value of :math:`a`."""

    @override
    def create_module(self) -> nn.Module:
        return nn.PReLU(num_parameters=self.num_parameters, init=self.init)

    def __call__(self, x: torch.Tensor) -> torch.Tensor:
        raise NotImplementedError(
            "PReLU requires learnable parameters and cannot be called directly."
        )


@final
@nonlinearity_registry.register
class GELUNonlinearityConfig(NonlinearityConfigBase):
    name: Literal["gelu"] = "gelu"

    approximate: Literal["tanh", "none"] = "none"
    """The gelu approximation algorithm to use."""

    @override
    def create_module(self) -> nn.Module:
        return nn.GELU(approximate=self.approximate)

    def __call__(self, x: torch.Tensor) -> torch.Tensor:
        return F.gelu(x, approximate=self.approximate)


@final
@nonlinearity_registry.register
class SwishNonlinearityConfig(NonlinearityConfigBase):
    name: Literal["swish"] = "swish"

    @override
    def create_module(self) -> nn.Module:
        return nn.SiLU()

    def __call__(self, x: torch.Tensor) -> torch.Tensor:
        return F.silu(x)


@final
@nonlinearity_registry.register
class SiLUNonlinearityConfig(NonlinearityConfigBase):
    name: Literal["silu"] = "silu"

    @override
    def create_module(self) -> nn.Module:
        return nn.SiLU()

    def __call__(self, x: torch.Tensor) -> torch.Tensor:
        return F.silu(x)


@final
@nonlinearity_registry.register
class MishNonlinearityConfig(NonlinearityConfigBase):
    name: Literal["mish"] = "mish"

    @override
    def create_module(self) -> nn.Module:
        return nn.Mish()

    def __call__(self, x: torch.Tensor) -> torch.Tensor:
        return F.mish(x)


class SwiGLU(nn.SiLU):
    @override
    def forward(self, input: torch.Tensor):
        input, gate = input.chunk(2, dim=-1)
        return input * super().forward(gate)


@final
@nonlinearity_registry.register
class SwiGLUNonlinearityConfig(NonlinearityConfigBase):
    name: Literal["swiglu"] = "swiglu"

    @override
    def create_module(self) -> nn.Module:
        return SwiGLU()

    def __call__(self, x: torch.Tensor) -> torch.Tensor:
        input, gate = x.chunk(2, dim=-1)
        return input * F.silu(gate)


NonlinearityConfig = TypeAliasType(
    "NonlinearityConfig",
    Annotated[NonlinearityConfigBase, nonlinearity_registry.DynamicResolution()],
)

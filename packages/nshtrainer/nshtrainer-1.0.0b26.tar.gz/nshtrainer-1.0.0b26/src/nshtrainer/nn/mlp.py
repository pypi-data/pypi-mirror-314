from __future__ import annotations

import copy
from collections.abc import Callable, Sequence
from typing import Literal, Protocol, runtime_checkable

import nshconfig as C
import torch
import torch.nn as nn
from typing_extensions import TypedDict, override

from .nonlinearity import BaseNonlinearityConfig, NonlinearityConfig


@runtime_checkable
class LinearModuleConstructor(Protocol):
    def __call__(
        self, in_features: int, out_features: int, bias: bool = True
    ) -> nn.Module: ...


class ResidualSequential(nn.Sequential):
    @override
    def forward(self, input: torch.Tensor) -> torch.Tensor:
        return input + super().forward(input)


class MLPConfigDict(TypedDict):
    bias: bool
    """Whether to include bias terms in the linear layers."""

    no_bias_scalar: bool
    """Whether to exclude bias terms when the output dimension is 1."""

    nonlinearity: NonlinearityConfig | None
    """Activation function to use between layers."""

    ln: bool | Literal["pre", "post"]
    """Whether to apply layer normalization before or after the linear layers."""

    dropout: float | None
    """Dropout probability to apply between layers."""

    residual: bool
    """Whether to use residual connections between layers."""


class MLPConfig(C.Config):
    bias: bool = True
    """Whether to include bias terms in the linear layers."""

    no_bias_scalar: bool = True
    """Whether to exclude bias terms when the output dimension is 1."""

    nonlinearity: NonlinearityConfig | None = None
    """Activation function to use between layers."""

    ln: bool | Literal["pre", "post"] = False
    """Whether to apply layer normalization before or after the linear layers."""

    dropout: float | None = None
    """Dropout probability to apply between layers."""

    residual: bool = False
    """Whether to use residual connections between layers."""

    def to_kwargs(self) -> MLPConfigDict:
        return {
            "bias": self.bias,
            "no_bias_scalar": self.no_bias_scalar,
            "nonlinearity": self.nonlinearity,
            "ln": self.ln,
            "dropout": self.dropout,
            "residual": self.residual,
        }

    def create_module(
        self,
        dims: Sequence[int],
        pre_layers: Sequence[nn.Module] = [],
        post_layers: Sequence[nn.Module] = [],
        linear_cls: LinearModuleConstructor = nn.Linear,
    ):
        return MLP(
            dims,
            **self.to_kwargs(),
            pre_layers=pre_layers,
            post_layers=post_layers,
            linear_cls=linear_cls,
        )


def MLP(
    dims: Sequence[int],
    activation: BaseNonlinearityConfig
    | nn.Module
    | Callable[[], nn.Module]
    | None = None,
    nonlinearity: BaseNonlinearityConfig
    | nn.Module
    | Callable[[], nn.Module]
    | None = None,
    bias: bool = True,
    no_bias_scalar: bool = True,
    ln: bool | Literal["pre", "post"] = False,
    dropout: float | None = None,
    residual: bool = False,
    pre_layers: Sequence[nn.Module] = [],
    post_layers: Sequence[nn.Module] = [],
    linear_cls: LinearModuleConstructor = nn.Linear,
):
    """
    Constructs a multi-layer perceptron (MLP) with the given dimensions and activation function.

    Args:
        dims (Sequence[int]): List of integers representing the dimensions of the MLP.
        nonlinearity (Callable[[], nn.Module]): Activation function to use between layers.
        activation (Callable[[], nn.Module]): Activation function to use between layers.
        bias (bool, optional): Whether to include bias terms in the linear layers. Defaults to True.
        no_bias_scalar (bool, optional): Whether to exclude bias terms when the output dimension is 1. Defaults to True.
        ln (bool | Literal["pre", "post"], optional): Whether to apply layer normalization before or after the linear layers. Defaults to False.
        dropout (float | None, optional): Dropout probability to apply between layers. Defaults to None.
        residual (bool, optional): Whether to use residual connections between layers. Defaults to False.
        pre_layers (Sequence[nn.Module], optional): List of layers to insert before the linear layers. Defaults to [].
        post_layers (Sequence[nn.Module], optional): List of layers to insert after the linear layers. Defaults to [].

    Returns:
        nn.Sequential: The constructed MLP.
    """

    if activation is None:
        activation = nonlinearity

    if len(dims) < 2:
        raise ValueError("mlp requires at least 2 dimensions")
    if ln is True:
        ln = "pre"
    elif isinstance(ln, str) and ln not in ("pre", "post"):
        raise ValueError("ln must be a boolean or 'pre' or 'post'")

    layers: list[nn.Module] = []
    if ln == "pre":
        layers.append(nn.LayerNorm(dims[0]))

    layers.extend(pre_layers)

    for i in range(len(dims) - 1):
        in_features = dims[i]
        out_features = dims[i + 1]
        bias_ = bias and not (no_bias_scalar and out_features == 1)
        layers.append(linear_cls(in_features, out_features, bias=bias_))
        if dropout is not None:
            layers.append(nn.Dropout(dropout))
        if i < len(dims) - 2:
            match activation:
                case BaseNonlinearityConfig():
                    layers.append(activation.create_module())
                case nn.Module():
                    # In this case, we create a deep copy of the module to avoid sharing parameters (if any).
                    layers.append(copy.deepcopy(activation))
                case Callable():
                    layers.append(activation())
                case _:
                    raise ValueError(
                        "Either `nonlinearity` or `activation` must be provided"
                    )

    layers.extend(post_layers)

    if ln == "post":
        layers.append(nn.LayerNorm(dims[-1]))

    cls = ResidualSequential if residual else nn.Sequential
    return cls(*layers)

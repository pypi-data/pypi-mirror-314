from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import nshconfig as C
import torch
from typing_extensions import TypeAliasType, assert_never

from ..bf16 import is_bf16_supported_no_emulation

if TYPE_CHECKING:
    from ...trainer._config import TrainerConfig

DTypeName = TypeAliasType(
    "DTypeName",
    Literal[
        "float32",
        "float",
        "float64",
        "double",
        "float16",
        "bfloat16",
        "float8_e4m3fn",
        "float8_e4m3fnuz",
        "float8_e5m2",
        "float8_e5m2fnuz",
        "half",
        "uint8",
        "uint16",
        "uint32",
        "uint64",
        "int8",
        "int16",
        "short",
        "int32",
        "int",
        "int64",
        "long",
        "complex32",
        "complex64",
        "chalf",
        "cfloat",
        "complex128",
        "cdouble",
        "quint8",
        "qint8",
        "qint32",
        "bool",
        "quint4x2",
        "quint2x4",
        "bits1x8",
        "bits2x4",
        "bits4x2",
        "bits8",
        "bits16",
    ],
)


class DTypeConfig(C.Config):
    name: DTypeName
    """The name of the dtype."""

    @classmethod
    def from_trainer_config(cls, trainer_config: TrainerConfig):
        if (precision := trainer_config.precision) is None:
            precision = "32-true"

        match precision:
            case "16-mixed-auto":
                return (
                    cls(name="bfloat16")
                    if is_bf16_supported_no_emulation()
                    else cls(name="float16")
                )
            case "fp16-mixed":
                return cls(name="float16")
            case "bf16-mixed":
                return cls(name="bfloat16")
            case "32-true":
                return cls(name="float32")
            case "64-true":
                return cls(name="float64")
            case _:
                assert_never(trainer_config.precision)

    @property
    def torch_dtype(self):
        if ((dtype := getattr(torch, self.name, None)) is None) or not isinstance(
            dtype, torch.dtype
        ):
            raise ValueError(f"Unknown dtype {self.name}")

        return dtype

from __future__ import annotations

from typing import Any, Literal

from lightning.pytorch.plugins.precision import Precision
from typing_extensions import override

from ...util.config.dtype import DTypeConfig
from .base import PluginConfigBase, plugin_registry


@plugin_registry.register
class MixedPrecisionPluginConfig(PluginConfigBase):
    name: Literal["mixed_precision"] = "mixed_precision"

    precision: Literal["16-mixed", "bf16-mixed"]
    """Whether to use ``torch.float16`` (``'16-mixed'``) or ``torch.bfloat16`` (``'bf16-mixed'``)."""

    device: str
    """The device for ``torch.autocast``."""

    @override
    def create_plugin(self, trainer_config) -> Precision:
        from lightning.pytorch.plugins.precision.amp import MixedPrecision

        return MixedPrecision(self.precision, self.device)


@plugin_registry.register
class BitsandbytesPluginConfig(PluginConfigBase):
    name: Literal["bitsandbytes_precision"] = "bitsandbytes_precision"

    mode: Literal["nf4", "nf4-dq", "fp4", "fp4-dq", "int8", "int8-training"]
    """The quantization mode to use."""

    dtype: DTypeConfig | None = None
    """The compute dtype to use."""

    ignore_modules: set[str] | None = None
    """The submodules whose Linear layers should not be replaced.

    This might be desirable for numerical stability. The string will be checked
    as a prefix, so a value like "transformer.blocks" will ignore all linear
    layers in all of the transformer blocks.
    """

    @override
    def create_plugin(self, trainer_config) -> Precision:
        from lightning.pytorch.plugins.precision.bitsandbytes import (
            BitsandbytesPrecision,
        )

        return BitsandbytesPrecision(
            mode=self.mode,
            dtype=self.dtype.torch_dtype if self.dtype is not None else None,
            ignore_modules=self.ignore_modules,
        )


@plugin_registry.register
class DeepSpeedPluginConfig(PluginConfigBase):
    name: Literal["deepspeed_precision"] = "deepspeed_precision"

    precision: Literal["16-true", "bf16-true", "16-mixed", "bf16-mixed", "32-true"]
    """Full precision (32-true), half precision (16-true, bf16-true) or
    mixed precision (16-mixed, bf16-mixed)."""

    @override
    def create_plugin(self, trainer_config) -> Precision:
        from lightning.pytorch.plugins.precision.deepspeed import DeepSpeedPrecision

        return DeepSpeedPrecision(precision=self.precision)


@plugin_registry.register
class DoublePrecisionPluginConfig(PluginConfigBase):
    name: Literal["double_precision"] = "double_precision"

    precision: Literal["64-true"] = "64-true"
    """Plugin for training with double (``torch.float64``) precision."""

    @override
    def create_plugin(self, trainer_config) -> Precision:
        from lightning.pytorch.plugins.precision.double import DoublePrecision

        return DoublePrecision()


@plugin_registry.register
class FSDPPrecisionPluginConfig(PluginConfigBase):
    name: Literal["fsdp_precision"] = "fsdp_precision"

    precision: Literal["16-true", "bf16-true", "16-mixed", "bf16-mixed", "32-true"]
    """Full precision (32-true), half precision (16-true, bf16-true) or
    mixed precision (16-mixed, bf16-mixed)."""

    @override
    def create_plugin(self, trainer_config) -> Precision:
        from lightning.pytorch.plugins.precision.fsdp import FSDPPrecision

        return FSDPPrecision(precision=self.precision)


@plugin_registry.register
class HalfPrecisionPluginConfig(PluginConfigBase):
    name: Literal["half_precision"] = "half_precision"

    precision: Literal["bf16-true", "16-true"]
    """Whether to use ``torch.float16`` (``'16-true'``) or ``torch.bfloat16`` (``'bf16-true'``)."""

    @override
    def create_plugin(self, trainer_config) -> Precision:
        from lightning.pytorch.plugins.precision.half import HalfPrecision

        return HalfPrecision(precision=self.precision)


@plugin_registry.register
class TransformerEnginePluginConfig(PluginConfigBase):
    name: Literal["transformer_engine_precision"] = "transformer_engine_precision"

    weights_dtype: DTypeConfig
    """The weights dtype to use."""

    recipe: dict[str, Any] | None = None
    """Recipe for the DelayedScaling configuration in dict format."""

    replace_layers: bool | None = None
    """Whether to replace ``Linear`` and ``LayerNorm`` layers automatically with their
    Transformer Engine alternatives."""

    fallback_compute_dtype: DTypeConfig | None = None
    """The compute dtype to use for operations that don't support fp8 autocast.
    Defaults to the same as weights_dtype."""

    @override
    def create_plugin(self, trainer_config) -> Precision:
        from lightning.pytorch.plugins.precision.transformer_engine import (
            TransformerEnginePrecision,
        )

        return TransformerEnginePrecision(
            weights_dtype=self.weights_dtype.torch_dtype,
            recipe=self.recipe,
            replace_layers=self.replace_layers,
            fallback_compute_dtype=self.fallback_compute_dtype.torch_dtype
            if self.fallback_compute_dtype
            else None,
        )


@plugin_registry.register
class XLAPluginConfig(PluginConfigBase):
    name: Literal["xla_precision"] = "xla_precision"

    precision: Literal["32-true", "16-true", "bf16-true"]
    """Full precision (32-true) or half precision (16-true, bf16-true)."""

    @override
    def create_plugin(self, trainer_config) -> Precision:
        from lightning.pytorch.plugins.precision.xla import XLAPrecision

        return XLAPrecision(precision=self.precision)

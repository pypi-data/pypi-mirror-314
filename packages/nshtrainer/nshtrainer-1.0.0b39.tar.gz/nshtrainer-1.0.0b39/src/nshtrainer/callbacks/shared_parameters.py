from __future__ import annotations

import logging
from collections.abc import Iterable
from typing import Literal, Protocol, runtime_checkable

import torch.nn as nn
from lightning.pytorch import LightningModule, Trainer
from lightning.pytorch.callbacks import Callback
from typing_extensions import TypeAliasType, final, override

from .base import CallbackConfigBase, callback_registry

log = logging.getLogger(__name__)


@final
@callback_registry.register
class SharedParametersCallbackConfig(CallbackConfigBase):
    """A callback that allows scaling the gradients of shared parameters that
    are registered in the ``self.shared_parameters`` list of the root module.

    This is useful for models that share parameters across multiple modules and
    want to downscale the gradients of these parameters to avoid overfitting.
    """

    name: Literal["shared_parameters"] = "shared_parameters"

    @override
    def create_callbacks(self, trainer_config):
        yield SharedParametersCallback(self)


def _parameters_to_names(parameters: Iterable[nn.Parameter], model: nn.Module):
    mapping = {id(p): n for n, p in model.named_parameters()}
    return [mapping[id(p)] for p in parameters]


SharedParametersList = TypeAliasType(
    "SharedParametersList", list[tuple[nn.Parameter, int | float]]
)


@runtime_checkable
class ModuleWithSharedParameters(Protocol):
    @property
    def shared_parameters(self) -> SharedParametersList: ...


class SharedParametersCallback(Callback):
    @override
    def __init__(self, config: SharedParametersCallbackConfig):
        super().__init__()

        self.config = config
        del config

        self._warned_shared_parameters = False

    def _shared_parameters(self, pl_module: LightningModule) -> SharedParametersList:
        if not isinstance(pl_module, ModuleWithSharedParameters):
            return []

        return pl_module.shared_parameters

    @override
    def on_after_backward(self, trainer: Trainer, pl_module: LightningModule):
        if not (shared_parameters := self._shared_parameters(pl_module)):
            log.debug(
                "No shared parameters to scale, skipping SharedParametersCallback"
            )
            return

        log.debug(f"Scaling {len(shared_parameters)} shared parameters...")
        no_grad_parameters: list[nn.Parameter] = []
        for p, factor in shared_parameters:
            if not hasattr(p, "grad") or p.grad is None:
                no_grad_parameters.append(p)
                continue

            _ = p.grad.data.div_(factor)

        if no_grad_parameters and not self._warned_shared_parameters:
            no_grad_parameters_str = ", ".join(
                _parameters_to_names(no_grad_parameters, pl_module)
            )
            log.warning(
                "The following parameters were marked as shared, but had no gradients: "
                f"{no_grad_parameters_str}"
            )
            self._warned_shared_parameters = True

        log.debug(f"Done scaling shared parameters. (len={len(shared_parameters)})")

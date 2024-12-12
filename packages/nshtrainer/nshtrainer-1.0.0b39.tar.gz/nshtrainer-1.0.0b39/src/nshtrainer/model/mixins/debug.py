from __future__ import annotations

import logging
from typing import Any

import torch

log = logging.getLogger(__name__)


def _trainer(module: Any):
    if torch.jit.is_scripting():
        return None

    if hasattr(module, "_trainer"):
        trainer = module._trainer
    else:
        try:
            trainer = module.trainer
        except RuntimeError:
            return None

    from ...trainer import Trainer

    if not isinstance(trainer, Trainer):
        return None

    return trainer


class _DebugModuleMixin:
    @property
    def nshtrainer_or_none(self):
        return _trainer(self)

    @property
    def nshtrainer(self):
        if (trainer := _trainer(self)) is None:
            raise RuntimeError("Could not resolve trainer.")
        return trainer

    @property
    def debug(self) -> bool:
        if (trainer := _trainer(self)) is None:
            return False
        return trainer.debug

    @debug.setter
    def debug(self, value: bool):
        if (trainer := _trainer(self)) is None:
            return
        trainer.debug = value

    @torch.jit.unused
    def breakpoint(self, rank_zero_only: bool = True):
        if (
            not rank_zero_only
            or not torch.distributed.is_initialized()
            or torch.distributed.get_rank() == 0
        ):
            breakpoint()

        if rank_zero_only and torch.distributed.is_initialized():
            _ = torch.distributed.barrier()

    @torch.jit.unused
    def ensure_finite(
        self,
        tensor: torch.Tensor,
        name: str | None = None,
        throw: bool = False,
    ):
        name_parts: list[str] = ["Tensor"]
        if name is not None:
            name_parts.append(name)
        name = " ".join(name_parts)

        not_finite = ~torch.isfinite(tensor)
        if not_finite.any():
            msg = f"{name} has {not_finite.sum().item()}/{not_finite.numel()} non-finite values."
            if throw:
                raise RuntimeError(msg)
            else:
                log.warning(msg)
            return False
        return True

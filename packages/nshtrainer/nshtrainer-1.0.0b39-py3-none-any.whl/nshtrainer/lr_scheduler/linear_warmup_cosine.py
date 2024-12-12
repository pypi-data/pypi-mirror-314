from __future__ import annotations

import math
import warnings
from typing import Literal

from torch.optim import Optimizer
from torch.optim.lr_scheduler import LRScheduler
from typing_extensions import final, override

from ..util.config import DurationConfig
from .base import LRSchedulerConfigBase, LRSchedulerMetadata, lr_scheduler_registry


@final
@lr_scheduler_registry.register
class LinearWarmupCosineDecayLRSchedulerConfig(LRSchedulerConfigBase):
    name: Literal["linear_warmup_cosine_decay"] = "linear_warmup_cosine_decay"

    warmup_duration: DurationConfig
    r"""The duration for the linear warmup phase.
    The learning rate is linearly increased from `warmup_start_lr` to the initial learning rate over this duration."""

    max_duration: DurationConfig
    r"""The total duration.
    The learning rate is decayed to `min_lr` over this duration."""

    warmup_start_lr_factor: float = 0.0
    r"""The initial learning rate for the linear warmup phase, as a factor of the initial learning rate.
    The learning rate is linearly increased from this value to the initial learning rate over `warmup_epochs` epochs."""

    min_lr_factor: float = 0.0
    r"""The minimum learning rate, as a factor of the initial learning rate.
    The learning rate is decayed to this value over `max_epochs` epochs."""

    annealing: bool = False
    r"""Whether to restart the learning rate schedule after `max_epochs` epochs.
    If `False`, the learning rate will be decayed to `min_lr` over `max_epochs` epochs, and then the learning rate will be set to `min_lr` for all subsequent epochs.
    If `True`, the learning rate will be decayed to `min_lr` over `max_epochs` epochs, and then the learning rate will be increased back to the initial learning rate over `max_epochs` epochs, and so on (this is called a cosine annealing schedule)."""

    @override
    def metadata(self) -> LRSchedulerMetadata:
        return {
            "interval": "step",
        }

    @override
    def create_scheduler_impl(self, optimizer, lightning_module):
        num_steps_per_epoch = self.compute_num_steps_per_epoch(lightning_module)
        warmup_steps = self.warmup_duration.to_steps(num_steps_per_epoch).value
        max_steps = self.max_duration.to_steps(num_steps_per_epoch).value

        # Warmup and max steps should be at least 1.
        warmup_steps = max(warmup_steps, 1)
        max_steps = max(max_steps, 1)

        # Create the scheduler
        scheduler = LinearWarmupCosineAnnealingLR(
            optimizer=optimizer,
            warmup_epochs=warmup_steps,
            max_epochs=max_steps,
            warmup_start_lr_factor=self.warmup_start_lr_factor,
            eta_min_factor=self.min_lr_factor,
            should_restart=self.annealing,
        )
        return scheduler


class LinearWarmupCosineAnnealingLR(LRScheduler):
    _get_lr_called_within_step: bool

    def __init__(
        self,
        optimizer: Optimizer,
        warmup_epochs: int,
        max_epochs: int,
        warmup_start_lr_factor: float = 0.0,
        eta_min_factor: float = 0.0,
        last_epoch: int = -1,
        should_restart: bool = True,
    ) -> None:
        self.warmup_epochs = warmup_epochs
        self.max_epochs = max_epochs
        self.warmup_start_lr_factor = warmup_start_lr_factor
        self.eta_min_factor = eta_min_factor
        self.should_restart = should_restart

        super().__init__(optimizer, last_epoch)

    @override
    def get_lr(self) -> list[float]:
        if not self._get_lr_called_within_step:
            warnings.warn(
                "To get the last learning rate computed by the scheduler, "
                "please use `get_last_lr()`.",
                UserWarning,
            )

        if self.last_epoch == 0:
            return [self.warmup_start_lr_factor * base_lr for base_lr in self.base_lrs]
        if self.last_epoch < self.warmup_epochs:
            return [
                group["lr"]
                + (base_lr - self.warmup_start_lr_factor * base_lr)
                / (self.warmup_epochs - 1)
                for base_lr, group in zip(self.base_lrs, self.optimizer.param_groups)
            ]
        if self.last_epoch == self.warmup_epochs:
            return self.base_lrs

        if not self.should_restart and self.last_epoch >= self.max_epochs:
            return [self.eta_min_factor * base_lr for base_lr in self.base_lrs]

        if (self.last_epoch - 1 - self.max_epochs) % (
            2 * (self.max_epochs - self.warmup_epochs)
        ) == 0:
            return [
                group["lr"]
                + (base_lr - self.eta_min_factor * base_lr)
                * (1 - math.cos(math.pi / (self.max_epochs - self.warmup_epochs)))
                / 2
                for base_lr, group in zip(self.base_lrs, self.optimizer.param_groups)
            ]

        return [
            (
                1
                + math.cos(
                    math.pi
                    * (self.last_epoch - self.warmup_epochs)
                    / (self.max_epochs - self.warmup_epochs)
                )
            )
            / (
                1
                + math.cos(
                    math.pi
                    * (self.last_epoch - self.warmup_epochs - 1)
                    / (self.max_epochs - self.warmup_epochs)
                )
            )
            * (group["lr"] - self.eta_min_factor * base_lr)
            + self.eta_min_factor * base_lr
            for base_lr, group in zip(self.base_lrs, self.optimizer.param_groups)
        ]

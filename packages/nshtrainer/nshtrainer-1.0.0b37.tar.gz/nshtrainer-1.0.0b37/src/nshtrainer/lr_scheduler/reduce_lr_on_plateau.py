from __future__ import annotations

from typing import Literal

from lightning.pytorch.utilities.types import LRSchedulerConfigType
from torch.optim.lr_scheduler import ReduceLROnPlateau
from typing_extensions import final, override

from ..metrics._config import MetricConfig
from .base import LRSchedulerConfigBase, LRSchedulerMetadata, lr_scheduler_registry


@final
@lr_scheduler_registry.register
class ReduceLROnPlateauConfig(LRSchedulerConfigBase):
    """Reduce learning rate when a metric has stopped improving."""

    name: Literal["reduce_lr_on_plateau"] = "reduce_lr_on_plateau"

    metric: MetricConfig | None = None
    """Metric to monitor.
    If not provided, the primary metric of the runner will be used."""

    patience: int
    r"""Number of epochs with no improvement after which learning rate will be reduced."""

    factor: float
    r"""Factor by which the learning rate will be reduced. new_lr = lr * factor."""

    cooldown: int = 0
    r"""Number of epochs to wait before resuming normal operation after lr has been reduced."""

    min_lr: float | list[float] = 0.0
    r"""A scalar or a list of scalars. A lower bound on the learning rate of all param groups or each group respectively."""

    eps: float = 1.0e-8
    r"""Minimal decay applied to lr. If the difference between new and old lr is smaller than eps, the update is ignored."""

    threshold: float = 1.0e-4
    r"""Threshold for measuring the new optimum, to only focus on significant changes."""

    threshold_mode: Literal["rel", "abs"] = "rel"
    r"""One of `rel`, `abs`. In `rel` mode, dynamic_threshold = best * (1 + threshold) in 'max' mode or best * (1 - threshold) in `min` mode. In `abs` mode, dynamic_threshold = best + threshold in `max` mode or best - threshold in `min` mode. Default: 'rel'."""

    @override
    def create_scheduler_impl(
        self, optimizer, lightning_module
    ) -> LRSchedulerConfigType:
        if (metric := self.metric) is None:
            from ..trainer import Trainer

            assert isinstance(
                trainer := lightning_module.trainer, Trainer
            ), "The trainer must be a `nshtrainer.Trainer` instance."

            assert (
                metric := trainer.hparams.primary_metric
            ) is not None, "Primary metric must be provided if metric is not specified."

        lr_scheduler = ReduceLROnPlateau(
            optimizer,
            mode=metric.mode,
            factor=self.factor,
            patience=self.patience,
            threshold=self.threshold,
            threshold_mode=self.threshold_mode,
            cooldown=self.cooldown,
            min_lr=self.min_lr,
            eps=self.eps,
        )
        return {
            "scheduler": lr_scheduler,
            "monitor": metric.validation_monitor,
        }

    @override
    def metadata(self) -> LRSchedulerMetadata:
        return {
            "interval": "epoch",
        }

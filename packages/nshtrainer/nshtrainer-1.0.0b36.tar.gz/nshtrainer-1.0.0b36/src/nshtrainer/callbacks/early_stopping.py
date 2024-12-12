from __future__ import annotations

import logging
import math
from typing import Literal

from lightning.fabric.utilities.rank_zero import _get_rank
from lightning.pytorch import Trainer
from lightning.pytorch.callbacks import EarlyStopping as _EarlyStopping
from lightning.pytorch.utilities.rank_zero import rank_prefixed_message
from typing_extensions import final, override

from ..metrics._config import MetricConfig
from .base import CallbackConfigBase, callback_registry

log = logging.getLogger(__name__)


@final
@callback_registry.register
class EarlyStoppingCallbackConfig(CallbackConfigBase):
    name: Literal["early_stopping"] = "early_stopping"

    metric: MetricConfig | None = None
    """
    The metric to monitor for early stopping.
    If None, the primary metric will be used.
    """

    patience: int
    """
    Number of epochs with no improvement after which training will be stopped.
    """

    min_delta: float = 1.0e-8
    """
    Minimum change in the monitored quantity to qualify as an improvement.
    """

    min_lr: float | None = None
    """
    Minimum learning rate. If the learning rate of the model is less than this value,
    the training will be stopped.
    """

    strict: bool = True
    """
    Whether to enforce that the monitored quantity must improve by at least `min_delta`
    to qualify as an improvement.
    """

    @override
    def create_callbacks(self, trainer_config):
        if (metric := self.metric) is None and (
            metric := trainer_config.primary_metric
        ) is None:
            raise ValueError(
                "Either `metric` or `trainer_config.primary_metric` must be set to use EarlyStopping."
            )

        yield EarlyStoppingCallback(self, metric)


class EarlyStoppingCallback(_EarlyStopping):
    def __init__(self, config: EarlyStoppingCallbackConfig, metric: MetricConfig):
        self.config = config
        self.metric = metric
        del config, metric

        super().__init__(
            monitor=self.metric.validation_monitor,
            mode=self.metric.mode,
            patience=self.config.patience,
            min_delta=self.config.min_delta,
            strict=self.config.strict,
        )

    @override
    @staticmethod
    def _log_info(trainer: Trainer | None, message: str, log_rank_zero_only: bool):
        rank = _get_rank()
        if trainer is not None and trainer.world_size <= 1:
            rank = None
        message = rank_prefixed_message(message, rank)
        if rank is None or not log_rank_zero_only or rank == 0:
            log.critical(message)

    @override
    def _run_early_stopping_check(self, trainer: Trainer):
        """Checks whether the early stopping condition is met and if so tells the trainer to stop the training."""
        logs = trainer.callback_metrics

        # Disable early_stopping with fast_dev_run
        if getattr(trainer, "fast_dev_run", False):
            return

        should_stop, reason = False, None

        if not should_stop:
            should_stop, reason = self._evaluate_stopping_criteria_min_lr(trainer)

        # If metric present
        if not should_stop and self._validate_condition_metric(logs):
            current = logs[self.monitor].squeeze()
            should_stop, reason = self._evaluate_stopping_criteria(current)

        # stop every ddp process if any world process decides to stop
        should_stop = trainer.strategy.reduce_boolean_decision(should_stop, all=False)
        trainer.should_stop = trainer.should_stop or should_stop
        if should_stop:
            self.stopped_epoch = trainer.current_epoch
        if reason and self.verbose:
            self._log_info(trainer, reason, self.log_rank_zero_only)

    def _evaluate_stopping_criteria_min_lr(
        self, trainer: Trainer
    ) -> tuple[bool, str | None]:
        if self.config.min_lr is None:
            return False, None

        # Get the maximum LR across all param groups in all optimizers
        model_max_lr = max(
            [
                param_group["lr"]
                for optimizer in trainer.optimizers
                for param_group in optimizer.param_groups
            ]
        )
        if not isinstance(model_max_lr, float) or not math.isfinite(model_max_lr):
            return False, None

        # If the maximum LR is less than the minimum LR, stop training
        if model_max_lr >= self.config.min_lr:
            return False, None

        return True, (
            "Stopping threshold reached: "
            f"The maximum LR of the model across all param groups is {model_max_lr:.2e} "
            f"which is less than the minimum LR {self.config.min_lr:.2e}"
        )

    def on_early_stopping(self, trainer: Trainer):
        pass

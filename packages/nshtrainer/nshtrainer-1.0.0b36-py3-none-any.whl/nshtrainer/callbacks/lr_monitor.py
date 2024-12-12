from __future__ import annotations

from typing import Literal

from lightning.pytorch.callbacks import LearningRateMonitor
from typing_extensions import final

from .base import CallbackConfigBase, callback_registry


@final
@callback_registry.register
class LearningRateMonitorConfig(CallbackConfigBase):
    name: Literal["learning_rate_monitor"] = "learning_rate_monitor"

    logging_interval: Literal["step", "epoch"] | None = None
    """
    Set to 'epoch' or 'step' to log 'lr' of all optimizers at the same interval, set to None to log at individual interval according to the 'interval' key of each scheduler. Defaults to None.
    """

    log_momentum: bool = False
    """
    Option to also log the momentum values of the optimizer, if the optimizer has the 'momentum' or 'betas' attribute. Defaults to False.
    """

    log_weight_decay: bool = False
    """
    Option to also log the weight decay values of the optimizer. Defaults to False.
    """

    def create_callbacks(self, trainer_config):
        yield LearningRateMonitor(
            logging_interval=self.logging_interval,
            log_momentum=self.log_momentum,
            log_weight_decay=self.log_weight_decay,
        )

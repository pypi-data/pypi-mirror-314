from __future__ import annotations

import logging
from typing import Literal

from typing_extensions import final, override

from .._callback import NTCallbackBase
from .base import CallbackConfigBase, callback_registry

log = logging.getLogger(__name__)


@final
@callback_registry.register
class DebugFlagCallbackConfig(CallbackConfigBase):
    name: Literal["debug_flag"] = "debug_flag"

    enabled: bool = True
    """Whether to enable the callback."""

    def __bool__(self):
        return self.enabled

    @override
    def create_callbacks(self, trainer_config):
        if not self:
            return

        yield DebugFlagCallback(self)


class DebugFlagCallback(NTCallbackBase):
    """
    Sets the debug flag to true in the following circumstances:
    - fast_dev_run is enabled
    - sanity check is running
    """

    @override
    def __init__(self, config: DebugFlagCallbackConfig):
        super().__init__()

        self.config = config
        del config

        self._debug = False

    @override
    def setup(self, trainer, pl_module, stage):
        if not getattr(trainer, "fast_dev_run", False):
            return

        if not trainer.debug:
            log.critical("Fast dev run detected, setting debug flag to True.")
        trainer.debug = True

    @override
    def on_sanity_check_start(self, trainer, pl_module):
        self._debug = trainer.debug
        if not self._debug:
            log.critical("Enabling debug flag during sanity check routine.")
        trainer.debug = True

    @override
    def on_sanity_check_end(self, trainer, pl_module):
        if not self._debug:
            log.critical("Sanity check routine complete, disabling debug flag.")
        trainer.debug = self._debug

from __future__ import annotations

__codegen__ = True

from nshtrainer.callbacks.print_table import CallbackConfigBase as CallbackConfigBase
from nshtrainer.callbacks.print_table import (
    PrintTableMetricsCallbackConfig as PrintTableMetricsCallbackConfig,
)
from nshtrainer.callbacks.print_table import callback_registry as callback_registry

__all__ = [
    "CallbackConfigBase",
    "PrintTableMetricsCallbackConfig",
    "callback_registry",
]

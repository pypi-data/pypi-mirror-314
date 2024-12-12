from __future__ import annotations

from ..callbacks import callback_registry as callback_registry
from ._config import TrainerConfig as TrainerConfig
from .accelerator import accelerator_registry as accelerator_registry
from .plugin import plugin_registry as plugin_registry
from .trainer import Trainer as Trainer

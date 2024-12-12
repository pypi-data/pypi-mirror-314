from __future__ import annotations

import contextlib
from pathlib import Path
from typing import Literal

from typing_extensions import TypeAliasType, final, override

from .._callback import NTCallbackBase
from .base import CallbackConfigBase, callback_registry

Stage = TypeAliasType("Stage", Literal["train", "validation", "test", "predict"])


@final
@callback_registry.register
class ActSaveConfig(CallbackConfigBase):
    name: Literal["act_save"] = "act_save"

    enabled: bool = True
    """Enable activation saving."""

    save_dir: Path | None = None
    """Directory to save activations to. If None, will use the activation directory set in `config.directory`."""

    def __bool__(self):
        return self.enabled

    @override
    def create_callbacks(self, trainer_config):
        yield ActSaveCallback(
            self,
            self.save_dir
            or trainer_config.directory.resolve_subdirectory(
                trainer_config.id, "activation"
            ),
        )


class ActSaveCallback(NTCallbackBase):
    def __init__(self, config: ActSaveConfig, save_dir: Path):
        super().__init__()

        self.config = config
        self.save_dir = save_dir
        self._enabled_context: contextlib._GeneratorContextManager | None = None
        self._active_contexts: dict[Stage, contextlib._GeneratorContextManager] = {}

    @override
    def setup(self, trainer, pl_module, stage) -> None:
        super().setup(trainer, pl_module, stage)

        if not self.config:
            return

        from nshutils import ActSave

        context = ActSave.enabled(self.save_dir)
        context.__enter__()
        self._enabled_context = context

    @override
    def teardown(self, trainer, pl_module, stage) -> None:
        super().teardown(trainer, pl_module, stage)

        if not self.config:
            return

        if self._enabled_context is not None:
            self._enabled_context.__exit__(None, None, None)
            self._enabled_context = None

    def _on_start(self, stage: Stage, trainer, pl_module):
        if not self.config:
            return

        from nshutils import ActSave

        # If we have an active context manager for this stage, exit it
        if active_contexts := self._active_contexts.get(stage):
            active_contexts.__exit__(None, None, None)

        # Enter a new context manager for this stage
        context = ActSave.context(stage)
        context.__enter__()
        self._active_contexts[stage] = context

    def _on_end(self, stage: Stage, trainer, pl_module):
        if not self.config:
            return

        # If we have an active context manager for this stage, exit it
        if (active_contexts := self._active_contexts.pop(stage, None)) is not None:
            active_contexts.__exit__(None, None, None)

    @override
    def on_train_epoch_start(self, trainer, pl_module):
        return self._on_start("train", trainer, pl_module)

    @override
    def on_train_epoch_end(self, trainer, pl_module):
        return self._on_end("train", trainer, pl_module)

    @override
    def on_validation_epoch_start(self, trainer, pl_module):
        return self._on_start("validation", trainer, pl_module)

    @override
    def on_validation_epoch_end(self, trainer, pl_module):
        return self._on_end("validation", trainer, pl_module)

    @override
    def on_test_epoch_start(self, trainer, pl_module):
        return self._on_start("test", trainer, pl_module)

    @override
    def on_test_epoch_end(self, trainer, pl_module):
        return self._on_end("test", trainer, pl_module)

    @override
    def on_predict_epoch_start(self, trainer, pl_module):
        return self._on_start("predict", trainer, pl_module)

    @override
    def on_predict_epoch_end(self, trainer, pl_module):
        return self._on_end("predict", trainer, pl_module)

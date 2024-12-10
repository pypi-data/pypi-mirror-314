from __future__ import annotations

import logging
from collections.abc import Callable, Iterable, Sequence
from typing import Any, cast

from lightning.pytorch import Callback, LightningModule
from typing_extensions import TypeAliasType, override

from ..._callback import NTCallbackBase
from ...util.typing_utils import mixin_base_type

log = logging.getLogger(__name__)

_Callback = TypeAliasType("_Callback", Callback | NTCallbackBase)
CallbackFn = TypeAliasType(
    "CallbackFn", Callable[[], _Callback | Iterable[_Callback] | None]
)


class CallbackRegistrarModuleMixin:
    @property
    def _nshtrainer_callbacks(self) -> list[CallbackFn]:
        if not hasattr(self, "_private_nshtrainer_callbacks_list"):
            self._private_nshtrainer_callbacks_list = []
        return self._private_nshtrainer_callbacks_list

    def register_callback(
        self,
        callback: _Callback | Iterable[_Callback] | CallbackFn | None = None,
    ):
        if not callable(callback):
            callback_ = cast(CallbackFn, lambda: callback)
        else:
            callback_ = callback

        self._nshtrainer_callbacks.append(callback_)


class CallbackModuleMixin(
    CallbackRegistrarModuleMixin,
    mixin_base_type(LightningModule),
):
    @property
    def _nshtrainer_callbacks(self) -> list[CallbackFn]:
        if not hasattr(self, "_private_nshtrainer_callbacks_list"):
            self._private_nshtrainer_callbacks_list = []
        return self._private_nshtrainer_callbacks_list

    def register_callback(
        self,
        callback: _Callback | Iterable[_Callback] | CallbackFn | None = None,
    ):
        if not callable(callback):
            callback_ = cast(CallbackFn, lambda: callback)
        else:
            callback_ = callback

        self._nshtrainer_callbacks.append(callback_)

    def _gather_all_callbacks(self):
        modules: list[Any] = []
        if isinstance(self, CallbackRegistrarModuleMixin):
            modules.append(self)
        if (
            datamodule := getattr(self.trainer, "datamodule", None)
        ) is not None and isinstance(datamodule, CallbackRegistrarModuleMixin):
            modules.append(datamodule)
        modules.extend(
            module
            for module in self.children()
            if isinstance(module, CallbackRegistrarModuleMixin)
        )
        for module in modules:
            yield from module._nshtrainer_callbacks

    @override
    def configure_callbacks(self):
        callbacks = super().configure_callbacks()
        if not isinstance(callbacks, Sequence):
            callbacks = [callbacks]

        callbacks = list(callbacks)
        for callback_fn in self._gather_all_callbacks():
            if (callback_result := callback_fn()) is None:
                continue

            if not isinstance(callback_result, Iterable):
                callback_result = [callback_result]

            for callback in callback_result:
                log.info(
                    f"Registering {callback.__class__.__qualname__} callback {callback}"
                )
                callbacks.append(callback)

        return callbacks

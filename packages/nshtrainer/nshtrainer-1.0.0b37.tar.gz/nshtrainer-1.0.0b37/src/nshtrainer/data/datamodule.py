from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any, Generic, cast

import nshconfig as C
import torch
from lightning.pytorch import LightningDataModule
from typing_extensions import Never, TypeVar, deprecated, override

from ..model.mixins.callback import CallbackRegistrarModuleMixin
from ..model.mixins.debug import _DebugModuleMixin

THparams = TypeVar("THparams", bound=C.Config, infer_variance=True)


class LightningDataModuleBase(
    _DebugModuleMixin,
    CallbackRegistrarModuleMixin,
    LightningDataModule,
    ABC,
    Generic[THparams],
):
    @property
    @override
    def hparams(self) -> THparams:  # pyright: ignore[reportIncompatibleMethodOverride]
        return cast(THparams, super().hparams)

    @property
    @override
    def hparams_initial(self):  # pyright: ignore[reportIncompatibleMethodOverride]
        hparams = cast(THparams, super().hparams_initial)
        return cast(Never, {"datamodule": hparams.model_dump(mode="json")})

    @property
    @deprecated("Use `hparams` instead")
    def config(self):
        return cast(Never, self.hparams)

    @classmethod
    @abstractmethod
    def hparams_cls(cls) -> type[THparams]: ...

    @override
    def __init__(self, hparams: THparams | Mapping[str, Any]):
        super().__init__()

        # Validate and save hyperparameters
        hparams_cls = self.hparams_cls()
        if isinstance(hparams, Mapping):
            hparams = hparams_cls.model_validate(hparams)
        elif not isinstance(hparams, hparams_cls):
            raise TypeError(
                f"Expected hparams to be either a Mapping or an instance of {hparams_cls}, got {type(hparams)}"
            )
        hparams = hparams.model_deep_validate()
        self.save_hyperparameters(hparams)

    @override
    @classmethod
    def load_from_checkpoint(cls, *args, **kwargs) -> Never:
        raise ValueError("This method is not supported. Use `from_checkpoint` instead.")

    @classmethod
    def hparams_from_checkpoint(
        cls,
        ckpt_or_path: dict[str, Any] | str | Path,
        /,
        strict: bool | None = None,
        *,
        update_hparams: Callable[[THparams], THparams] | None = None,
        update_hparams_dict: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
    ):
        if isinstance(ckpt_or_path, dict):
            ckpt = ckpt_or_path
        else:
            ckpt = torch.load(ckpt_or_path, map_location="cpu")

        if (hparams := ckpt.get(cls.CHECKPOINT_HYPER_PARAMS_KEY)) is None:
            raise ValueError(
                f"The checkpoint does not contain hyperparameters. It must contain the key '{cls.CHECKPOINT_HYPER_PARAMS_KEY}'."
            )
        if update_hparams_dict is not None:
            hparams = update_hparams_dict(hparams)

        hparams = cls.hparams_cls().model_validate(hparams, strict=strict)
        if update_hparams is not None:
            hparams = update_hparams(hparams)

        return hparams

    @classmethod
    def from_checkpoint(
        cls,
        ckpt_or_path: dict[str, Any] | str | Path,
        /,
        strict: bool | None = None,
        map_location: torch.serialization.MAP_LOCATION = None,
        *,
        update_hparams: Callable[[THparams], THparams] | None = None,
        update_hparams_dict: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
    ):
        # Load checkpoint
        if isinstance(ckpt_or_path, Mapping):
            ckpt = ckpt_or_path
        else:
            ckpt = torch.load(ckpt_or_path, map_location=map_location)

        # Load hyperparameters from checkpoint
        hparams = cls.hparams_from_checkpoint(
            ckpt,
            strict=strict,
            update_hparams=update_hparams,
            update_hparams_dict=update_hparams_dict,
        )

        # Load datamodule from checkpoint
        datamodule = cls(hparams)
        if datamodule.__class__.__qualname__ in ckpt:
            datamodule.load_state_dict(ckpt[datamodule.__class__.__qualname__])

        return datamodule

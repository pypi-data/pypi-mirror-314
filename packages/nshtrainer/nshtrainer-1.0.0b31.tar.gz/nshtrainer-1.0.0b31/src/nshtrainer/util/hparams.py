from __future__ import annotations

import nshconfig as C
from lightning.pytorch.core.mixins.hparams_mixin import (
    HyperparametersMixin as _LightningHyperparametersMixin,
)
from typing_extensions import override


class HyperparamsMixin(_LightningHyperparametersMixin):
    @override
    def _set_hparams(self, hp):
        if isinstance(hp, C.Config):
            self._hparams = hp
            return

        return super()._set_hparams(hp)

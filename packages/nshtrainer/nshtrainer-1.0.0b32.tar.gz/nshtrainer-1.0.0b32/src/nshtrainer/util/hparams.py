from __future__ import annotations

from typing import TYPE_CHECKING

import nshconfig as C
from lightning.pytorch.core.mixins.hparams_mixin import (
    HyperparametersMixin as _LightningHyperparametersMixin,
)


class HyperparamsMixin(_LightningHyperparametersMixin):
    if not TYPE_CHECKING:

        def _to_hparams_dict(self, hp):
            if isinstance(hp, C.Config):
                return hp.model_dump(mode="python")

            return super()._set_hparams(hp)

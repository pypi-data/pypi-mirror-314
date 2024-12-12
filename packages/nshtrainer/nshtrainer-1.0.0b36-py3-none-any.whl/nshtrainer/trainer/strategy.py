from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Literal

import nshconfig as C
from lightning.pytorch.strategies.strategy import Strategy
from typing_extensions import TypeAliasType

if TYPE_CHECKING:
    from ._config import TrainerConfig

StrategyLiteral = TypeAliasType(
    "StrategyLiteral",
    Literal[
        "auto",
        "ddp",
        "ddp_find_unused_parameters_false",
        "ddp_find_unused_parameters_true",
        "ddp_spawn",
        "ddp_spawn_find_unused_parameters_false",
        "ddp_spawn_find_unused_parameters_true",
        "ddp_fork",
        "ddp_fork_find_unused_parameters_false",
        "ddp_fork_find_unused_parameters_true",
        "ddp_notebook",
        "dp",
        "deepspeed",
        "deepspeed_stage_1",
        "deepspeed_stage_1_offload",
        "deepspeed_stage_2",
        "deepspeed_stage_2_offload",
        "deepspeed_stage_3",
        "deepspeed_stage_3_offload",
        "deepspeed_stage_3_offload_nvme",
        "fsdp",
        "fsdp_cpu_offload",
        "single_xla",
        "xla_fsdp",
        "xla",
        "single_tpu",
    ],
)


class StrategyConfigBase(C.Config, ABC):
    @abstractmethod
    def create_strategy(self, trainer_config: "TrainerConfig") -> Strategy: ...


StrategyConfig = TypeAliasType("StrategyConfig", StrategyConfigBase)

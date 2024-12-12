from __future__ import annotations

from typing import Annotated

from typing_extensions import TypeAliasType

from . import checkpoint as checkpoint
from .actsave import ActSaveCallback as ActSaveCallback
from .actsave import ActSaveConfig as ActSaveConfig
from .base import CallbackConfigBase as CallbackConfigBase
from .base import callback_registry as callback_registry
from .checkpoint import BestCheckpointCallback as BestCheckpointCallback
from .checkpoint import BestCheckpointCallbackConfig as BestCheckpointCallbackConfig
from .checkpoint import LastCheckpointCallback as LastCheckpointCallback
from .checkpoint import LastCheckpointCallbackConfig as LastCheckpointCallbackConfig
from .checkpoint import OnExceptionCheckpointCallback as OnExceptionCheckpointCallback
from .checkpoint import (
    OnExceptionCheckpointCallbackConfig as OnExceptionCheckpointCallbackConfig,
)
from .debug_flag import DebugFlagCallback as DebugFlagCallback
from .debug_flag import DebugFlagCallbackConfig as DebugFlagCallbackConfig
from .directory_setup import DirectorySetupCallback as DirectorySetupCallback
from .directory_setup import (
    DirectorySetupCallbackConfig as DirectorySetupCallbackConfig,
)
from .early_stopping import EarlyStoppingCallback as EarlyStoppingCallback
from .early_stopping import EarlyStoppingCallbackConfig as EarlyStoppingCallbackConfig
from .ema import EMACallback as EMACallback
from .ema import EMACallbackConfig as EMACallbackConfig
from .finite_checks import FiniteChecksCallback as FiniteChecksCallback
from .finite_checks import FiniteChecksCallbackConfig as FiniteChecksCallbackConfig
from .gradient_skipping import GradientSkippingCallback as GradientSkippingCallback
from .gradient_skipping import (
    GradientSkippingCallbackConfig as GradientSkippingCallbackConfig,
)
from .interval import EpochIntervalCallback as EpochIntervalCallback
from .interval import IntervalCallback as IntervalCallback
from .interval import StepIntervalCallback as StepIntervalCallback
from .log_epoch import LogEpochCallback as LogEpochCallback
from .log_epoch import LogEpochCallbackConfig as LogEpochCallbackConfig
from .lr_monitor import LearningRateMonitor as LearningRateMonitor
from .lr_monitor import LearningRateMonitorConfig as LearningRateMonitorConfig
from .norm_logging import NormLoggingCallback as NormLoggingCallback
from .norm_logging import NormLoggingCallbackConfig as NormLoggingCallbackConfig
from .print_table import PrintTableMetricsCallback as PrintTableMetricsCallback
from .print_table import (
    PrintTableMetricsCallbackConfig as PrintTableMetricsCallbackConfig,
)
from .rlp_sanity_checks import RLPSanityChecksCallback as RLPSanityChecksCallback
from .rlp_sanity_checks import (
    RLPSanityChecksCallbackConfig as RLPSanityChecksCallbackConfig,
)
from .shared_parameters import SharedParametersCallback as SharedParametersCallback
from .shared_parameters import (
    SharedParametersCallbackConfig as SharedParametersCallbackConfig,
)
from .timer import EpochTimerCallback as EpochTimerCallback
from .timer import EpochTimerCallbackConfig as EpochTimerCallbackConfig
from .wandb_upload_code import WandbUploadCodeCallback as WandbUploadCodeCallback
from .wandb_upload_code import (
    WandbUploadCodeCallbackConfig as WandbUploadCodeCallbackConfig,
)
from .wandb_watch import WandbWatchCallback as WandbWatchCallback
from .wandb_watch import WandbWatchCallbackConfig as WandbWatchCallbackConfig

CallbackConfig = TypeAliasType(
    "CallbackConfig",
    Annotated[CallbackConfigBase, callback_registry.DynamicResolution()],
)

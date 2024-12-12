from __future__ import annotations

import datetime
import logging
import time
from dataclasses import dataclass
from typing import Any, Literal

from lightning.pytorch.callbacks.callback import Callback
from typing_extensions import TypeAliasType, override

log = logging.getLogger(__name__)

Stage = TypeAliasType("Stage", Literal["train", "validate", "test", "predict"])
ALL_STAGES = ("train", "validate", "test", "predict")


@dataclass
class TimeInfo:
    datetime: datetime.datetime
    monotonic: float


class RuntimeTrackerCallback(Callback):
    def __init__(self):
        super().__init__()
        self._start_time: dict[Stage, TimeInfo] = {}
        self._end_time: dict[Stage, TimeInfo] = {}
        self._offsets = {stage: datetime.timedelta() for stage in ALL_STAGES}

    def start_time(self, stage: Stage) -> TimeInfo | None:
        """Return the start time of a particular stage"""
        return self._start_time.get(stage)

    def end_time(self, stage: Stage) -> TimeInfo | None:
        """Return the end time of a particular stage"""
        return self._end_time.get(stage)

    def time_elapsed(self, stage: Stage) -> datetime.timedelta:
        """Return the time elapsed for a particular stage"""
        start = self.start_time(stage)
        end = self.end_time(stage)
        offset = self._offsets[stage]
        if start is None:
            return offset
        if end is None:
            current = TimeInfo(datetime.datetime.now(), time.monotonic())
            return (
                datetime.timedelta(seconds=current.monotonic - start.monotonic) + offset
            )
        return datetime.timedelta(seconds=end.monotonic - start.monotonic) + offset

    def _record_time(self, stage: Stage, time_dict: dict[Stage, TimeInfo]):
        time_dict[stage] = TimeInfo(datetime.datetime.now(), time.monotonic())

    @override
    def on_train_start(self, trainer, pl_module):
        self._record_time("train", self._start_time)

    @override
    def on_train_end(self, trainer, pl_module):
        self._record_time("train", self._end_time)

    @override
    def on_validation_start(self, trainer, pl_module):
        self._record_time("validate", self._start_time)

    @override
    def on_validation_end(self, trainer, pl_module):
        self._record_time("validate", self._end_time)

    @override
    def on_test_start(self, trainer, pl_module):
        self._record_time("test", self._start_time)

    @override
    def on_test_end(self, trainer, pl_module):
        self._record_time("test", self._end_time)

    @override
    def on_predict_start(self, trainer, pl_module):
        self._record_time("predict", self._start_time)

    @override
    def on_predict_end(self, trainer, pl_module):
        self._record_time("predict", self._end_time)

    @override
    def state_dict(self) -> dict[str, Any]:
        return {
            "time_elapsed": {
                stage: self.time_elapsed(stage).total_seconds() for stage in ALL_STAGES
            },
            "start_times": {
                stage: (info.datetime.isoformat(), info.monotonic)
                for stage, info in self._start_time.items()
            },
            "end_times": {
                stage: (info.datetime.isoformat(), info.monotonic)
                for stage, info in self._end_time.items()
            },
        }

    @override
    def load_state_dict(self, state_dict: dict[str, Any]):
        time_elapsed: dict[Stage, float] = state_dict.get("time_elapsed", {})
        for stage in ALL_STAGES:
            self._offsets[stage] = datetime.timedelta(
                seconds=time_elapsed.get(stage, 0)
            )

        start_times: dict[Stage, tuple[str, float]] = state_dict.get("start_times", {})
        for stage, (dt_str, monotonic) in start_times.items():
            self._start_time[stage] = TimeInfo(
                datetime.datetime.fromisoformat(dt_str), monotonic
            )

        end_times: dict[Stage, tuple[str, float]] = state_dict.get("end_times", {})
        for stage, (dt_str, monotonic) in end_times.items():
            self._end_time[stage] = TimeInfo(
                datetime.datetime.fromisoformat(dt_str), monotonic
            )

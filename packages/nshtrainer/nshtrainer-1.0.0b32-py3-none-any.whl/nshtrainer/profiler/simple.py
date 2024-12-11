from __future__ import annotations

import logging
from typing import Literal

from typing_extensions import override

from ._base import BaseProfilerConfig

log = logging.getLogger(__name__)


class SimpleProfilerConfig(BaseProfilerConfig):
    name: Literal["simple"] = "simple"

    extended: bool = True
    """
    If ``True``, adds extra columns representing number of calls and percentage of
        total time spent onrespective action.
    """

    @override
    def create_profiler(self, trainer_config):
        from lightning.pytorch.profilers.simple import SimpleProfiler

        if (dirpath := self.dirpath) is None:
            dirpath = trainer_config.directory.resolve_subdirectory(
                trainer_config.id, "profile"
            )

        if (filename := self.filename) is None:
            filename = f"{trainer_config.id}_profile.txt"

        return SimpleProfiler(
            extended=self.extended,
            dirpath=dirpath,
            filename=filename,
        )

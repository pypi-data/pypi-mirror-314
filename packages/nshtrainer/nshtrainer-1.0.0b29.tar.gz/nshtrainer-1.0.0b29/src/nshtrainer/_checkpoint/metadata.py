from __future__ import annotations

import copy
import datetime
import logging
from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

import nshconfig as C
import numpy as np
import torch

from ..util._environment_info import EnvironmentConfig
from ..util.path import compute_file_checksum, try_symlink_or_copy

if TYPE_CHECKING:
    from ..trainer.trainer import Trainer

log = logging.getLogger(__name__)


METADATA_PATH_SUFFIX = ".metadata.json"


def _full_hparams_dict(trainer: Trainer):
    hparams = {}
    hparams["trainer"] = trainer.hparams.model_dump(mode="json")

    if trainer.lightning_module is not None:
        from ..model import LightningModuleBase

        if isinstance(trainer.lightning_module, LightningModuleBase):
            hparams["model"] = trainer.lightning_module.hparams.model_dump(mode="json")

    return hparams


class CheckpointMetadata(C.Config):
    PATH_SUFFIX: ClassVar[str] = METADATA_PATH_SUFFIX

    checkpoint_path: Path
    checkpoint_filename: str
    checkpoint_checksum: str

    run_id: str
    name: str
    project: str | None
    checkpoint_timestamp: datetime.datetime
    start_timestamp: datetime.datetime | None

    epoch: int
    global_step: int
    training_time: datetime.timedelta
    metrics: dict[str, Any]
    environment: EnvironmentConfig

    hparams: Any | None

    @classmethod
    def from_file(cls, path: Path):
        return cls.model_validate_json(path.read_text(encoding="utf-8"))

    @classmethod
    def from_ckpt_path(cls, checkpoint_path: Path):
        if not (metadata_path := checkpoint_path.with_suffix(cls.PATH_SUFFIX)).exists():
            raise FileNotFoundError(
                f"Metadata file not found for checkpoint: {checkpoint_path}"
            )
        return cls.from_file(metadata_path)


def _generate_checkpoint_metadata(
    trainer: Trainer,
    checkpoint_path: Path,
    metadata_path: Path,
):
    checkpoint_timestamp = datetime.datetime.now()
    start_timestamp = trainer.start_time()
    training_time = trainer.time_elapsed()

    metrics: dict[str, Any] = {}
    for name, metric in copy.deepcopy(trainer.callback_metrics).items():
        match metric:
            case torch.Tensor() | np.ndarray():
                metrics[name] = metric.detach().cpu().item()
            case _:
                metrics[name] = metric

    return CheckpointMetadata(
        # checkpoint_path=checkpoint_path,
        # We should store the path as a relative path
        # to the metadata file to avoid issues with
        # moving the checkpoint directory
        checkpoint_path=checkpoint_path.relative_to(metadata_path.parent),
        checkpoint_filename=checkpoint_path.name,
        checkpoint_checksum=compute_file_checksum(checkpoint_path),
        run_id=trainer.hparams.id,
        name=trainer.hparams.full_name,
        project=trainer.hparams.project,
        checkpoint_timestamp=checkpoint_timestamp,
        start_timestamp=start_timestamp.datetime
        if start_timestamp is not None
        else None,
        epoch=trainer.current_epoch,
        global_step=trainer.global_step,
        training_time=training_time,
        metrics=metrics,
        environment=trainer.hparams.environment,
        hparams=_full_hparams_dict(trainer),
    )


def _metadata_path(checkpoint_path: Path):
    return checkpoint_path.with_suffix(CheckpointMetadata.PATH_SUFFIX)


def _write_checkpoint_metadata(trainer: Trainer, checkpoint_path: Path):
    metadata_path = _metadata_path(checkpoint_path)
    metadata = _generate_checkpoint_metadata(trainer, checkpoint_path, metadata_path)

    # Write the metadata to the checkpoint directory
    try:
        metadata_path.write_text(metadata.model_dump_json(indent=4), encoding="utf-8")
    except Exception:
        log.warning(f"Failed to write metadata to {metadata_path}", exc_info=True)
        return None

    log.debug(f"Checkpoint metadata written to {metadata_path}")
    return metadata_path


def _remove_checkpoint_metadata(checkpoint_path: Path):
    path = _metadata_path(checkpoint_path)
    try:
        path.unlink(missing_ok=True)
    except Exception:
        log.warning(f"Failed to remove {path}", exc_info=True)
    else:
        log.debug(f"Removed {path}")


def _link_checkpoint_metadata(checkpoint_path: Path, linked_checkpoint_path: Path):
    # First, remove any existing metadata files
    _remove_checkpoint_metadata(linked_checkpoint_path)

    # Link the metadata files to the new checkpoint
    path = _metadata_path(checkpoint_path)
    linked_path = _metadata_path(linked_checkpoint_path)
    try_symlink_or_copy(path, linked_path)


def _sort_ckpts_by_metadata(
    checkpoint_paths: list[Path],
    key: Callable[[CheckpointMetadata, Path], Any],
    reverse: bool = False,
):
    return sorted(
        [(CheckpointMetadata.from_ckpt_path(path), path) for path in checkpoint_paths],
        key=lambda args_tuple: key(*args_tuple),
        reverse=reverse,
    )

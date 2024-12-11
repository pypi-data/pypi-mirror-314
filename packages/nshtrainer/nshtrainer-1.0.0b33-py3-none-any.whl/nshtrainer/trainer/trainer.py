from __future__ import annotations

import logging
import os
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import torch
from lightning.fabric.plugins.environments.lsf import LSFEnvironment
from lightning.fabric.plugins.environments.slurm import SLURMEnvironment
from lightning.fabric.plugins.precision.precision import _PRECISION_INPUT
from lightning.pytorch import LightningModule
from lightning.pytorch import Trainer as LightningTrainer
from lightning.pytorch.callbacks import Callback
from lightning.pytorch.profilers import Profiler
from lightning.pytorch.trainer.states import TrainerFn
from lightning.pytorch.utilities.types import _EVALUATE_OUTPUT, _PREDICT_OUTPUT
from typing_extensions import Never, Unpack, assert_never, deprecated, override

from .._checkpoint.metadata import _write_checkpoint_metadata
from ..callbacks.base import resolve_all_callbacks
from ..util._environment_info import EnvironmentConfig
from ..util.bf16 import is_bf16_supported_no_emulation
from ._config import LightningTrainerKwargs, TrainerConfig
from ._runtime_callback import RuntimeTrackerCallback, Stage
from .accelerator import AcceleratorConfigBase
from .plugin import PluginConfigBase
from .signal_connector import _SignalConnector
from .strategy import StrategyConfigBase

log = logging.getLogger(__name__)


class Trainer(LightningTrainer):
    CHECKPOINT_HYPER_PARAMS_KEY = "trainer_hyper_parameters"

    @property
    def hparams(self) -> TrainerConfig:
        """The collection of hyperparameters saved with :meth:`save_hyperparameters`. It is mutable by the user. For
        the frozen set of initial hyperparameters, use :attr:`hparams_initial`.

        Returns:
            Mutable hyperparameters dictionary

        """
        return self._hparams

    @property
    @deprecated("Use `hparams` instead")
    def config(self):
        return cast(Never, self.hparams)

    @classmethod
    def hparams_cls(cls):
        return TrainerConfig

    @classmethod
    def _pre_init(cls, hparams: TrainerConfig):
        if (precision := hparams.set_float32_matmul_precision) is not None:
            torch.set_float32_matmul_precision(precision)

    @classmethod
    def _update_kwargs(
        cls,
        hparams: TrainerConfig,
        kwargs_ctor: LightningTrainerKwargs,
    ):
        kwargs: LightningTrainerKwargs = {
            "deterministic": hparams.deterministic,
            "fast_dev_run": hparams.fast_dev_run,
            "max_epochs": hparams.max_epochs,
            "min_epochs": hparams.min_epochs,
            "max_steps": hparams.max_steps,
            "min_steps": hparams.min_steps,
            "max_time": hparams.max_time,
            "limit_train_batches": hparams.limit_train_batches,
            "limit_val_batches": hparams.limit_val_batches,
            "limit_test_batches": hparams.limit_test_batches,
            "limit_predict_batches": hparams.limit_predict_batches,
            "overfit_batches": hparams.overfit_batches,
            "val_check_interval": hparams.val_check_interval,
            "num_sanity_val_steps": hparams.num_sanity_val_steps,
            "log_every_n_steps": hparams.log_every_n_steps,
            "inference_mode": hparams.inference_mode,
            "callbacks": [],
            "plugins": [],
            "logger": [],
            # Moved to `lightning_kwargs`:
            # "enable_checkpointing": hparams.enable_checkpointing,
            # "accelerator": hparams.accelerator,
            # "strategy": hparams.strategy,
            # "num_nodes": hparams.num_nodes,
            # "precision": hparams.precision,
            # "logger": hparams.logging.enabled,
            # "log_every_n_steps": hparams.log_every_n_steps,
            # "enable_progress_bar": hparams.enable_progress_bar,
            # "enable_model_summary": hparams.enable_model_summary,
            # "accumulate_grad_batches": hparams.accumulate_grad_batches,
            # "benchmark": hparams.benchmark,
            # "use_distributed_sampler": hparams.use_distributed_sampler,
            # "detect_anomaly": hparams.detect_anomaly,
            # "barebones": hparams.barebones,
            # "plugins": hparams.plugins,
            # "sync_batchnorm": hparams.sync_batchnorm,
            # "reload_dataloaders_every_n_epochs": hparams.reload_dataloaders_every_n_epochs,
        }

        def _update_key(key: str, new_value: Any):
            # First, check to see if the key is already in the kwargs.
            if key not in kwargs:
                kwargs[key] = new_value
                return

            # If the key is already in the kwargs, then we check the type:
            # - If the type is a sequence, then we extend the sequence.
            # - Otherwise, we just update the value but warn the user.

            match existing_value := kwargs[key]:
                case Sequence() as existing_value:
                    # Make sure value is a sequence too
                    if not isinstance(new_value, Sequence):
                        new_value = [new_value]
                    kwargs[key] = [*existing_value, *new_value]
                case _:
                    log.warning(
                        f"Trainer.__init__: Overwriting existing value {existing_value=} with {new_value=} for key {key=}."
                    )
                    kwargs[key] = new_value

        def _update_kwargs(**update: Unpack[LightningTrainerKwargs]):
            for key, value in update.items():
                _update_key(key, value)

        # Set `barebones`
        if hparams.barebones:
            _update_kwargs(barebones=True)

        # Set `default_root_dir` if `auto_set_default_root_dir` is enabled.
        if hparams.auto_set_default_root_dir:
            if kwargs.get("default_root_dir"):
                raise ValueError(
                    "You have set `hparams.default_root_dir`. "
                    "But we are trying to set it automatically. "
                    "Please use `hparams.directory.base` rather than `hparams.default_root_dir`. "
                    "If you want to set it manually, please set `hparams.auto_set_default_root_dir=False`."
                )

            _update_kwargs(
                default_root_dir=hparams.directory.resolve_run_root_directory(
                    hparams.id
                )
            )

        if (devices_input := hparams.devices) is not None:
            match devices_input:
                case "all":
                    devices = -1
                case "auto":
                    devices = "auto"
                case Sequence():
                    devices = list(devices_input)
                case _:
                    raise ValueError(f"Invalid value for devices={devices_input}.")

            _update_kwargs(devices=devices)

        if (use_distributed_sampler := hparams.use_distributed_sampler) is not None:
            _update_kwargs(use_distributed_sampler=use_distributed_sampler)

        if (accelerator := hparams.accelerator) is not None:
            if isinstance(accelerator, AcceleratorConfigBase):
                accelerator = accelerator.create_accelerator(hparams)
            _update_kwargs(accelerator=accelerator)

        if (strategy := hparams.strategy) is not None:
            if isinstance(strategy, StrategyConfigBase):
                strategy = strategy.create_strategy(hparams)
            _update_kwargs(strategy=strategy)

        if (precision := hparams.precision) is not None:
            resolved_precision: _PRECISION_INPUT
            match precision:
                case "64-true" | "32-true" | "bf16-mixed":
                    resolved_precision = precision
                case "fp16-mixed":
                    resolved_precision = "16-mixed"
                case "16-mixed-auto":
                    try:
                        resolved_precision = (
                            "bf16-mixed"
                            if is_bf16_supported_no_emulation()
                            else "16-mixed"
                        )
                    except BaseException:
                        resolved_precision = "16-mixed"
                        log.warning(
                            "Failed to detect bfloat16 support. Falling back to 16-mixed."
                        )

                    log.critical(
                        f"Auto-resolving {precision=} to {resolved_precision=}."
                    )
                case _:
                    assert_never(precision)

            _update_kwargs(precision=resolved_precision)

        if (detect_anomaly := hparams.detect_anomaly) is not None:
            _update_kwargs(detect_anomaly=detect_anomaly)

        if (
            grad_clip_config := hparams.gradient_clipping
        ) is not None and grad_clip_config.enabled:
            # kwargs["gradient_clip_algorithm"] = grad_clip_config.algorithm
            # kwargs["gradient_clip_val"] = grad_clip_config.value
            _update_kwargs(
                gradient_clip_algorithm=grad_clip_config.algorithm,
                gradient_clip_val=grad_clip_config.value,
            )

        if profiler_config := hparams.profiler:
            if (profiler := profiler_config.create_profiler(hparams)) is None:
                log.warning(f"Profiler hparams {profiler_config=} returned None.")
            # Make sure that the profiler is an instance of `Profiler`.
            elif not isinstance(profiler, Profiler):
                raise ValueError(f"{profiler=} is not an instance of `{Profiler}`.")
            # Otherwise, if the profiler is a string (e.g., "simpe", "advanced", "pytorch"),
            #   then we just pass it through.
            else:
                _update_kwargs(profiler=profiler)

        if callbacks := resolve_all_callbacks(hparams):
            _update_kwargs(callbacks=callbacks)

        if plugin_configs := hparams.plugins:
            _update_kwargs(
                plugins=[
                    plugin_config.create_plugin(hparams)
                    for plugin_config in plugin_configs
                ]
            )

        _update_kwargs(
            logger=[
                logger
                for logger_config in hparams._nshtrainer_all_logger_configs()
                if logger_config is not None
                and (logger := logger_config.create_logger(hparams)) is not None
            ]
        )

        if hparams.auto_determine_num_nodes:
            # When num_nodes is auto, we need to detect the number of nodes.
            if SLURMEnvironment.detect():
                if (num_nodes := os.environ.get("SLURM_NNODES")) is not None:
                    num_nodes = int(num_nodes)
                    log.critical(f"SLURM detected with {num_nodes=}.")
                    _update_kwargs(num_nodes=num_nodes)
                else:
                    log.critical(
                        "SLURM detected, but SLURM_NNODES not found. "
                        "We'll continue without setting num_nodes, but this may cause issues."
                    )

            elif LSFEnvironment.detect():
                num_nodes = LSFEnvironment().world_size()
                log.critical(f"LSF detected with {num_nodes=}.")
                _update_kwargs(num_nodes=num_nodes)
            else:
                log.info(
                    "hparams.auto_determine_num_nodes ignored because no SLURM or LSF detected."
                )

        # Update the kwargs with the additional trainer kwargs
        _update_kwargs(**cast(Any, hparams.additional_lightning_kwargs))
        _update_kwargs(**hparams.lightning_kwargs)
        _update_kwargs(**kwargs_ctor)

        # Handle barebones mode
        if kwargs.get("barebones"):
            # Remove the logger if it's an empty list
            if (logger := kwargs.get("logger")) is not None and not logger:
                kwargs["logger"] = None

        return kwargs

    if TYPE_CHECKING:
        callbacks: list[Callback]

    @override
    def __init__(
        self,
        hparams: TrainerConfig | Mapping[str, Any],
        /,
        **kwargs: Unpack[LightningTrainerKwargs],
    ):
        # Validate the hparams.
        hparams_cls = Trainer.hparams_cls()
        if isinstance(hparams, Mapping):
            hparams = hparams_cls.model_validate(hparams)
        elif not isinstance(hparams, hparams_cls):
            raise ValueError(
                f"Trainer hparams must either be an instance of {hparams_cls} or a mapping. "
                f"Got {type(hparams)=} instead."
            )
        hparams = hparams.model_deep_validate()
        hparams._nshtrainer_validate_before_run()

        self._pre_init(hparams)

        kwargs = self._update_kwargs(hparams, kwargs)
        log.critical(f"LightningTrainer.__init__ with {kwargs=}.")

        self._hparams = hparams
        self.debug = self.hparams.debug

        experimental_profiler = None
        if hparams.experimental_barebones_profiler_enabled:
            experimental_profiler = kwargs.pop("profiler", None)
            log.warning(
                "Barebones profiler is enabled. This is an experimental feature and may not work as expected."
            )

        experimental_barebones_progress_bar = None
        if hparams.experimental_barebones_progress_bar_enabled:
            experimental_barebones_progress_bar = kwargs.pop(
                "enable_progress_bar", True
            )

        super().__init__(**kwargs)

        # Set up the profiler again
        if experimental_profiler is not None:
            from lightning.pytorch.trainer import setup

            setup._init_profiler(self, experimental_profiler)

        # Set up the progress bar again
        if experimental_barebones_progress_bar is not None:
            self._callback_connector._configure_progress_bar(
                experimental_barebones_progress_bar
            )

        # Add our own start time callback to measure the start time.
        self.callbacks.append(RuntimeTrackerCallback())

        # Replace the signal connector with our own.
        self._signal_connector = _SignalConnector(self)

        # Print out the log dir, so that we can easily find it in the logs.
        if log_dir := self.log_dir:
            log_dir = str(Path(log_dir).resolve())
        log.critical(f"LightningTrainer log directory: {self.log_dir}.")

        # Set the checkpoint
        if (ckpt_path := hparams.ckpt_path) is not None:
            self.ckpt_path = str(Path(ckpt_path).resolve().absolute())

    def __runtime_tracker(self):
        return next(
            (
                callback
                for callback in self.callbacks
                if isinstance(callback, RuntimeTrackerCallback)
            ),
            None,
        )

    def __current_stage(self) -> Stage:
        match self.state.fn:
            case None:
                raise ValueError(
                    "Trainer state function is not set. "
                    "You must call `fit`, `validate`, `test`, or `predict`, "
                    "or explicitly provide a stage."
                )
            case TrainerFn.FITTING:
                return "train"
            case TrainerFn.VALIDATING:
                return "validate"
            case TrainerFn.TESTING:
                return "test"
            case TrainerFn.PREDICTING:
                return "predict"
            case _:
                assert_never(self.state.fn)

    def start_time(self, stage: Stage | None = None):
        """Return the start time of the run"""
        if (tracker := self.__runtime_tracker()) is None:
            raise ValueError(
                "RuntimeTrackerCallback is not set. Cannot get start time."
            )
        if stage is None:
            stage = self.__current_stage()

        return tracker.start_time(stage)

    def end_time(self, stage: Stage | None = None):
        """Return the end time of the run"""
        if (tracker := self.__runtime_tracker()) is None:
            raise ValueError(
                "RuntimeTrackerCallback is not set. Cannot get start time."
            )
        if stage is None:
            stage = self.__current_stage()

        return tracker.end_time(stage)

    def time_elapsed(self, stage: Stage | None = None):
        """Return the time elapsed for the run"""
        if (tracker := self.__runtime_tracker()) is None:
            raise ValueError(
                "RuntimeTrackerCallback is not set. Cannot get start time."
            )
        if stage is None:
            stage = self.__current_stage()

        return tracker.time_elapsed(stage)

    @property
    def _base_module(self):
        if self.lightning_module is None:
            raise ValueError("LightningModule is not set.")

        from ..model.base import LightningModuleBase

        if not isinstance(self.lightning_module, LightningModuleBase):
            raise ValueError(
                f"LightningModule is not an instance of {LightningModuleBase}."
            )

        return self.lightning_module

    @override
    def _run(
        self, model: LightningModule, ckpt_path: str | Path | None = None
    ) -> _EVALUATE_OUTPUT | _PREDICT_OUTPUT | None:
        """Lightning doesn't support gradient clipping with manual optimization.
        We patch the `Trainer._run` method to throw if gradient clipping is enabled
        and `model.automatic_optimization` is False.
        """
        # Save the current environment information
        datamodule = getattr(self, "datamodule", None)
        self.hparams.environment = EnvironmentConfig.from_current_environment(
            self.hparams, model, datamodule
        )

        # If gradient clipping is enabled, then we need to make sure that
        # `model.automatic_optimization` is enabled. Otherwise, gradient clipping
        # is not actually going to do anything, as we expect the user to manually
        # call `optimizer.step()` and `optimizer.zero_grad()`.
        if not model.automatic_optimization and (
            self.gradient_clip_val is not None
            or self.gradient_clip_algorithm is not None
        ):
            raise ValueError(
                "Automatic gradient clipping is not supported with manual optimization. "
                f"Please set {model.__class__.__name__}.automatic_optimization to True "
                "or disable automatic gradient clipping. "
            )

        return super()._run(model, ckpt_path)

    @override
    def save_checkpoint(
        self,
        filepath: str | Path,
        weights_only: bool = False,
        storage_options: Any | None = None,
    ):
        filepath = Path(filepath)

        super().save_checkpoint(filepath, weights_only, storage_options)

        # Save the checkpoint metadata
        metadata_path = None
        if self.hparams.save_checkpoint_metadata and self.is_global_zero:
            # Generate the metadata and write to disk
            metadata_path = _write_checkpoint_metadata(self, filepath)

        # Call the `on_checkpoint_saved` method on all callbacks
        from .. import _callback

        _callback._call_on_checkpoint_saved(self, filepath, metadata_path)

    @classmethod
    def hparams_from_checkpoint(
        cls,
        ckpt_or_path: dict[str, Any] | str | Path,
        /,
        strict: bool | None = None,
        *,
        update_hparams: Callable[[TrainerConfig], TrainerConfig] | None = None,
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
        path: str | Path,
        strict: bool | None = None,
        *,
        update_hparams: Callable[[TrainerConfig], TrainerConfig] | None = None,
        update_hparams_dict: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
    ):
        hparams = cls.hparams_from_checkpoint(
            path,
            strict=strict,
            update_hparams=update_hparams,
            update_hparams_dict=update_hparams_dict,
        )
        return cls(hparams)

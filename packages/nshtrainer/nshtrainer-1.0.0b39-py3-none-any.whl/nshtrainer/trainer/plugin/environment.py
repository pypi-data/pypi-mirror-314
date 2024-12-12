from __future__ import annotations

import signal
from typing import Any, Literal

from lightning.pytorch.plugins.environments import ClusterEnvironment
from typing_extensions import override

from ...util.config.dtype import DTypeConfig
from .base import PluginConfigBase, plugin_registry


@plugin_registry.register
class KubeflowEnvironmentPlugin(PluginConfigBase):
    name: Literal["kubeflow_environment"] = "kubeflow_environment"

    """Environment for distributed training using the PyTorchJob operator from Kubeflow.

    This environment, unlike others, does not get auto-detected and needs to be passed
    to the Fabric/Trainer constructor manually.
    """

    @override
    def create_plugin(self, trainer_config) -> ClusterEnvironment:
        from lightning.fabric.plugins.environments.kubeflow import KubeflowEnvironment

        return KubeflowEnvironment()


@plugin_registry.register
class LightningEnvironmentPlugin(PluginConfigBase):
    name: Literal["lightning_environment"] = "lightning_environment"

    """The default environment used by Lightning for a single node or free cluster (not managed).

    There are two modes the Lightning environment can operate with:
    1. User launches main process by `python train.py ...` with no additional environment variables.
       Lightning will spawn new worker processes for distributed training in the current node.
    2. User launches all processes manually or with utilities like `torch.distributed.launch`.
       The appropriate environment variables need to be set, and at minimum `LOCAL_RANK`.
    """

    @override
    def create_plugin(self, trainer_config) -> ClusterEnvironment:
        from lightning.fabric.plugins.environments.lightning import LightningEnvironment

        return LightningEnvironment()


@plugin_registry.register
class LSFEnvironmentPlugin(PluginConfigBase):
    name: Literal["lsf_environment"] = "lsf_environment"

    """An environment for running on clusters managed by the LSF resource manager.

    It is expected that any execution using this ClusterEnvironment was executed
    using the Job Step Manager i.e. `jsrun`.
    """

    @override
    def create_plugin(self, trainer_config) -> ClusterEnvironment:
        from lightning.fabric.plugins.environments.lsf import LSFEnvironment

        return LSFEnvironment()


@plugin_registry.register
class MPIEnvironmentPlugin(PluginConfigBase):
    name: Literal["mpi_environment"] = "mpi_environment"

    """An environment for running on clusters with processes created through MPI.

    Requires the installation of the `mpi4py` package.
    """

    @override
    def create_plugin(self, trainer_config) -> ClusterEnvironment:
        from lightning.fabric.plugins.environments.mpi import MPIEnvironment

        return MPIEnvironment()


@plugin_registry.register
class SLURMEnvironmentPlugin(PluginConfigBase):
    name: Literal["slurm_environment"] = "slurm_environment"

    auto_requeue: bool = True
    """Whether automatic job resubmission is enabled or not."""

    requeue_signal: signal.Signals | None = None
    """The signal that SLURM will send to indicate that the job should be requeued."""

    @override
    def create_plugin(self, trainer_config) -> ClusterEnvironment:
        from lightning.fabric.plugins.environments.slurm import SLURMEnvironment

        return SLURMEnvironment(
            auto_requeue=self.auto_requeue,
            requeue_signal=self.requeue_signal,
        )


@plugin_registry.register
class TorchElasticEnvironmentPlugin(PluginConfigBase):
    name: Literal["torchelastic_environment"] = "torchelastic_environment"

    """Environment for fault-tolerant and elastic training with torchelastic."""

    @override
    def create_plugin(self, trainer_config) -> ClusterEnvironment:
        from lightning.fabric.plugins.environments.torchelastic import (
            TorchElasticEnvironment,
        )

        return TorchElasticEnvironment()


@plugin_registry.register
class XLAEnvironmentPlugin(PluginConfigBase):
    name: Literal["xla_environment"] = "xla_environment"

    """Cluster environment for training on a TPU Pod with the PyTorch/XLA library."""

    @override
    def create_plugin(self, trainer_config) -> ClusterEnvironment:
        from lightning.fabric.plugins.environments.xla import XLAEnvironment

        return XLAEnvironment()

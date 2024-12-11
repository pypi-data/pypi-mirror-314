from __future__ import annotations

import getpass
import importlib.metadata
import inspect
import logging
import os
import platform
import socket
import sys
from datetime import timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import nshconfig as C
import psutil
import torch
from lightning.pytorch import LightningDataModule, LightningModule
from packaging import version
from typing_extensions import Self

from .slurm import parse_slurm_node_list

if TYPE_CHECKING:
    from ..trainer._config import TrainerConfig


log = logging.getLogger(__name__)


class EnvironmentClassInformationConfig(C.Config):
    """Configuration for class information in the environment."""

    name: str | None = None
    """The name of the class."""

    module: str | None = None
    """The module where the class is defined."""

    full_name: str | None = None
    """The fully qualified name of the class."""

    file_path: Path | None = None
    """The file path where the class is defined."""

    source_file_path: Path | None = None
    """The source file path of the class, if available."""

    @classmethod
    def empty(cls):
        return cls(
            name=None,
            module=None,
            full_name=None,
            file_path=None,
            source_file_path=None,
        )

    @classmethod
    def from_class(cls, cls_: type):
        name = cls_.__name__
        module = cls_.__module__
        full_name = f"{cls_.__module__}.{cls_.__qualname__}"

        file_path = inspect.getfile(cls_)
        source_file_path = inspect.getsourcefile(cls_)
        return cls(
            name=name,
            module=module,
            full_name=full_name,
            file_path=Path(file_path),
            source_file_path=Path(source_file_path) if source_file_path else None,
        )

    @classmethod
    def from_instance(cls, instance: object):
        return cls.from_class(type(instance))


class EnvironmentSLURMInformationConfig(C.Config):
    """Configuration for SLURM environment information."""

    hostname: str | None = None
    """The hostname of the current node."""

    hostnames: list[str] | None = None
    """List of hostnames for all nodes in the job."""

    job_id: str | None = None
    """The SLURM job ID."""

    raw_job_id: str | None = None
    """The raw SLURM job ID."""

    array_job_id: str | None = None
    """The SLURM array job ID, if applicable."""

    array_task_id: str | None = None
    """The SLURM array task ID, if applicable."""

    num_tasks: int | None = None
    """The number of tasks in the SLURM job."""

    num_nodes: int | None = None
    """The number of nodes in the SLURM job."""

    node: str | int | None = None
    """The node ID or name."""

    global_rank: int | None = None
    """The global rank of the current process."""

    local_rank: int | None = None
    """The local rank of the current process within its node."""

    @classmethod
    def empty(cls):
        return cls(
            hostname=None,
            hostnames=None,
            job_id=None,
            raw_job_id=None,
            array_job_id=None,
            array_task_id=None,
            num_tasks=None,
            num_nodes=None,
            node=None,
            global_rank=None,
            local_rank=None,
        )

    @classmethod
    def from_current_environment(cls):
        try:
            from lightning.fabric.plugins.environments.slurm import SLURMEnvironment

            if not SLURMEnvironment.detect():
                return None

            hostname = socket.gethostname()
            hostnames = [hostname]
            if node_list := os.environ.get("SLURM_JOB_NODELIST", ""):
                hostnames = parse_slurm_node_list(node_list)

            raw_job_id = os.environ["SLURM_JOB_ID"]
            job_id = raw_job_id
            array_job_id = os.environ.get("SLURM_ARRAY_JOB_ID")
            array_task_id = os.environ.get("SLURM_ARRAY_TASK_ID")
            if array_job_id and array_task_id:
                job_id = f"{array_job_id}_{array_task_id}"

            num_tasks = int(os.environ["SLURM_NTASKS"])
            num_nodes = int(os.environ["SLURM_JOB_NUM_NODES"])

            node_id = os.environ.get("SLURM_NODEID")

            global_rank = int(os.environ["SLURM_PROCID"])
            local_rank = int(os.environ["SLURM_LOCALID"])

            return cls(
                hostname=hostname,
                hostnames=hostnames,
                job_id=job_id,
                raw_job_id=raw_job_id,
                array_job_id=array_job_id,
                array_task_id=array_task_id,
                num_tasks=num_tasks,
                num_nodes=num_nodes,
                node=node_id,
                global_rank=global_rank,
                local_rank=local_rank,
            )
        except (ImportError, RuntimeError, ValueError, KeyError):
            return None


class EnvironmentLSFInformationConfig(C.Config):
    """Configuration for LSF environment information."""

    hostname: str | None = None
    """The hostname of the current node."""

    hostnames: list[str] | None = None
    """List of hostnames for all nodes in the job."""

    job_id: str | None = None
    """The LSF job ID."""

    array_job_id: str | None = None
    """The LSF array job ID, if applicable."""

    array_task_id: str | None = None
    """The LSF array task ID, if applicable."""

    num_tasks: int | None = None
    """The number of tasks in the LSF job."""

    num_nodes: int | None = None
    """The number of nodes in the LSF job."""

    node: str | int | None = None
    """The node ID or name."""

    global_rank: int | None = None
    """The global rank of the current process."""

    local_rank: int | None = None
    """The local rank of the current process within its node."""

    @classmethod
    def empty(cls):
        return cls(
            hostname=None,
            hostnames=None,
            job_id=None,
            array_job_id=None,
            array_task_id=None,
            num_tasks=None,
            num_nodes=None,
            node=None,
            global_rank=None,
            local_rank=None,
        )

    @classmethod
    def from_current_environment(cls):
        try:
            import os
            import socket

            hostname = socket.gethostname()
            hostnames = [hostname]
            if node_list := os.environ.get("LSB_HOSTS", ""):
                hostnames = node_list.split()

            job_id = os.environ["LSB_JOBID"]
            array_job_id = os.environ.get("LSB_JOBINDEX")
            array_task_id = os.environ.get("LSB_JOBINDEX")

            num_tasks = int(os.environ.get("LSB_DJOB_NUMPROC", 1))
            num_nodes = len(set(hostnames))

            node_id = (
                os.environ.get("LSB_HOSTS", "").split().index(hostname)
                if "LSB_HOSTS" in os.environ
                else None
            )

            # LSF doesn't have direct equivalents for global_rank and local_rank
            # You might need to calculate these based on your specific setup
            global_rank = int(os.environ.get("PMI_RANK", 0))
            local_rank = int(os.environ.get("LSB_RANK", 0))

            return cls(
                hostname=hostname,
                hostnames=hostnames,
                job_id=job_id,
                array_job_id=array_job_id,
                array_task_id=array_task_id,
                num_tasks=num_tasks,
                num_nodes=num_nodes,
                node=node_id,
                global_rank=global_rank,
                local_rank=local_rank,
            )
        except (ImportError, RuntimeError, ValueError, KeyError):
            return None


class EnvironmentLinuxEnvironmentConfig(C.Config):
    """Configuration for Linux environment information."""

    user: str | None = None
    """The current user."""

    hostname: str | None = None
    """The hostname of the machine."""

    system: str | None = None
    """The operating system name."""

    release: str | None = None
    """The operating system release."""

    version: str | None = None
    """The operating system version."""

    machine: str | None = None
    """The machine type."""

    processor: str | None = None
    """The processor type."""

    cpu_count: int | None = None
    """The number of CPUs."""

    memory: int | None = None
    """The total system memory in bytes."""

    uptime: timedelta | None = None
    """The system uptime."""

    boot_time: float | None = None
    """The system boot time as a timestamp."""

    load_avg: tuple[float, float, float] | None = None
    """The system load average (1, 5, and 15 minutes)."""

    @classmethod
    def empty(cls):
        return cls(
            user=None,
            hostname=None,
            system=None,
            release=None,
            version=None,
            machine=None,
            processor=None,
            cpu_count=None,
            memory=None,
            uptime=None,
            boot_time=None,
            load_avg=None,
        )

    @classmethod
    def from_current_environment(cls):
        return cls(
            user=getpass.getuser(),
            hostname=platform.node(),
            system=platform.system(),
            release=platform.release(),
            version=platform.version(),
            machine=platform.machine(),
            processor=platform.processor(),
            cpu_count=os.cpu_count(),
            memory=psutil.virtual_memory().total,
            uptime=timedelta(seconds=psutil.boot_time()),
            boot_time=psutil.boot_time(),
            load_avg=os.getloadavg(),
        )


class EnvironmentSnapshotConfig(C.Config):
    """Configuration for environment snapshot information."""

    snapshot_dir: Path | None = None
    """The directory where the snapshot is stored."""

    modules: list[str] | None = None
    """List of modules included in the snapshot."""

    @classmethod
    def empty(cls):
        return cls(snapshot_dir=None, modules=None)

    @classmethod
    def from_current_environment(cls):
        draft = cls.draft()
        if snapshot_dir := os.environ.get("NSHRUNNER_SNAPSHOT_DIR"):
            draft.snapshot_dir = Path(snapshot_dir)
        if modules := os.environ.get("NSHRUNNER_SNAPSHOT_MODULES"):
            draft.modules = modules.split(",")
        return draft.finalize()


class EnvironmentPackageConfig(C.Config):
    """Configuration for Python package information."""

    name: str | None = None
    """The name of the package."""

    version: str | None = None
    """The version of the package."""

    path: Path | None = None
    """The installation path of the package."""

    summary: str | None = None
    """A brief summary of the package."""

    author: str | None = None
    """The author of the package."""

    license: str | None = None
    """The license of the package."""

    requires: list[str] | None = None
    """List of package dependencies."""

    @classmethod
    def empty(cls):
        return cls(
            name=None,
            version=None,
            path=None,
            summary=None,
            author=None,
            license=None,
            requires=None,
        )

    @classmethod
    def from_current_environment(cls):
        python_packages: dict[str, Self] = {}
        try:
            for dist in importlib.metadata.distributions():
                try:
                    # Get package metadata
                    metadata = dist.metadata

                    # Parse the version, stripping any local version identifier
                    pkg_version = version.parse(dist.version)
                    clean_version = (
                        f"{pkg_version.major}.{pkg_version.minor}.{pkg_version.micro}"
                    )

                    # Get requirements
                    requires = []
                    for req in dist.requires or []:
                        try:
                            requires.append(str(req))
                        except ValueError:
                            # If there's an invalid requirement, we'll skip it
                            log.warning(
                                f"Skipping invalid requirement for {dist.name}: {req}"
                            )

                    python_packages[dist.name] = cls(
                        name=dist.name,
                        version=clean_version,
                        path=Path(str(f)) if (f := dist.locate_file("")) else None,
                        summary=metadata["Summary"] if "Summary" in metadata else None,
                        author=metadata["Author"] if "Author" in metadata else None,
                        license=metadata["License"] if "License" in metadata else None,
                        requires=requires,
                    )
                except Exception:
                    log.warning(f"Error processing package {dist.name}", exc_info=True)

        except ImportError:
            log.warning(
                "importlib.metadata not available, skipping package information"
            )

        return python_packages


class EnvironmentGPUConfig(C.Config):
    """Configuration for individual GPU information."""

    name: str | None = None
    """Name of the GPU."""

    total_memory: int | None = None
    """Total memory of the GPU in bytes."""

    major: int | None = None
    """Major version of CUDA capability."""

    minor: int | None = None
    """Minor version of CUDA capability."""

    multi_processor_count: int | None = None
    """Number of multiprocessors on the GPU."""

    @classmethod
    def empty(cls):
        return cls(
            name=None,
            total_memory=None,
            major=None,
            minor=None,
            multi_processor_count=None,
        )


class EnvironmentCUDAConfig(C.Config):
    """Configuration for CUDA environment information."""

    is_available: bool | None = None
    """Whether CUDA is available."""

    version: str | None = None
    """CUDA version."""

    cudnn_version: int | None = None
    """cuDNN version."""

    @classmethod
    def empty(cls):
        return cls(is_available=None, version=None, cudnn_version=None)


class EnvironmentHardwareConfig(C.Config):
    """Configuration for hardware information."""

    cpu_count_physical: int | None = None
    """Number of physical CPU cores."""

    cpu_count_logical: int | None = None
    """Number of logical CPU cores."""

    cpu_frequency_current: float | None = None
    """Current CPU frequency in MHz."""

    cpu_frequency_min: float | None = None
    """Minimum CPU frequency in MHz."""

    cpu_frequency_max: float | None = None
    """Maximum CPU frequency in MHz."""

    ram_total: int | None = None
    """Total RAM in bytes."""

    ram_available: int | None = None
    """Available RAM in bytes."""

    disk_total: int | None = None
    """Total disk space in bytes."""

    disk_used: int | None = None
    """Used disk space in bytes."""

    disk_free: int | None = None
    """Free disk space in bytes."""

    gpu_count: int | None = None
    """Number of GPUs available."""

    gpus: list[EnvironmentGPUConfig] | None = None
    """List of GPU configurations."""

    cuda: EnvironmentCUDAConfig | None = None
    """CUDA environment configuration."""

    @classmethod
    def empty(cls):
        return cls(
            cpu_count_physical=None,
            cpu_count_logical=None,
            cpu_frequency_current=None,
            cpu_frequency_min=None,
            cpu_frequency_max=None,
            ram_total=None,
            ram_available=None,
            disk_total=None,
            disk_used=None,
            disk_free=None,
            gpu_count=None,
            gpus=None,
            cuda=None,
        )

    @classmethod
    def from_current_environment(cls):
        draft = cls.draft()

        # CPU information
        draft.cpu_count_physical = psutil.cpu_count(logical=False)
        draft.cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq()
        if cpu_freq:
            draft.cpu_frequency_current = cpu_freq.current
            draft.cpu_frequency_min = cpu_freq.min
            draft.cpu_frequency_max = cpu_freq.max

        # RAM information
        ram = psutil.virtual_memory()
        draft.ram_total = ram.total
        draft.ram_available = ram.available

        # Disk information
        disk = psutil.disk_usage("/")
        draft.disk_total = disk.total
        draft.disk_used = disk.used
        draft.disk_free = disk.free

        # GPU and CUDA information
        draft.cuda = EnvironmentCUDAConfig(
            is_available=torch.cuda.is_available(),
            version=cast(Any, torch).version.cuda,
            cudnn_version=torch.backends.cudnn.version()
            if torch.backends.cudnn.is_available()
            else None,
        )

        if draft.cuda.is_available:
            draft.gpu_count = torch.cuda.device_count()
            draft.gpus = []
            for i in range(draft.gpu_count):
                gpu_props = torch.cuda.get_device_properties(i)
                gpu_config = EnvironmentGPUConfig(
                    name=gpu_props.name,
                    total_memory=gpu_props.total_memory,
                    major=gpu_props.major,
                    minor=gpu_props.minor,
                    multi_processor_count=gpu_props.multi_processor_count,
                )
                draft.gpus.append(gpu_config)

        return draft.finalize()


class GitRepositoryConfig(C.Config):
    """Configuration for Git repository information."""

    is_git_repo: bool | None = None
    """Whether the current directory is a Git repository."""

    branch: str | None = None
    """The current Git branch."""

    commit_hash: str | None = None
    """The current commit hash."""

    commit_message: str | None = None
    """The current commit message."""

    author: str | None = None
    """The author of the current commit."""

    commit_date: str | None = None
    """The date of the current commit."""

    remote_url: str | None = None
    """The URL of the remote repository."""

    is_dirty: bool | None = None
    """Whether there are uncommitted changes."""

    @classmethod
    def empty(cls):
        return cls(
            is_git_repo=None,
            branch=None,
            commit_hash=None,
            commit_message=None,
            author=None,
            commit_date=None,
            remote_url=None,
            is_dirty=None,
        )

    @classmethod
    def from_current_directory(cls):
        try:
            import git
        except ImportError:
            return cls()

        draft = cls.draft()
        try:
            repo = git.Repo(os.getcwd(), search_parent_directories=True)
            draft.is_git_repo = True
            draft.branch = repo.active_branch.name
            commit = repo.head.commit
            draft.commit_hash = commit.hexsha

            # Handle both str and bytes for commit message
            if isinstance(commit.message, str):
                draft.commit_message = commit.message.strip()
            elif isinstance(commit.message, bytes):
                draft.commit_message = commit.message.decode(
                    "utf-8", errors="replace"
                ).strip()
            else:
                draft.commit_message = str(commit.message).strip()

            draft.author = f"{commit.author.name} <{commit.author.email}>"
            draft.commit_date = commit.committed_datetime.isoformat()
            if repo.remotes:
                draft.remote_url = repo.remotes.origin.url
            draft.is_dirty = repo.is_dirty()
        except git.InvalidGitRepositoryError:
            draft.is_git_repo = False
        except Exception:
            log.warning("Failed to get Git repository information", exc_info=True)
            draft.is_git_repo = None

        return draft.finalize()


class EnvironmentConfig(C.Config):
    """Configuration for the overall environment."""

    cwd: Path | None = None
    """The current working directory."""

    snapshot: EnvironmentSnapshotConfig | None = None
    """The environment snapshot configuration."""

    python_executable: Path | None = None
    """The path to the Python executable."""

    python_path: list[Path] | None = None
    """The Python path."""

    python_version: str | None = None
    """The Python version."""

    python_packages: dict[str, EnvironmentPackageConfig] | None = None
    """A mapping of package names to their configurations."""

    config: EnvironmentClassInformationConfig | None = None
    """The configuration class information."""

    model: EnvironmentClassInformationConfig | None = None
    """The Lightning module class information."""

    datamodule: EnvironmentClassInformationConfig | None = None
    """The Lightning data module class information."""

    linux: EnvironmentLinuxEnvironmentConfig | None = None
    """The Linux environment information."""

    hardware: EnvironmentHardwareConfig | None = None
    """Hardware configuration information."""

    slurm: EnvironmentSLURMInformationConfig | None = None
    """The SLURM environment information."""

    lsf: EnvironmentLSFInformationConfig | None = None
    """The LSF environment information."""

    base_dir: Path | None = None
    """The base directory for the run."""

    log_dir: Path | None = None
    """The directory for logs."""

    checkpoint_dir: Path | None = None
    """The directory for checkpoints."""

    stdio_dir: Path | None = None
    """The directory for standard input/output files."""

    seed: int | None = None
    """The global random seed."""

    seed_workers: bool | None = None
    """Whether to seed workers."""

    git: GitRepositoryConfig | None = None
    """Git repository information."""

    @classmethod
    def empty(cls):
        return cls(
            cwd=None,
            snapshot=None,
            python_executable=None,
            python_path=None,
            python_version=None,
            python_packages=None,
            config=None,
            model=None,
            linux=None,
            hardware=None,
            slurm=None,
            lsf=None,
            base_dir=None,
            log_dir=None,
            checkpoint_dir=None,
            stdio_dir=None,
            seed=None,
            seed_workers=None,
            git=None,
        )

    @classmethod
    def from_current_environment(
        cls,
        trainer_config: TrainerConfig,
        model: LightningModule,
        datamodule: LightningDataModule | None = None,
    ):
        draft = cls.draft()
        draft.cwd = Path(os.getcwd())
        draft.python_executable = Path(sys.executable)
        draft.python_path = [Path(path) for path in sys.path]
        draft.python_version = sys.version
        draft.python_packages = EnvironmentPackageConfig.from_current_environment()
        draft.config = EnvironmentClassInformationConfig.from_instance(trainer_config)
        draft.model = EnvironmentClassInformationConfig.from_instance(model)
        if datamodule is not None:
            draft.datamodule = EnvironmentClassInformationConfig.from_instance(
                datamodule
            )
        draft.linux = EnvironmentLinuxEnvironmentConfig.from_current_environment()
        draft.hardware = EnvironmentHardwareConfig.from_current_environment()
        draft.slurm = EnvironmentSLURMInformationConfig.from_current_environment()
        draft.lsf = EnvironmentLSFInformationConfig.from_current_environment()
        draft.base_dir = trainer_config.directory.resolve_run_root_directory(
            trainer_config.id
        )
        draft.log_dir = trainer_config.directory.resolve_subdirectory(
            trainer_config.id, "log"
        )
        draft.checkpoint_dir = trainer_config.directory.resolve_subdirectory(
            trainer_config.id, "checkpoint"
        )
        draft.stdio_dir = trainer_config.directory.resolve_subdirectory(
            trainer_config.id, "stdio"
        )
        draft.seed = (
            int(seed_str) if (seed_str := os.environ.get("PL_GLOBAL_SEED")) else None
        )
        draft.seed_workers = (
            bool(int(seed_everything))
            if (seed_everything := os.environ.get("PL_SEED_WORKERS"))
            else None
        )
        draft.snapshot = EnvironmentSnapshotConfig.from_current_environment()
        draft.git = GitRepositoryConfig.from_current_directory()
        return draft.finalize()

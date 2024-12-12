from __future__ import annotations

import torch


def is_bf16_supported_no_emulation():
    r"""Return a bool indicating if the current CUDA/ROCm device supports dtype bfloat16."""
    version = getattr(torch, "version")

    # Check for ROCm, if true return true, no ROCM_VERSION check required,
    # since it is supported on AMD GPU archs.
    if version.hip:
        return True

    device = torch.cuda.current_device()

    # Check for CUDA version and device compute capability.
    # This is a fast way to check for it.
    cuda_version = version.cuda
    if (
        cuda_version is not None
        and int(cuda_version.split(".")[0]) >= 11
        and torch.cuda.get_device_properties(device).major >= 8
    ):
        return True

    return False

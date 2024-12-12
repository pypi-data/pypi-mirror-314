from __future__ import annotations

import heapq
import logging
from typing import Any, Protocol, runtime_checkable

import numpy as np
import torch
import torch.distributed
from lightning_fabric.utilities.distributed import _DatasetSamplerWrapper
from torch.utils.data import BatchSampler, DistributedSampler
from typing_extensions import override

log = logging.getLogger(__name__)


def _all_gather(tensor: torch.Tensor, device: torch.device | None = None):
    gathered = [
        torch.zeros_like(tensor, device=device)
        for _ in range(torch.distributed.get_world_size())
    ]
    _ = torch.distributed.all_gather(gathered, tensor)
    return gathered


# @numba.njit
def _balanced_partition(sizes: np.ndarray, num_parts: int):
    """
    Greedily partition the given set by always inserting
    the largest element into the smallest partition.
    """
    sort_idx = np.argsort(-sizes)  # Sort in descending order
    heap = []
    for idx in sort_idx[:num_parts]:
        heap.append((sizes[idx], [idx]))
    heapq.heapify(heap)
    for idx in sort_idx[num_parts:]:
        smallest_part = heapq.heappop(heap)
        new_size = smallest_part[0] + sizes[idx]
        new_idx = smallest_part[1] + [idx]
        heapq.heappush(heap, (new_size, new_idx))
    idx_balanced = [part[1] for part in heap]
    return idx_balanced


@runtime_checkable
class DatasetWithSizes(Protocol):
    def data_sizes(self, indices: list[int]) -> np.ndarray: ...


@runtime_checkable
class DataSizesFunction(Protocol):
    def __call__(self, dataset: Any, indices: list[int]) -> np.ndarray: ...


class BalancedBatchSampler(BatchSampler):
    @staticmethod
    def _unwrap_dataset(dataset: Any):
        # Lightning's DistributedSampler wraps the dataset in a _DatasetSamplerWrapper,
        # so we need to unwrap it to get the actual dataset.
        if isinstance(dataset, _DatasetSamplerWrapper):
            if (data_source := getattr(dataset._sampler, "data_source", None)) is None:
                raise ValueError("Could not unwrap dataset from _DatasetSamplerWrapper")
            return data_source
        return dataset

    @property
    def distributed_sampler(self):
        if not isinstance(self.sampler, DistributedSampler):
            raise ValueError(
                f"Sampler must be a DistributedSampler, got {type(self.sampler)}"
            )
        return self.sampler

    def __init__(
        self,
        sampler: DistributedSampler,
        *,
        batch_size: int,
        device: torch.device,
        drop_last: bool = False,
        data_sizes_fn: DataSizesFunction | None = None,
    ):
        super().__init__(sampler, batch_size, drop_last=drop_last)

        # Validate the dataset
        dataset = self._unwrap_dataset(self.distributed_sampler.dataset)
        # Dataset much either implement `data_sizes`, or we need to provide a custom
        # implementation of the dataset sizes function.
        if isinstance(dataset, DatasetWithSizes):
            log.critical(f"BalancedBatchSampler: Resolved dataset to {type(dataset)}")

        elif self._data_sizes_fn is not None:
            log.critical("BalancedBatchSampler: Using custom data_sizes_fn")
        else:
            raise ValueError(
                "Dataset must implement the `data_sizes` method, "
                "or a custom data_sizes_fn must be provided "
                "to the BalancedBatchSampler."
            )

        self._device = device
        self._data_sizes_fn = data_sizes_fn

        log.info(
            f"Created BalancedBatchSampler with {sampler=}, {batch_size=}, {drop_last=}"
        )

    @staticmethod
    def _dist_enabled():
        return torch.distributed.is_available() and torch.distributed.is_initialized()

    def _dataset_sizes(self, indices: list[int]) -> np.ndarray:
        dataset = self._unwrap_dataset(self.distributed_sampler.dataset)
        # Dataset much either implement `data_sizes`, or we need to provide a custom
        # implementation of the dataset sizes function.
        if isinstance(dataset, DatasetWithSizes):
            return dataset.data_sizes(indices)

        if (data_sizes_fn := self._data_sizes_fn) is not None:
            return data_sizes_fn(dataset, indices)

        raise ValueError(
            "Dataset must implement the `data_sizes` method, "
            "or a custom data_sizes_fn must be provided "
            "to the BalancedBatchSampler."
        )

    @override
    def __iter__(self):
        if not self._dist_enabled():
            yield from super().__iter__()
            return

        for batch_idxs in super().__iter__():
            sizes = self._dataset_sizes(batch_idxs)
            idx_sizes = torch.stack(
                [
                    torch.tensor(batch_idxs, device=self._device),
                    torch.tensor(sizes, device=self._device),
                ]
            )
            idx_sizes_all = _all_gather(idx_sizes, device=self._device)
            idx_sizes_all = torch.cat(idx_sizes_all, dim=-1).cpu()
            idx_all = idx_sizes_all[0]
            sizes_all = idx_sizes_all[1]

            local_idx_balanced = _balanced_partition(
                sizes_all.numpy(), num_parts=self.distributed_sampler.num_replicas
            )
            # Since DistributedSampler pads the last batch
            # this should always have an entry for each replica.
            yield idx_all[local_idx_balanced[self.distributed_sampler.rank]].tolist()

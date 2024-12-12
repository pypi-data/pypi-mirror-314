"""
Module to handle workers for running tasks on
"""

from pathlib import Path

from pydantic import BaseModel

from iccore.filesystem import read_file_lines
from iccore.base_models import Range
from icsystemutils.cluster.node import ComputeNode
from icsystemutils.cpu import cpu_info


class Worker(BaseModel, frozen=True):
    """
    A worker or processor to run a task on. It has a unique identifier and
    an optional range of 'cores' that the task can run on.
    """

    id: int
    cores: Range


class Host(BaseModel, frozen=True):
    """
    A network location hosting workers, this can correspond to a cluster node
    or a single laptop
    """

    id: int
    node: ComputeNode
    workers: list[Worker] = []

    @property
    def address(self) -> str:
        return self.node.address


class TaskDistribution(BaseModel, frozen=True):
    """
    This is the task distribution on a host
    """

    cores_per_node: int = 0
    threads_per_core: int = 1
    cores_per_task: int = 1

    @property
    def num_procs(self) -> int:
        return int(self.cores_per_node / self.cores_per_task) * self.threads_per_core


def _get_core_range(proc_id: int, task_dist: TaskDistribution) -> Range:
    start = proc_id % task_dist.cores_per_node * task_dist.cores_per_task
    end = start + task_dist.cores_per_task - 1
    return Range(start=start, end=end)


def _get_runtime_task_dist(task_dist: TaskDistribution) -> TaskDistribution:
    if task_dist.cores_per_node == 0:
        cpu = cpu_info.read()
        cores_per_node = cpu.cores_per_node
        threads_per_core = cpu.threads_per_core
    else:
        cores_per_node = task_dist.cores_per_node
        threads_per_core = task_dist.threads_per_core

    return TaskDistribution(
        cores_per_node=cores_per_node,
        threads_per_core=threads_per_core,
        cores_per_task=task_dist.cores_per_task,
    )


def load(nodes: list[ComputeNode], task_dist: TaskDistribution) -> list[Host]:
    """
    Given a collection of available compute nodes and a task distribution
    set up the worker collection
    """

    task_dist = _get_runtime_task_dist(task_dist)
    return [
        Host(
            id=idx,
            node=node,
            workers=[
                Worker(
                    id=proc_id % task_dist.num_procs,
                    cores=_get_core_range(proc_id, task_dist),
                )
                for proc_id in range(task_dist.num_procs)
            ],
        )
        for idx, node in enumerate(nodes)
    ]


def read(path: Path, task_dist: TaskDistribution) -> list[Host]:
    """
    Read the node configuration from file and with the given task
    distribution create a collection of workers
    """
    return load(
        [ComputeNode(address=line) for line in read_file_lines(path)], task_dist
    )

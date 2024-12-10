"""
Module for session configuration
"""

import uuid

from pydantic import BaseModel

from .worker import TaskDistribution
from .scheduler.schedulers import slurm
from .scheduler.schedulers.slurm import SlurmJob
from .stopping_condition import StoppingCondition


class Config(BaseModel):
    """This is the configuration for a task running session

    :param str job_id: An identifier for the session,
    can be the Slurm job id for example.
    :param TaskDistribution task_dist: The distribution of tasks on
    available resources
    :param list[StroppingCondition] stopping_conditions: Conditions for the
    session to stop
    :param bool stop_on_error: Whether to stop on error
    :param str stdout_filename: The name of the stdout file
    :param str stderr_filename: The name of the stderr file
    :param SlurmJob slurm_job: An optional associated slurm job
    """

    job_id: str = ""
    task_dist: TaskDistribution = TaskDistribution(
        cores_per_node=0, threads_per_core=1, cores_per_task=1
    )
    stopping_conditions: list[StoppingCondition] = []
    stop_on_error: bool = True
    stdout_filename: str = "task_stdout.txt"
    stderr_filename: str = "task_stderr.txt"
    slurm_job: SlurmJob | None = None

    def model_post_init(self, __context):
        slurm_id = slurm.get_id()
        if not self.slurm_job and slurm_id:
            self.slurm_job = SlurmJob(id=slurm_id)

        if not self.job_id:
            if self.slurm_job:
                self.job_id = slurm_id
            else:
                self.job_id = str(uuid.uuid4().hex)

import shutil
import queue
from functools import partial

from iccore.test_utils import get_test_output_dir

import ictasks
import ictasks.task
from ictasks.task import Task


def test_basic_tasks_session():

    work_dir = get_test_output_dir()

    task_queue = queue.Queue()
    task_queue.put(Task(id="0", launch_cmd="echo 'hello from task 0'"))
    task_queue.put(Task(id="1", launch_cmd="echo 'hello from task 1'"))

    write_task_func = partial(ictasks.task.write, work_dir)

    ictasks.run(
        task_queue,
        work_dir,
        on_task_launched=write_task_func,
        on_task_completed=write_task_func,
    )

    shutil.rmtree(work_dir)


def test_function_tasks_session():

    work_dir = get_test_output_dir()
    write_task_func = partial(ictasks.task.write, work_dir)

    tasks = [
        Task(id="0", launch_func=write_task_func),
        Task(id="1", launch_func=write_task_func),
    ]

    ictasks.run_funcs(tasks)

    shutil.rmtree(work_dir)

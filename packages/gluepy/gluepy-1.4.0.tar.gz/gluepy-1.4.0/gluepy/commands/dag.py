import os
import logging
from typing import List, Optional
import time
import click
from gluepy.conf import default_context_manager, default_context
from gluepy.files.storages import default_storage
from gluepy.ops import default_mlops
from . import cli

logger = logging.getLogger(__name__)


@cli.command()
@click.option("--task", type=str)
@click.option("--from-task", type=str)
@click.option("--patch", "-p", type=str, multiple=True)
@click.option("--retry", type=str)
@click.argument("label")
def dag(
    label,
    retry: Optional[str] = None,
    patch: Optional[List[str]] = None,
    from_task: Optional[str] = None,
    task: Optional[str] = None,
):
    """Wrapper around run_dag function to expose to CLI"""
    run_dag(label, retry, patch, from_task, task)


def run_dag(
    label,
    retry: Optional[str] = None,
    patch: Optional[List[str]] = None,
    from_task: Optional[str] = None,
    task: Optional[str] = None,
):
    """Command to run a DAG by its label.

    Args:
        label (str): The label of the DAG to execute.
        retry (Optional[str], optional): Path to existing run_folder of a run to retry.
          Defaults to None.
        patch (Optional[List[str]], optional): Path to patch YAML file to override
            context with. Defaults to None.
        from_task (Optional[str], optional): Label of task in DAG to retry from.
            Defaults to None.
        task (Optional[str], optional): Label of task if only want to execute a
            single task in DAG. Defaults to None.

    """
    DAG = _get_dag_by_label(label)
    assert not (from_task and task), "Only one of --from-task or --task can be set."
    retry = retry if retry is None else retry.strip(default_storage.separator)

    if retry and default_storage.exists(os.path.join(retry, "context.yaml")):
        default_context_manager.load_context(
            os.path.join(retry, "context.yaml"), patches=list(patch)
        )
    elif retry:
        # Retry a run folder path that does not exist by creating it.
        default_context_manager.create_context(
            run_id=os.path.basename(retry),
            run_folder=retry,
            patches=list(patch) if patch else None,
            evaluate_lazy=True,
        )
    elif patch:
        default_context_manager.create_context(patches=list(patch), evaluate_lazy=True)

    tasks = DAG().inject_tasks()

    if task:
        tasks = [_get_task_by_label(task)]

    if from_task:
        Task = _get_task_by_label(from_task)
        for i, t in enumerate(tasks):
            if t is Task:
                pos = i
                break
        else:
            raise ValueError(f"Task '{from_task}' not found in DAG list of tasks.")
        tasks = tasks[pos:]

    default_mlops.create_run(dag=label, config=default_context.to_dict())

    for t in tasks:
        logger.info(f"---------- Started task '{t.__name__}'")
        time_start = time.time()
        t().run()
        time_end = time.time()
        logger.info(
            f"---------- Completed task '{t.__name__}' in "
            f"{'{:f}'.format(time_end-time_start)} seconds"
        )


def _get_dag_by_label(label):
    from gluepy.exec import DAG_REGISTRY

    try:
        DAG = DAG_REGISTRY[label]
    except KeyError:
        raise ValueError(f"DAG with label '{label}' was not found in registry.")

    return DAG


def _get_task_by_label(label):
    from gluepy.exec import TASK_REGISTRY

    try:
        Task = TASK_REGISTRY[label]
    except KeyError:
        raise ValueError(f"Task with label '{label}' was not found in registry.")

    return Task

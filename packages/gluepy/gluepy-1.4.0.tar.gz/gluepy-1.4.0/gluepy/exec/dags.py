from typing import List

from gluepy.exec.tasks import Task
from gluepy.utils.loading import import_string
from gluepy.conf import default_settings


class DAG:
    """Class that defines a pipeline or a 'directed acyclic graph'.

    The DAG itself contain minimum logic, and is only a grouping of a set
    of :ref:`tasks` instances that execute in a specific order combined
    with a set of configuration or options.

    Attributes:
        label (str): The label of this DAG is a descriptive label that is
            used to identify and run this DAG in future. Defaults to lowercase
            version of class name.
        extra_options (dict): Dictionary of additional options specific to this DAG.
        tasks (list): List of :ref:`tasks` instances to execute in a specific order.

    """

    label = None
    extra_options = {}
    tasks = []

    def __init__(self) -> None:
        self.label == self.label or self.__class__.__name__.lower()

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        label = cls.label or cls.__name__.lower()
        if label in REGISTRY:
            raise KeyError(
                f"Duplicate DAG label '{cls.label}' already exists in DAG REGISTRY"
            )
        REGISTRY[label] = cls

    def inject_tasks(self) -> List[Task]:
        """Inject all tasks including :setting:`START_TASK` to the final
        list of executable tasks of this DAG.

        Returns:
            List[Task]: Full list of tasks of DAG.
        """
        return [import_string(default_settings.START_TASK)] + self.tasks


REGISTRY = {}

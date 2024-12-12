import yaml
import logging
from io import StringIO
from gluepy.conf import default_context
from gluepy.files.storages import default_storage

logger = logging.getLogger(__name__)

REGISTRY = {}


class Task:
    """Class that represent a single step in a :ref:`dags`.

    Attributes:
        label (str): Name of the task used when calling the task.

    """

    label = None

    def __init__(self) -> None:
        self.label == self.label or self.__class__.__name__.lower()

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        label = cls.label or cls.__name__.lower()
        if label in REGISTRY:
            raise KeyError(
                f"Duplicate Task label '{cls.label}' already exists in Task REGISTRY"
            )
        REGISTRY[label] = cls

    def run(self):
        """Entrypoint of the Task.

        This is the method called when executing each step of the :ref:`dags`.

        Raises:
            NotImplementedError: Raise exeception if the child task have not yet
                implemented the entrypoint method.
        """
        raise NotImplementedError()


class BootstrapTask(Task):
    """Used by default as the START_TASK and injected in each DAG.

    Provide various bootstrapping functionality such as serializing context
    at start of execution.

    """

    label = "bootstraptask"

    def run(self):
        logger.debug(
            f"""
            Run ID: {default_context.gluepy.run_id}
            Run Folder: {default_context.gluepy.run_folder}
            """
        )
        default_storage.touch(
            default_storage.runpath("context.yaml"),
            StringIO(yaml.dump(default_context.to_dict())),
        )

import os
from typing import Any
from gluepy.utils.loading import LazyProxy, import_module, SingletonMixin


class Settings(SingletonMixin):
    """Gluepy settings object

    This singleton settings object captures all the current
    active settings of the project and execution. It will load all
    settings using the GLUEPY_SETTINGS_MODULE environment variable,
    which allow you to have multiple different setting files that
    can be loaded by configuring your environment.

    """

    BASE_DIR: str
    CONFIG_PATH: str
    INSTALLED_MODULES: list[str]
    STORAGE_BACKEND: str
    STORAGE_ROOT: str
    DATA_BACKEND: str
    CONTEXT_BACKEND: str
    START_TASK: str
    MLOPS_BACKEND: str
    AIRFLOW_DAG_PREFIX: str
    AIRFLOW_TEMPLATE: str
    AIRFLOW_IMAGE: str
    AIRFLOW_CONFIGMAPS: list[str]
    AIRFLOW_POD_RESOURCES: dict[str, dict]
    AIRFLOW_KUBERNETES_CONFIG: str
    LOGGING: dict[str, Any]

    def __init__(self, dotted_path: str, *args, **kwargs):
        module = import_module(dotted_path)
        for key in dir(module):
            if key.isupper():
                setattr(self, key, getattr(module, key))


default_settings = LazyProxy(lambda: Settings(os.environ.get("GLUEPY_SETTINGS_MODULE")))

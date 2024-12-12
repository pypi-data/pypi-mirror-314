import os
import uuid
import yaml
import logging
import re
from functools import reduce
from datetime import datetime
from typing import List, Optional
from box import Box
from gluepy.utils.loading import LazyProxy, import_string, SingletonMixin
from gluepy.utils.dict import merge
from gluepy.conf import default_settings

logger = logging.getLogger(__name__)


class Context(SingletonMixin):
    _data = Box()

    def __init__(self, data=None, *args, **kwargs):
        if data:
            self._data.clear()
            self._data.update(data)

    @property
    def instance(self):
        return self.__singleton_instance

    def __str__(self):
        return str(self._data)

    def __hash__(self):
        return hash(self._data)

    def __dir__(self):
        return dir(self._data)

    def __getattr__(self, attr):
        return getattr(self._data, attr)

    def __setattr__(self, name, value):
        raise TypeError(
            f"'{self.__class__.__name__}' object does not support item assignment"
        )


class DefaultContextManager:
    """
    Class responsible for populating the ``Context`` object that is
    later used by ``default_context``.

    The default context manager is populating the context object by reading
    in a set of YAML files located in the :setting:`CONFIG_PATH` directory.


    """

    def __init__(self) -> None:
        self._ctx = None

    def create_context(
        self,
        run_id: Optional[str] = None,
        run_folder: Optional[str] = None,
        patches: Optional[List[str]] = None,
        evaluate_lazy: bool = False,
    ):
        """Create a new context instance.

        Read in existing configuration files from :setting:`CONFIG_PATH` directory
        and patch them with any overrides from ``patches`` kwarg passed in.

        Also populates the ``meta`` key of the context with run meta data
        such as run_folder, run_id and created_at timestamp.

        """
        # Imported here to avoid circular import.
        from gluepy.files.storages import default_storage

        patches = patches or []
        if patches:
            for i, path in enumerate(patches):
                if not default_storage.exists(path):
                    logger.warning(f"Patch '{path}' was not found.")
                    patches[i] = dict()
                    continue

                patches[i] = yaml.load(
                    default_storage.open(path),
                    Loader=yaml.SafeLoader,
                )

        yamls = filter(
            lambda f: os.path.splitext(f)[1] in {".yaml", ".yml"},
            os.listdir(default_settings.CONFIG_PATH),
        )

        patches = [
            yaml.load(
                open(os.path.join(default_settings.CONFIG_PATH, y)),
                Loader=yaml.SafeLoader,
            )
            for y in yamls
        ] + patches

        patches += [self.get_run_meta(run_id=run_id, run_folder=run_folder)]

        ctx = Context(
            data=reduce(lambda config, patch: merge(config, patch), patches, {})
        )

        if evaluate_lazy:
            self._ctx = ctx
        return ctx

    def load_context(self, path: str, patches: Optional[List[str]] = None):
        """Loads an existing context.

        When we may want to recreate or rerun a pre-existing model execution,
        we may want to load the same context and parameters used by that pre-existing
        execution.

        This method reads in an existing file and applies a set of optional patches
        as overrides, and will reuse the same run_id, run_folder as is already
        defined in the pre-existing context YAML file passed in.

        """
        # Imported here to avoid circular import.
        from gluepy.files.storages import default_storage

        patches = patches or []
        # Reformat folder name to be valid.
        path_formatted = re.sub(r"[:\+\s]+", "-", os.path.dirname(path))
        path_formatted = re.sub(r"[^a-zA-Z0-9-_/\.]+", "", path_formatted)
        # Reconstrut the newly formatted dir path with the file name.
        path_formatted = os.path.join(path_formatted, os.path.basename(path))
        if path != path_formatted:
            logger.warning(
                f"Given run folder ('{path}') path was "
                f"reformatted into '{path_formatted}'"
            )

        if not default_storage.exists(path_formatted):
            self._ctx = self.create_context(
                run_id=(
                    os.path.dirname(path_formatted.rstrip(os.sep)).split(os.sep)[-1]
                    or str(uuid.uuid4())
                ),
                run_folder=os.path.dirname(path_formatted),
                patches=patches,
            )
            return self._ctx

        _, ext = os.path.splitext(path_formatted)
        if ext not in {".yaml", ".yml"}:
            raise ValueError(f"File path '{path_formatted}' is not a YAML file.")

        self._ctx = Context(
            yaml.load(default_storage.open(path_formatted), Loader=yaml.SafeLoader)
        )
        return self._ctx

    def get_run_meta(self, **kwargs):
        dt = datetime.utcnow()
        run_id = kwargs.get("run_id") or str(uuid.uuid4())
        run_folder = kwargs.get("run_folder") or os.path.join(
            f"runs/{dt.year}/{dt.month}/{dt.day}", run_id
        )
        return {
            "gluepy": {
                "run_id": run_id,
                "created_at": dt,
                "run_folder": run_folder,
            }
        }


default_context_manager = LazyProxy(
    lambda: import_string(default_settings.CONTEXT_BACKEND)()
)
default_context = LazyProxy(
    lambda: default_context_manager._ctx
    if default_context_manager._ctx
    else default_context_manager.create_context()
)

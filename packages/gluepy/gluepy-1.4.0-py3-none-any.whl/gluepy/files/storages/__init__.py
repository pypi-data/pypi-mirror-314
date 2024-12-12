# flake8: noqa
from gluepy.conf import default_settings
from gluepy.utils.loading import LazyProxy, import_string
from .base import BaseStorage


default_storage: BaseStorage = LazyProxy(
    lambda: import_string(default_settings.STORAGE_BACKEND)()
)

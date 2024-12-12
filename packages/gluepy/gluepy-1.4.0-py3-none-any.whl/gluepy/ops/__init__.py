# flake8: noqa
from gluepy.conf import default_settings
from gluepy.utils.loading import LazyProxy, import_string
from .backend import BaseOpsBackend


default_mlops: BaseOpsBackend = LazyProxy(
    lambda: import_string(default_settings.MLOPS_BACKEND)()
)

# flake8: noqa
from gluepy.conf import default_settings
from gluepy.utils.loading import LazyProxy, import_string
from .base import BaseDataManager
from .pandas import PandasDataManager


data_manager: BaseDataManager = LazyProxy(
    lambda: import_string(default_settings.DATA_BACKEND)()
)

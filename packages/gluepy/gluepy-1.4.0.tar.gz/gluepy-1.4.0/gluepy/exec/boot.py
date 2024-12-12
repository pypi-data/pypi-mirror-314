import logging.config
from gluepy.conf import default_settings
from gluepy.utils.loading import import_module


def bootstrap():
    if not hasattr(default_settings, "INSTALLED_MODULES"):
        return

    logging.config.dictConfig(default_settings.LOGGING)
    for module in default_settings.INSTALLED_MODULES:
        for pkg in {"tasks", "dags", "commands"}:
            pkg_path = ".".join([module, pkg])
            try:
                import_module(pkg_path)
            except ModuleNotFoundError as ex:
                # Only skip error if it is specifically raised due to
                # failing importing the requested pkg path.
                if pkg_path in str(ex.msg):
                    continue
                raise

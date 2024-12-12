import warnings
from pathlib import Path
from typing import Any

from raphson_mp import settings


def get_config_dict() -> dict[str, Any]:
    config: dict[str, Any] = {
        "version": 1,
        "formatters": {
            "detailed": {
                "format": "%(asctime)s [%(process)d:%(thread)d] [%(levelname)s] [%(name)s:%(module)s:%(lineno)s] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S %Z",
            },
            "default": {
                "format": "%(asctime)s %(levelname)s %(name)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S %Z",
            },
            "short": {
                "format": "%(asctime)s %(levelname)s %(name)s: %(message)s",
                "datefmt": "%H:%M:%S",
            },
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "short" if settings.log_short else "default",
            },
        },
        "root": {
            "level": settings.log_level,
            "handlers": ["stdout"],
        },
        "disable_existing_loggers": False,
    }

    if settings.log_warnings_to_file:
        config["root"]["handlers"].append("errors")
        error_log_path = Path(settings.data_dir, "errors.log")
        config["handlers"]["errors"] = {
            "class": "logging.FileHandler",
            "filename": error_log_path.absolute().as_posix(),
            "level": "WARNING",
            "formatter": "detailed",
        }

    return config


def apply() -> None:
    """
    Apply dictionary config
    """
    import logging.config  # pylint: disable=import-outside-toplevel
    warnings.simplefilter('always')
    logging.config.dictConfig(get_config_dict())


def apply_debug() -> None:
    settings.log_level = "DEBUG"
    apply()

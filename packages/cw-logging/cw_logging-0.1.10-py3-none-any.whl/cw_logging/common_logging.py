""" Simple package to implement a common logging interface for CLEARWINDOW python projects """

import functools
import logging
import logging.config
import os

from inspect import ismethod
from typing import Callable

COMMON_LOGS_DIR = os.environ.get(
    "PY_LOGS_DIR", os.path.expanduser("~/.python_logs")
)


LEVEL_FILTER_MAP = {
    logging.INFO: [logging.INFO, logging.WARNING],
    logging.ERROR: [logging.ERROR, logging.CRITICAL],
    logging.DEBUG: [logging.DEBUG],
}


class Global:
    """A global class to store the logger instance and other properties."""

    logger = None
    app_name = None


class LevelFilter(logging.Filter):
    """A logging filter to filter log records based on the log level"""

    def __init__(self, level: int) -> None:
        super().__init__()
        self.level = level

    def filter(self, record):
        return record.levelno in LEVEL_FILTER_MAP[self.level]


class GunicornErrorFilter(logging.Filter):
    """A logging filter to filter log records based on the log level"""

    def filter(self, record):
        return record.name == "gunicorn.error"


class GunicornAccessFilter(logging.Filter):
    """A logging filter to filter log records based on the log level"""

    def filter(self, record):
        return record.name == "gunicorn.access"


def configure_logger(app_name: str) -> logging.Logger:
    """Configure logging for the application.

    Args:
        app_name (str): The name of the application
    """
    LOGS_DIR = os.path.join(COMMON_LOGS_DIR, app_name)

    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "root": {"level": "INFO", "handlers": ["file", "console"]},
        "handlers": {
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "generic",
                "filename": os.path.join(LOGS_DIR, "app.log"),
                "maxBytes": 104857600,
            },
            "file_error": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "generic",
                "filename": os.path.join(LOGS_DIR, "error.log"),
                "maxBytes": 104857600,
                "filters": ["error_filter"],
            },
            "file_info": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "generic",
                "filename": os.path.join(LOGS_DIR, "info.log"),
                "maxBytes": 104857600,
                "filters": ["info_filter"],
            },
            "file_debug": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "generic",
                "filename": os.path.join(LOGS_DIR, "debug.log"),
                "maxBytes": 104857600,
                "filters": ["debug_filter"],
            },
            "file_gn_error": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "generic",
                "filename": os.path.join(LOGS_DIR, "gunicorn_error.log"),
                "maxBytes": 104857600,
                "filters": ["error_filter"],
            },
            "file_gn_access": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "generic",
                "filename": os.path.join(LOGS_DIR, "gunicorn_access.log"),
                "maxBytes": 104857600,
                "filters": ["info_filter"],
            },
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "generic",
                "stream": "ext://sys.stdout",
                "filters": ["info_filter"],
            },
            "console_error": {
                "class": "logging.StreamHandler",
                "level": "ERROR",
                "formatter": "generic",
                "stream": "ext://sys.stderr",
                "filters": ["error_filter"],
            },
            "console_debug": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "generic",
                "stream": "ext://sys.stdout",
                "filters": ["debug_filter"],
            },
        },
        "filters": {
            "info_filter": {"()": LevelFilter, "level": logging.INFO},
            "error_filter": {"()": LevelFilter, "level": logging.ERROR},
            "debug_filter": {"()": LevelFilter, "level": logging.DEBUG},
        },
        "loggers": {
            f"{app_name}": {
                "level": "INFO",
                "handlers": [
                    "file",
                    "console",
                    "console_error",
                    "console_debug",
                    "file_error",
                    "file_info",
                    "file_debug",
                ],
                "propagate": False,
            },
            "gunicorn.error": {
                "level": "ERROR",
                "handlers": ["file_gn_error"],
                "propagate": False,
            },
            "gunicorn.access": {
                "level": "DEBUG",
                "handlers": ["file_gn_access"],
                "propagate": False,
            },
        },
        "formatters": {
            "generic": {
                "format": "%(asctime)s [%(module)s] [%(levelname)s] %(message)s",
                "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
                "class": "logging.Formatter",
            },
        },
    }

    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)

    logging.config.dictConfig(log_config)
    Global.app_name = app_name
    Global.logger = logging.getLogger(app_name)
    return logging.getLogger(app_name)


def loggable(fn: Callable = None, *, level: int = logging.INFO):
    """A decorator that logs function calls, arguments, and return values."""
    if fn is None:
        return lambda fn: loggable(fn, level=level)

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        func_logger = logging.getLogger(Global.app_name)
        # Determine if the function is a method of a class
        # TODO: improve class detection, as this picks up things like int, str, etc.
        if len(args) > 0 and hasattr(args[0], "__class__") and ismethod(fn):
            # Function is a class method
            class_name = args[0].__class__.__name__
            method_name = f"{class_name}.{fn.__name__}"
            filtered_args = args[1:]  # Exclude 'self' from the arguments
        else:
            # Function is not a class method
            method_name = fn.__name__
            filtered_args = args

        # Log the function entry with arguments
        func_logger.log(
            level,
            "Entering %s with arguments: %s, %s",
            method_name,
            filtered_args,
            kwargs,
        )

        # Execute the function and capture the result
        result = fn(*args, **kwargs)

        # Log the function exit with the return value
        func_logger.log(
            level, "Exiting %s with return value: %s", method_name, result
        )

        return result

    return wrapper


if __name__ == "__main__":
    configure_logger("test")

    logger = logging.getLogger("gunicorn.error")

    @loggable
    def add(a: int, b: int) -> int:
        return a + b

    add(1, 2)
    logger.error("Test message")

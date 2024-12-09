""" Common package for logging. """

from cw_logging.common_logging import configure_logger, loggable
from cw_logging.base_logging import LoggableBase

configure_logging = configure_logger

__all__ = ["configure_logging", "configure_logger", "loggable", "LoggableBase"]

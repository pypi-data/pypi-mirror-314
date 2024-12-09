""" Common package for logging. """

from cw_logging.common_logging import configure_logger, loggable

configure_logging = configure_logger
__all__ = ["configure_logging", "configure_logger", "loggable"]

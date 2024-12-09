""" Module containing a base class to implement logging functions """

import logging


class LoggableBase:
    """Base class to implement logging functions"""

    def __init__(self, logger: logging.Logger | str | None = None) -> None:
        """Initialize the class with a logger instance"""
        if isinstance(logger, str):
            self.logger = logging.getLogger(logger)
        else:
            self.logger = logger or logging.getLogger()

    def debug(self, *args, **kwargs) -> None:
        """Log a debug message"""
        self.logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs) -> None:
        """Log an info message"""
        self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs) -> None:
        """Log a warning message"""
        self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs) -> None:
        """Log an error message"""
        self.logger.error(*args, **kwargs)

    def critical(self, *args, **kwargs) -> None:
        """Log a critical message"""
        self.logger.critical(*args, **kwargs)

    def exception(self, *args, **kwargs) -> None:
        """Log an exception message"""
        self.logger.exception(*args, **kwargs)

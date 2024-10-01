"""SSB logger module.

This module is designed to set up and manage logging within an application.
The SsbLogger is ment to be the top-level logger in the application, that receives
log messages from all other modules. It formats the messages in an uniform way and
directs the messages to the specified outputs (console, file, etc.).
"""

import logging
from collections.abc import Callable
from functools import wraps
from typing import Any
from typing import TypeVar

from colorlog import ColoredFormatter


class SsbLogger:
    """A logger class that facilitates logging to both console and file.

    This class sets up a logger with specified parameters, allowing for easy logging
    of messages with a consistent format. It provides a method to retrieve the
    configured logger instance for use in other parts of the application.
    """

    def __init__(
        self,
        log_level: int = logging.DEBUG,
        log_file: str = "app.log",
        name: str = "root",
    ) -> None:
        """Initialize the SsbLogger class.

        Args:
            name: The name of the logger. Defaults to 'root'.
            log_file: The file where logs will be written. Defaults to 'app.log'.
            log_level: The logging level. Defaults to logging.DEBUG.
        """
        # Create a logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # Create handlers
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")

        fmt = "{asctime} [{levelname:^8}] - {message} < {module}.{funcName}#L{lineno}"
        colored_fmt = "{log_color}" + fmt
        datefmt = "%Y-%m-%dT%H:%M:%S%z"  # ISO 8601

        iso_formatter = logging.Formatter(fmt, datefmt=datefmt, style="{")
        colored_iso_formatter = ColoredFormatter(
            colored_fmt, datefmt=datefmt, style="{"
        )

        console_handler.setFormatter(colored_iso_formatter)
        file_handler.setFormatter(iso_formatter)

        # Add handlers to the logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        """Returns the configured logger instance."""
        return self.logger


# Type variable to represent any function signature
F = TypeVar("F", bound=Callable[..., Any])


def log_function_enter_exit(func: F) -> F:
    """Decorator that logs the entry and exit of a function."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logging.info(f"-> Entering {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"<- Exiting {func.__name__} with result: {result}")
        return result

    return wrapper

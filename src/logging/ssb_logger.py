"""SSB logger module.

This module is designed to set up and manage logging within an application.
The SsbLogger is ment to be the top-level logger in the application, that receives
log messages from all other modules. It formats the messages in a uniform way and
directs the messages to the specified outputs (console, file, etc.).
"""

import json
import logging
from collections.abc import Callable
from functools import wraps
from pathlib import Path
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
        log_file: str | Path = "app.log",
        name: str = "root",
        jsonl=False,
    ) -> None:
        """Initialize the SsbLogger class.

        Args:
            log_level: The logging level. Defaults to logging.DEBUG.
            log_file: The file where logs will be written. Defaults to 'app.log'.
            name: The name of the logger. Defaults to 'root'.
            jsonl: If a jsonl handler should be added or not. Default to False.
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

        if jsonl:
            jsonl_filename = Path(log_file).with_suffix(".jsonl")
            jsonl_handler = logging.FileHandler(
                jsonl_filename, mode="a", encoding="utf-8"
            )
            jsonl_formatter = JsonlFormatter(datefmt=datefmt)
            jsonl_handler.setFormatter(jsonl_formatter)
            self.logger.addHandler(jsonl_handler)

    def get_logger(self):
        """Returns the configured logger instance."""
        return self.logger


class JsonlFormatter(logging.Formatter):
    """Handles the formatting of log records into JSON Lines format.

    This class formats log records into JSON Lines format. Basic
    log information like time, level, and message are included in the
    formatted output.

    Additionally, if the log record has extra data defined in a 'data' attribute,
    it integrates it into the JSON log record. This formatter is particularly
    useful for structured logging or log aggregation systems that consume JSON logs.

    Example:
        >>> example_data = {"event": "user_login", "user_id": 123, "success": True}
        >>> logger.info("Logging example data", extra={"data": example_data})
    """

    def format(self, record):
        log_record = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        # Add additional fields from record if needed
        if hasattr(record, "data"):
            log_record.update(record.data)
        return json.dumps(log_record)


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

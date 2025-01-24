"""SSB logger module.

This module is designed to set up and manage logging within an application.
The StatLogger is meant to be the root-level logger in the application, that receives
log messages from all other modules. It formats the messages in a uniform way and
directs the messages to the specified outputs (console, file, etc.).
"""

from __future__ import annotations

import json
import logging
from collections.abc import Callable
from functools import wraps
from logging.handlers import RotatingFileHandler
from pathlib import Path
from threading import Lock
from typing import Any
from typing import TypeVar

from colorlog import ColoredFormatter


class SingletonMeta(type):
    """A thread-safe implementation of the Singleton pattern.

    By using this as a class's metaclass, we ensure that there is only one instance
    of the class.
    """

    _instance = None
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            # Double-checked locking pattern
            with cls._lock:
                if cls._instance is None:
                    instance = super().__call__(*args, **kwargs)
                    cls._instance = instance
        return cls._instance


class StatLogger(metaclass=SingletonMeta):
    """A root logger class that facilitates logging to console and files.

    This class is meant to be the root-level logger in an application, that receives
    log messages from all other modules. It formats the messages in a uniform way and
    directs the messages to the specified outputs (console, file, etc.)

    There is only one instance of this class, ensured by a singelton pattern
    implementation.
    """

    LOG_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"  # ISO 8601
    LOG_FORMAT = "{asctime} {levelname:^8} {message} < {module}.{funcName} #L{lineno}"
    COLORED_LOG_FORMAT = "{log_color}" + LOG_FORMAT

    # File handler constants
    FILE_HANDLER_MAX_BYTES = 1_000_000  # 1MB
    FILE_HANDLER_BACKUP_COUNT = 5

    def __init__(
        self,
        log_level: int = logging.DEBUG,
        log_file: str | Path = "app.log",
        jsonl: bool = False,
    ) -> None:
        """Initialize the StatLogger class.

        Args:
            log_level: The logging level. Defaults to logging.DEBUG.
            log_file: The file where logs will be written. Defaults to 'app.log'.
            jsonl: If a jsonl handler should be added or not. Default to False.
        """
        # Create a logger
        self.logger = logging.getLogger()  # root logger
        self.logger.setLevel(log_level)

        iso_formatter = logging.Formatter(
            self.LOG_FORMAT, datefmt=self.LOG_DATE_FORMAT, style="{"
        )
        colored_iso_formatter = ColoredFormatter(
            self.COLORED_LOG_FORMAT, datefmt=self.LOG_DATE_FORMAT, style="{"
        )

        self._add_console_logger(colored_iso_formatter)
        self._add_file_logger(iso_formatter, log_file)
        if jsonl:
            self._add_jsonl_logger(log_file)

    def _add_console_logger(self, formatter: logging.Formatter) -> None:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def _add_file_logger(
        self, formatter: logging.Formatter, log_file: str | Path
    ) -> None:
        file_handler = self._create_rotating_file_handler(log_file, formatter)
        self.logger.addHandler(file_handler)

    def _add_jsonl_logger(self, log_file: str | Path) -> None:
        jsonl_formatter = JsonlFormatter(datefmt=self.LOG_DATE_FORMAT)
        jsonl_filename = Path(log_file).with_suffix(".jsonl")
        jsonl_handler = self._create_rotating_file_handler(
            jsonl_filename, jsonl_formatter
        )
        self.logger.addHandler(jsonl_handler)

    def _create_rotating_file_handler(
        self,
        file_path: str | Path,
        formatter: logging.Formatter,
        max_bytes: int = FILE_HANDLER_MAX_BYTES,
        backup_count: int = FILE_HANDLER_BACKUP_COUNT,
    ) -> RotatingFileHandler:
        """Helper function to create a RotatingFileHandler with standard settings."""
        handler = RotatingFileHandler(
            file_path,
            mode="a",
            encoding="utf-8",
            maxBytes=max_bytes,
            backupCount=backup_count,
        )
        handler.setFormatter(formatter)
        return handler

    def get_logger(self):
        """Returns the configured logger instance."""
        return self.logger

    @classmethod
    def _reset_instance(cls) -> None:
        """Resets the Singleton instance for testing purposes."""
        with cls._lock:
            cls._instance = None


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

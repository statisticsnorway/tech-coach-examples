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
from collections.abc import Iterable
from enum import Enum
from functools import wraps
from logging.handlers import RotatingFileHandler
from pathlib import Path
from threading import Lock
from typing import Any
from typing import Literal
from typing import TypeVar
from typing import cast

from colorlog import ColoredFormatter


class LoggerType(str, Enum):
    """Represents the types of loggers you can add to `StatLogger`.

    Attributes:
        CONSOLE: A logger that writes colored logs to the console.
        FILE: A logger that writes logs to a file in the same format as the CONSOLE logger.
        JSONL: A logger that writes logs in JSON Lines format, including
               message, timestamp, severity level and an optional extra field.
        JSONL_EXTRA_ONLY: A logger that writes only information from the extra field
            information in JSON Lines format. Used for logging process and quality data.
    """

    CONSOLE = "console"
    FILE = "file"
    JSONL = "jsonl"
    JSONL_EXTRA_ONLY = "jsonl_extra_only"


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


class NoEmptyExtraLogsFilter(logging.Filter):
    """Filter to exclude log messages that would produce empty JSON."""

    def filter(self, record: logging.LogRecord) -> bool:
        # Reject records without an extra data field
        return bool(record.data) if hasattr(record, "data") else False


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
        loggers: Iterable[LoggerType] = (LoggerType.CONSOLE, LoggerType.FILE),
    ) -> None:
        """Initialize the StatLogger class.

        Args:
            log_level: The logging level. Defaults to logging.DEBUG.
            log_file: The file where logs will be written. Defaults to 'app.log'.
            loggers: Optional list of `LoggerType`s that should be added. Defaults to
            LoggerType.CONSOLE and LoggerType.FILE.

        Raises:
            TypeError: If not all loggers have type LoggerType.
        """
        if not all(isinstance(logger, LoggerType) for logger in loggers):
            raise TypeError("All loggers must be of type LoggerType.")

        # Create a logger
        self.logger = logging.getLogger()  # root logger
        self.logger.setLevel(log_level)

        iso_formatter = logging.Formatter(
            self.LOG_FORMAT, datefmt=self.LOG_DATE_FORMAT, style="{"
        )
        colored_iso_formatter = ColoredFormatter(
            self.COLORED_LOG_FORMAT, datefmt=self.LOG_DATE_FORMAT, style="{"
        )

        if LoggerType.CONSOLE in loggers:
            self._add_console_logger(colored_iso_formatter)
        if LoggerType.FILE in loggers:
            self._add_file_logger(iso_formatter, log_file)
        if LoggerType.JSONL in loggers:
            self._add_jsonl_logger(log_file, extra_only=False)
        if LoggerType.JSONL_EXTRA_ONLY in loggers:
            self._add_jsonl_logger(log_file, extra_only=True)

    def _add_console_logger(self, formatter: logging.Formatter) -> None:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def _add_file_logger(
        self, formatter: logging.Formatter, log_file: str | Path
    ) -> None:
        file_handler = self._create_rotating_file_handler(log_file, formatter)
        self.logger.addHandler(file_handler)

    def _add_jsonl_logger(self, log_file: str | Path, extra_only: bool) -> None:
        jsonl_formatter = JsonlFormatter(
            datefmt=self.LOG_DATE_FORMAT, extra_only=extra_only
        )
        jsonl_filename = Path(log_file).with_suffix(".jsonl")
        jsonl_handler = self._create_rotating_file_handler(
            jsonl_filename, jsonl_formatter
        )
        if extra_only:
            jsonl_handler.addFilter(NoEmptyExtraLogsFilter())
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

    def getLogger(self) -> logging.Logger:
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
        >>> logger = logging.getLogger(__name__)
        >>> example_data = {"event": "user_login", "user_id": 123, "success": True}
        >>> logger.info("Logging example data", extra={"data": example_data})
    """

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        style: Literal["%", "{", "$"] = "%",
        extra_only: bool = False,
    ) -> None:
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self.extra_only = extra_only

    def format(self, record: logging.LogRecord) -> str:
        if not self.extra_only:
            log_record = {
                "time": self.formatTime(record, self.datefmt),
                "level": record.levelname,
                "message": record.getMessage(),
            }
        else:
            log_record = {}
        # Add additional fields from record if needed
        if hasattr(record, "data"):
            log_record |= record.data

        return json.dumps(log_record) if log_record else ""


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

    return cast(F, wrapper)

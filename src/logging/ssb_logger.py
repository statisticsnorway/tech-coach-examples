import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from colorlog import ColoredFormatter


# Create a custom formatter with Oslo timezone
class OsloTzFormatter(logging.Formatter):
    """Custom logging formatter that formats log timestamps in the Oslo timezone."""

    def formatTime(self, record: logging.LogRecord, datefmt: str | None = None) -> str:
        # Convert the created time to a datetime object in Oslo timezone
        dt = datetime.fromtimestamp(record.created, tz=ZoneInfo("Europe/Oslo"))
        return dt.strftime(datefmt) if datefmt else dt.isoformat()


class ColoredOsloTzFormatter(ColoredFormatter, OsloTzFormatter):
    pass


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
        style = "{"
        datefmt = "%Y-%m-%d %H:%M:%S %Z(%z)"

        oslo_tz_formatter = OsloTzFormatter(fmt, style=style, datefmt=datefmt)
        colored_oslo_tz_formatter = ColoredOsloTzFormatter(
            colored_fmt, style=style, datefmt=datefmt
        )
        console_handler.setFormatter(colored_oslo_tz_formatter)
        file_handler.setFormatter(oslo_tz_formatter)

        # Add handlers to the logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        """Returns the configured logger instance."""
        return self.logger

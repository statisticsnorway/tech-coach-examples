import logging


class SsbLogger:
    """A logger class that facilitates logging to both console and file.

    This class sets up a logger with specified parameters, allowing for easy logging of messages with a consistent format. It provides a method to retrieve the configured logger instance for use in other parts of the application.

    Args:
        name: The name of the logger. Defaults to "root".
        log_file: The file where logs will be written. Defaults to "app.log".
        log_level: The logging level. Defaults to logging.DEBUG.

    Methods:
        get_logger(): Returns the configured logger instance.
    """

    def __init__(
        self,
        name: str = "root",
        log_file: str = "app.log",
        log_level: int = logging.DEBUG,
        time_zone: str = "Europe/Oslo",
    ) -> None:
        # Create a logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # Create handlers
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")

        # Create a formatter and set it for both handlers
        formatter = logging.Formatter(
            "{asctime} - {module} - {levelname} - {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add handlers to the logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger

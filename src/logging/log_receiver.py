"""Log receiver module.

This module is designed to set up and manage logging within an application.
It is ment to be the top-level logger in the application, that receives log messages
from all other modules. It formats the messages in an uniform way and directs the
messages to the specified outputs (console, file, google cloud log).

Todo:
    * Check https://github.com/statisticsnorway/ssb-timeseries/blob/main/src/ssb_timeseries/logging.py
    * Use a class for setting up the configuration to remove boilerplate code for the end user.
    * Add decorator for function enter-exit logging?
    * Decide time format for output (UTC?, local time? Number of decimals?)
"""

import logging

from log_sender import function_with_logging


# Create a root logger to things like formatting for all loggers
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")

formatter = logging.Formatter(
    "{asctime} - {module} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


def main() -> None:
    logger.info("-> Enter main()")
    function_with_logging()
    logger.info("<- Exit main()")


if __name__ == "__main__":
    main()

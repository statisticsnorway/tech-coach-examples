"""Log receiver module.

This module is designed to set up and manage logging within an application.
It is ment to be the top-level logger in the application, that receives log messages
from all other modules. It formats the messages in an uniform way and directs the
messages to the specified outputs (console, file, google cloud log).

Todo:
    * Check https://github.com/statisticsnorway/ssb-timeseries/blob/main/src/ssb_timeseries/logging.py
    * Add decorator for function enter-exit logging?
    * Decide time format for output (UTC?, local time? Number of decimals?)
"""

from log_sender import function_with_logging
from ssb_logger import SsbLogger


logger = SsbLogger().get_logger()


def main() -> None:
    logger.info("Enter main()")
    function_with_logging()
    logger.debug("Debug message")
    logger.error("Error message")
    logger.info("Exit main()")


if __name__ == "__main__":
    main()

"""This module demonstrates how to write log statements in ordinary code.

In the top-level module, the root where you run the code, you need to add an instance
of the StatLogger class to receive and print the log messages.
"""

import logging


logger = logging.getLogger(__name__)


def function_with_logging(a: str, b: str) -> None:
    logger.warning("Warning from function_with_logging!")

    # Use %-style formatting when logging in order to get lazy formatting.
    # Then the string is only formatted if the log message is actually emitted
    logger.debug("The arguments are %s and %s", a, b)

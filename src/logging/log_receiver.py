"""Log receiver module.

This module demonstrates use of the SsbLogger class to set up and manage logging within
an application. It is ment to be the top-level logger in the application, that receives
log messages from all other modules. Each Jupyter Notebook that you "run" and want
logs from should have one instance of the SsbLogger class.

Todo:
    * Check https://github.com/statisticsnorway/ssb-timeseries/blob/main/src/ssb_timeseries/logging.py
"""

import log_sender
from ssb_logger import SsbLogger
from ssb_logger import log_function_enter_exit


logger = SsbLogger().get_logger()


@log_function_enter_exit
def my_local_function(a: int, b: int) -> int:
    product = a * b
    logger.debug("The product is %d", product)
    return product


def main() -> None:
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    log_sender.function_with_logging("Hello", "World")
    product = my_local_function(2, 3)
    print(f"The product is: {product}")


if __name__ == "__main__":
    main()

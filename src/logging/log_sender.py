import logging


logger = logging.getLogger(__name__)


def function_with_logging() -> None:
    logger.info("-> Enter function_with_logging()")
    logger.warning("Warning from function_with_logging!")
    logger.info("<- Exit function_with_logging()")

import logging

from log_sender import function_with_logging


# Create a root logger to things like formatting for all loggers
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")

formatter = logging.Formatter(
    "{asctime} - {module: <12} - {levelname: <8} - {message}",
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

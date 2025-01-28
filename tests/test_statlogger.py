import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import pytest

from src.logging.statlogger import LoggerType
from src.logging.statlogger import StatLogger


@pytest.fixture(autouse=True)
def reset_ssb_logger() -> None:
    """Reset the StatLogger for each test. Necessary because it is a singelton object."""
    StatLogger._reset_instance()


class TestStatLogger:

    # Initialize logger with default parameters and verify console and file handlers are created
    def test_init_default_parameters(self, tmp_path) -> None:
        # Arrange
        log_file = tmp_path / "app.log"

        # pytest add its own handlers to the root logger, need to account for that
        previous_handlers = len(logging.getLogger().handlers)

        # Act
        logger = StatLogger(log_file=log_file)

        # Assert
        handlers = logger.logger.handlers
        assert len(handlers) == previous_handlers + 2
        assert isinstance(handlers[previous_handlers], logging.StreamHandler)
        assert isinstance(handlers[previous_handlers + 1], RotatingFileHandler)
        assert handlers[previous_handlers + 1].baseFilename == str(log_file)
        assert logger.logger.level == logging.DEBUG

    # Verify log messages are written to both console and file with correct format
    def test_log_messages_written_to_console_and_file(self, tmp_path, caplog) -> None:
        # Arrange
        log_file = tmp_path / "app.log"
        StatLogger(log_file=log_file)
        test_message = "Test log message"

        # Act
        logging.getLogger(__file__).info(test_message)

        # Assert
        # Check console output
        console_output = caplog.text
        assert test_message in console_output

        # Check file output
        with open(log_file) as f:
            file_content = f.read()
            assert test_message in file_content

    # Test that only one instance of StatLogger is created (Singelton pattern)
    def test_multiple_instances(self, tmp_path) -> None:
        # Arrange
        log_file = tmp_path / "app.log"

        # Act
        logger1 = StatLogger(log_file=log_file)
        logger2 = StatLogger(log_file=log_file)

        # Assert
        assert logger2 is logger1

    # JSONL logging creates separate file with JSON formatted logs when enabled
    def test_jsonl_logging_creates_separate_file(self, tmp_path, caplog) -> None:

        # Initialize StatLogger with jsonl enabled
        log_file = Path(tmp_path) / "app.log"
        StatLogger(loggers=[LoggerType.JSONL], log_file=log_file)
        test_message = "Test log message"

        # Act
        # with caplog.at_level(logging.ERROR):
        logging.getLogger(__file__).info(test_message)

        # Check file output
        jsonl_file = log_file.with_suffix(".jsonl")
        with open(jsonl_file) as file:
            jsonl_list = list(file)
            assert len(jsonl_list) == 1
            json_result = json.loads(jsonl_list[0])
            assert json_result["message"] == test_message

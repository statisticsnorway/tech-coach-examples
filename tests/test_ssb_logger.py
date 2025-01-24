from src.logging.ssb_logger import SsbLogger
from logging.handlers import RotatingFileHandler
import logging


class TestSsbLogger:

    # Initialize logger with default parameters and verify console and file handlers are created
    def test_init_default_parameters(self, tmp_path):
        # Arrange
        log_file = tmp_path / "app.log"
        log_file2 = tmp_path / "app2.log"

        # pytest add its own handlers to the root logger, need to account for that
        previous_handlers = len(logging.getLogger().handlers)

        # Act
        logger = SsbLogger(log_file=log_file)
        logger2 = SsbLogger(log_file=log_file2)

        # Assert
        handlers = logger.logger.handlers
        assert len(handlers) == previous_handlers + 2
        assert isinstance(handlers[previous_handlers], logging.StreamHandler)
        assert isinstance(handlers[previous_handlers + 1], RotatingFileHandler)
        assert handlers[previous_handlers + 1].baseFilename == str(log_file)
        assert logger.logger.level == logging.DEBUG

    # Verify log messages are written to both console and file with correct format
    def test_log_messages_written_to_console_and_file(self, tmp_path, caplog):
        # Arrange
        log_file = tmp_path / "app.log"
        logger = SsbLogger(log_file=log_file)
        test_message = "Test log message"

        # Act
        logger.get_logger().info(test_message)

        # Assert
        # Check console output
        console_output = caplog.text
        assert test_message in console_output

        # Check file output
        with open(log_file, "r") as f:
            file_content = f.read()
            assert test_message in file_content

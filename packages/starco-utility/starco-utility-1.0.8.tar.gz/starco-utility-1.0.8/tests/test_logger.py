import pytest
import logging
import os
from utility.logger import Logger
from unittest.mock import patch, MagicMock

@pytest.fixture
def test_logger():
    return Logger("test_logger", alert=False)

@pytest.fixture
def alert_logger():
    return Logger("alert_logger", alert=True)

def test_logger_initialization(test_logger):
    assert isinstance(test_logger, Logger)
    assert test_logger.name == "test_logger"
    assert test_logger.level == logging.DEBUG
    assert test_logger.alert is False
    assert len(test_logger.handlers) == 2  # File and console handlers

def test_logger_file_creation(test_logger):
    log_file = f"{test_logger.name}.log"
    assert os.path.exists(log_file)
    os.remove(log_file)  # Cleanup

def test_logging_levels(test_logger):
    with patch.object(test_logger, '_log_with_telegram') as mock_log:
        test_logger.debug("Debug message")
        mock_log.assert_called_with(logging.ERROR, "Debug message", exc_info=True)
        
        test_logger.info("Info message")
        mock_log.assert_called_with(logging.INFO, "Info message")
        
        test_logger.warning("Warning message")
        mock_log.assert_called_with(logging.WARNING, "Warning message")
        

def test_telegram_alert_disabled(test_logger):
    result = test_logger.send_telegram_message("Test message")
    assert result is False

@patch('requests.post')
def test_telegram_alert_enabled(mock_post, alert_logger):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response
    
    result = alert_logger.send_telegram_message("Test message")
    assert result is True
    mock_post.assert_called_once()

def test_alert_level_include():
    logger = Logger("test", alert=True, alert_log_level_inclue=[logging.ERROR])
    with patch.object(logger, 'send_telegram_message') as mock_send:
        logger.info("This shouldn't trigger alert")
        mock_send.assert_not_called()
        
        logger.error("This should trigger alert")
        mock_send.assert_called_once()

def test_alert_level_exclude():
    logger = Logger("test", alert=True, alert_log_level_exclude=[logging.INFO])
    with patch.object(logger, 'send_telegram_message') as mock_send:
        logger.info("This shouldn't trigger alert")
        mock_send.assert_not_called()
        
        logger.error("This should trigger alert")
        mock_send.assert_called_once()

def test_exception_logging(test_logger):
    with patch.object(test_logger, '_log_with_telegram') as mock_log:
        try:
            raise ValueError("Test exception")
        except ValueError:
            test_logger.error("Error occurred")
            mock_log.assert_called_once()
            args, kwargs = mock_log.call_args
            assert kwargs.get('exc_info') is True

import pytest
import logging
import os
from unittest.mock import patch, MagicMock
from utility.logger import Logger

@pytest.fixture
def mock_logger():
    return Logger("test_logger", alert=False)

@pytest.fixture
def mock_telegram_logger():
    return Logger("test_telegram", 
                 alert=True,
                 bot_token="test_token",
                 chat_id="test_chat_id")

def test_logger_initialization(mock_logger):
    assert mock_logger.name == "test_logger"
    assert mock_logger.level == logging.DEBUG
    assert mock_logger.alert is False
    assert len(mock_logger.handlers) == 2  # File and console handlers

def test_logger_file_creation(mock_logger):
    assert os.path.exists("test_logger.log")
    os.remove("test_logger.log")  # Cleanup

@patch('requests.post')
def test_send_telegram_message_success(mock_post, mock_telegram_logger):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response
    
    result = mock_telegram_logger.send_telegram_message("Test message")
    assert result is True
    mock_post.assert_called_once()

@patch('requests.post')
def test_send_telegram_message_failure(mock_post, mock_telegram_logger):
    mock_post.side_effect = Exception("Network error")
    
    result = mock_telegram_logger.send_telegram_message("Test message")
    assert result is False

def test_logging_levels(mock_logger):
    with patch.object(mock_logger, '_log_with_telegram') as mock_log:
        mock_logger.debug("Debug message")
        mock_log.assert_called_with(logging.DEBUG, "Debug message")
        
        mock_logger.info("Info message")
        mock_log.assert_called_with(logging.INFO, "Info message")
        
        mock_logger.warning("Warning message")
        mock_log.assert_called_with(logging.WARNING, "Warning message")
        
        # mock_logger.error("Error message")
        # mock_log.assert_called_with(logging.ERROR, "Error message")
        
        # mock_logger.critical("Critical message")
        # mock_log.assert_called_with(logging.CRITICAL, "Critical message")

def test_alert_level_include():
    logger = Logger("test_include", 
                   alert=True,
                   alert_log_level_inclue=[logging.ERROR, logging.CRITICAL])
    
    with patch.object(logger, 'send_telegram_message') as mock_send:
        logger.info("Should not alert")
        mock_send.assert_not_called()
        
        logger.error("Should alert")
        mock_send.assert_called()

def test_alert_level_exclude():
    logger = Logger("test_exclude", 
                   alert=True,
                   alert_log_level_exclude=[logging.INFO, logging.DEBUG])
    
    with patch.object(logger, 'send_telegram_message') as mock_send:
        logger.info("Should not alert")
        mock_send.assert_not_called()
        
        logger.critical("Should alert")
        mock_send.assert_called()

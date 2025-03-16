"""Tests for the logging configuration system."""

import os
import logging
import pytest
import pathlib
from unittest.mock import patch
from calculator.logging_config import LoggingConfig, get_logger


@pytest.fixture
def reset_logging():
    """Fixture to reset logging configuration after each test."""
    # Store original environment variables
    original_env = {}
    for key in ['CALCULATOR_LOG_LEVEL', 'CALCULATOR_LOG_DEST', 'CALCULATOR_LOG_FILE',
                'CALCULATOR_LOG_MAX_BYTES', 'CALCULATOR_LOG_BACKUP_COUNT']:
        original_env[key] = os.environ.get(key)
    
    yield
    
    # Restore original environment variables
    for key, value in original_env.items():
        if value is None:
            if key in os.environ:
                del os.environ[key]
        else:
            os.environ[key] = value
    
    # Reset the singleton instance
    LoggingConfig._instance = None
    
    # Reset the root logger
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)


def test_singleton_pattern():
    """Test that LoggingConfig implements the singleton pattern."""
    # Get two instances
    instance1 = LoggingConfig()
    instance2 = LoggingConfig()
    
    # Verify they are the same instance
    assert instance1 is instance2


@patch.dict(os.environ, {"CALCULATOR_LOG_LEVEL": ""}, clear=True)
def test_default_log_level(reset_logging):
    """Test default log level is INFO."""
    # Create a new instance
    LoggingConfig()
    
    # Verify root logger level is INFO
    assert logging.getLogger().level == logging.INFO


@patch.dict(os.environ, {"CALCULATOR_LOG_LEVEL": "DEBUG"}, clear=True)
def test_custom_log_level(reset_logging):
    """Test setting custom log level."""
    # Create a new instance
    LoggingConfig()
    
    # Verify root logger level is DEBUG
    assert logging.getLogger().level == logging.DEBUG


@patch.dict(os.environ, {"CALCULATOR_LOG_DEST": ""}, clear=True)
def test_default_log_destination(reset_logging):
    """Test default log destination is file."""
    # Create a new instance
    LoggingConfig()
    
    # Verify handler is FileHandler
    root_logger = logging.getLogger()
    assert len(root_logger.handlers) == 1
    assert isinstance(root_logger.handlers[0], logging.FileHandler)


@patch.dict(os.environ, {"CALCULATOR_LOG_DEST": "console"}, clear=True)
def test_console_log_destination(reset_logging):
    """Test console log destination."""
    # Create a new instance
    LoggingConfig()
    
    # Verify handler is StreamHandler
    root_logger = logging.getLogger()
    assert len(root_logger.handlers) == 1
    assert isinstance(root_logger.handlers[0], logging.StreamHandler)


@patch.dict(os.environ, {
    "CALCULATOR_LOG_DEST": "file",
    "CALCULATOR_LOG_FILE": "test_log.log"
}, clear=True)
def test_file_log_destination(reset_logging):
    """Test file log destination."""
    test_log_file = "test_log.log"
    
    try:
        # Create a new instance
        LoggingConfig()
        
        # Verify handler is FileHandler
        root_logger = logging.getLogger()
        assert len(root_logger.handlers) == 1
        assert isinstance(root_logger.handlers[0], logging.FileHandler)
        
        # Log a test message
        logger = get_logger('test_logger')
        logger.info('Test message')
        
        # Verify log file exists and contains the message
        assert os.path.exists(test_log_file)
        with open(test_log_file, 'r') as f:
            content = f.read()
            assert 'Test message' in content
    finally:
        # Clean up
        if os.path.exists(test_log_file):
            os.remove(test_log_file)


@patch.dict(os.environ, {
    "CALCULATOR_LOG_DEST": "rotating_file",
    "CALCULATOR_LOG_FILE": "test_rotating_log.log",
    "CALCULATOR_LOG_MAX_BYTES": "1024",
    "CALCULATOR_LOG_BACKUP_COUNT": "3"
}, clear=True)
def test_rotating_file_log_destination(reset_logging):
    """Test rotating file log destination."""
    test_log_file = "test_rotating_log.log"
    
    try:
        # Create a new instance
        LoggingConfig()
        
        # Verify handler is RotatingFileHandler
        root_logger = logging.getLogger()
        assert len(root_logger.handlers) == 1
        assert isinstance(root_logger.handlers[0], logging.handlers.RotatingFileHandler)
        
        # Verify handler properties
        handler = root_logger.handlers[0]
        assert handler.maxBytes == 1024
        assert handler.backupCount == 3
    finally:
        # Clean up
        if os.path.exists(test_log_file):
            os.remove(test_log_file)


def test_get_logger_function():
    """Test the get_logger convenience function."""
    # Get a logger
    logger = get_logger('test_module')
    
    # Verify it's a Logger instance
    assert isinstance(logger, logging.Logger)
    assert logger.name == 'test_module'


def test_logs_directory_creation():
    """Test that logs directory is created if it doesn't exist."""
    # Get the logs directory path
    logs_dir = pathlib.Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).joinpath('logs')
    
    # Ensure the directory exists
    assert logs_dir.exists()
    assert logs_dir.is_dir()

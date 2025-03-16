"""Module for configuring the application's logging system."""

import os
import logging
import logging.handlers
from typing import Dict, Any
import pathlib

class LoggingConfig:
    """Singleton class for configuring and managing application logging."""
    
    _instance = None
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(LoggingConfig, cls).__new__(cls)
            cls._instance._configure()
        return cls._instance
    
    def _configure(self):
        """Configure the logging system based on environment variables."""
        # Get log level from environment variable or default to INFO
        log_level_name = os.environ.get('CALCULATOR_LOG_LEVEL', 'INFO').upper()
        log_level = getattr(logging, log_level_name, logging.INFO)
        
        # Get log destination from environment variable or default to file
        log_dest = os.environ.get('CALCULATOR_LOG_DEST', 'file').lower()
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        
        # Remove any existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Ensure logs directory exists
        logs_dir = pathlib.Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).joinpath('logs')
        logs_dir.mkdir(exist_ok=True)
        
        # Set up handler based on destination
        if log_dest == 'file':
            log_file = os.environ.get('CALCULATOR_LOG_FILE', str(logs_dir.joinpath('calculator.log')))
            handler = logging.FileHandler(log_file)
        elif log_dest == 'rotating_file':
            log_file = os.environ.get('CALCULATOR_LOG_FILE', str(logs_dir.joinpath('calculator.log')))
            max_bytes = int(os.environ.get('CALCULATOR_LOG_MAX_BYTES', 1024 * 1024))  # 1MB default
            backup_count = int(os.environ.get('CALCULATOR_LOG_BACKUP_COUNT', 3))
            handler = logging.handlers.RotatingFileHandler(
                log_file, maxBytes=max_bytes, backupCount=backup_count
            )
        else:  # Default to console
            handler = logging.StreamHandler()
        
        # Set formatter and add handler
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)
        
        # Log configuration details
        root_logger.info(f"Logging configured with level={log_level_name}, destination={log_dest}")
        if log_dest in ('file', 'rotating_file'):
            root_logger.info(f"Log file location: {log_file}")
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """Get a logger with the specified name.
        
        Args:
            name: Name for the logger, typically __name__ of the module.
            
        Returns:
            Configured logger instance.
        """
        return logging.getLogger(name)


# Initialize logging configuration when module is imported
logging_config = LoggingConfig()

def get_logger(name: str) -> logging.Logger:
    """Convenience function to get a logger with the specified name.
    
    Args:
        name: Name for the logger, typically __name__ of the module.
        
    Returns:
        Configured logger instance.
    """
    return logging_config.get_logger(name)

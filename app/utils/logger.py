# File: app/utils/logger.py
import logging
from logging.handlers import RotatingFileHandler
import os
from app.config.settings import settings


class Logger:
    """Singleton Logger class using RotatingFileHandler with environment-based log levels."""

    _instance = None

    @staticmethod
    def get_logger():
        """Retrieve the singleton logger instance."""
        if Logger._instance is None:
            Logger()
        return Logger._instance

    def __init__(self):
        if Logger._instance is not None:
            raise Exception("Logger is a singleton class. Use get_logger().")

        # Ensure the directory for logs exists
        log_directory = "logs"
        try:
            os.makedirs(log_directory, exist_ok=True)
        except Exception as e:
            print(f"Failed to create log directory: {e}")
            raise RuntimeError(f"Failed to create log directory '{log_directory}': {e}")

        # Log file path
        log_file_path = os.path.join(log_directory, "app.log")

        # Create a logger
        logger = logging.getLogger("app_logger")

        # Set log level dynamically from .env
        log_level = settings.log_level.upper()
        logger.setLevel(getattr(logging, log_level, logging.INFO))

        # Formatter with timezone-aware timestamps
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # File handler with rotation
        file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=5 * 1024 * 1024,  # 5 MB max per log file
            backupCount=5  # Keep the last 5 log files as backups
        )
        file_handler.setLevel(getattr(logging, log_level, logging.INFO))
        file_handler.setFormatter(formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, log_level, logging.INFO))
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        # Set the singleton instance
        Logger._instance = logger
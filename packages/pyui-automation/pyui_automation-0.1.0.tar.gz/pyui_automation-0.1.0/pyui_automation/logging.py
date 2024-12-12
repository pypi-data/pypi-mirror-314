import logging
import sys
from pathlib import Path
from typing import Optional

class AutomationLogger:
    """Logger for UI Automation"""
    
    def __init__(self, name: str = 'pyui_automation'):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)  # Set to DEBUG by default
        self._setup_console_handler()

    def _setup_console_handler(self) -> None:
        """Setup console handler"""
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)  # Set handler to DEBUG
        formatter = logging.Formatter(
            '%(levelname)-8s %(name)s:%(filename)s:%(lineno)d %(message)s'
        )
        handler.setFormatter(formatter)
        # Remove existing handlers to avoid duplicates
        self._logger.handlers.clear()
        self._logger.addHandler(handler)

    def add_file_handler(self, filepath: Path) -> None:
        """Add file handler"""
        handler = logging.FileHandler(str(filepath))
        handler.setLevel(logging.DEBUG)  # Set handler to DEBUG
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    def set_level(self, level: int) -> None:
        """Set logging level"""
        self._logger.setLevel(level)
        for handler in self._logger.handlers:
            handler.setLevel(level)

    def debug(self, msg: str) -> None:
        """Log debug message"""
        self._logger.debug(msg)

    def info(self, msg: str) -> None:
        """Log info message"""
        self._logger.info(msg)

    def warning(self, msg: str) -> None:
        """Log warning message"""
        self._logger.warning(msg)

    def error(self, msg: str) -> None:
        """Log error message"""
        self._logger.error(msg)

    def critical(self, msg: str) -> None:
        """Log critical message"""
        self._logger.critical(msg)

    def exception(self, msg: str) -> None:
        """Log exception message"""
        self._logger.exception(msg)

# Global logger instance
logger = AutomationLogger()

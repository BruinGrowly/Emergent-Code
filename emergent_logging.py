"""
SPDX-License-Identifier: MIT
Emergent Code - Logging Configuration

Provides centralized logging configuration for the entire project.
"""

import logging
import sys
from typing import Optional

# Default log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
SIMPLE_FORMAT = "%(levelname)s: %(message)s"

# Color codes for terminal output
class LogColors:
    """ANSI color codes for colorized logging."""
    GREY = '\033[90m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD_RED = '\033[91m\033[1m'
    RESET = '\033[0m'


class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support for terminal output."""
    
    LEVEL_COLORS = {
        logging.DEBUG: LogColors.GREY,
        logging.INFO: LogColors.BLUE,
        logging.WARNING: LogColors.YELLOW,
        logging.ERROR: LogColors.RED,
        logging.CRITICAL: LogColors.BOLD_RED,
    }
    
    def format(self, record):
        color = self.LEVEL_COLORS.get(record.levelno, LogColors.RESET)
        record.levelname = f"{color}{record.levelname}{LogColors.RESET}"
        return super().format(record)


def setup_logging(
    level: int = logging.INFO,
    name: Optional[str] = None,
    use_colors: bool = True,
    simple: bool = False
) -> logging.Logger:
    """
    Set up logging configuration for the application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        name: Logger name (defaults to root logger if None)
        use_colors: Whether to use colored output
        simple: Whether to use simple format (no timestamps)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # Set formatter
    fmt = SIMPLE_FORMAT if simple else LOG_FORMAT
    if use_colors and sys.stdout.isatty():
        formatter = ColoredFormatter(fmt)
    else:
        formatter = logging.Formatter(fmt)
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Get a logger instance for a module.
    
    Args:
        name: Module name (usually __name__)
        level: Logging level
    
    Returns:
        Logger instance
    """
    return setup_logging(level=level, name=name)


# Create a default logger for the project
default_logger = setup_logging(name="emergent_code", simple=True)

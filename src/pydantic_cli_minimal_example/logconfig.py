"""
Logging configuration module with colorized output and local timestamps.
"""

import json
import logging
import os
import sys
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path
from typing import override

from .config import get_settings


class TextLogFormatter(logging.Formatter):
    """Custom formatter that colorizes log levels and uses local timestamps."""

    # ANSI color codes
    COLORS: dict[str, str] = {
        "DEBUG": "\033[0;36m",  # Cyan
        "INFO": "\033[0;32m",  # Green
        "WARNING": "\033[0;33m",  # Yellow
        "ERROR": "\033[0;31m",  # Red
        "CRITICAL": "\033[0;35m",  # Magenta
        "RESET": "\033[0m",  # Reset color
    }

    def __init__(self, fmt: str | None = None, colorize: bool = True):
        """Initialize the formatter with default format if none provided."""
        if fmt is None:
            fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        super().__init__(fmt)
        self.colorize: bool = colorize

    @override
    def format(self, record: logging.LogRecord) -> str:
        if not self.colorize:
            return super().format(record)

        # save the original level name, because we will add ANSI escape sequences to it
        original_levelname = record.levelname

        # Get the color for this log level
        level_color = self.COLORS.get(record.levelname, "")
        reset_color = self.COLORS["RESET"]

        # Colorize the level name
        record.levelname = f"{level_color}{record.levelname}{reset_color}"

        # Format the record with the parent formatter
        formatted = super().format(record)
        record.levelname = original_levelname  # restore the original level name

        return formatted

    @override
    def formatTime(self, record: logging.LogRecord, datefmt: str | None = None) -> str:
        local_dt = datetime.fromtimestamp(record.created).astimezone()

        # default timespec is 'auto' will gives a variable number of digits,
        # if the remaining digits are 0
        # return local_dt.isoformat(timespec='auto') # 2025-08-09T10:12:06.096717+02:00
        # return local_dt.isoformat(timespec='milliseconds') # 2025-08-09T10:12:06.096+02:00
        return local_dt.isoformat(
            timespec="microseconds"
        )  # 2025-08-09T10:12:06.096717+02:00


class JSONLFormatter(logging.Formatter):
    """Custom formatter that formats log records as JSONL."""

    @override
    def format(self, record: logging.LogRecord) -> str:
        # super().format(record) won't set record.message or record.asctime unless the
        # fmt passed  in __init__() references %(message)s and %(asctime)s
        record.message = super().format(
            record
        )  # record.message and record.asctime need to be set by LogFormatter
        record.asctime = self.formatTime(record)

        structured_record = {
            "timestamp": record.asctime,
            "level": record.levelname,
            "message": record.message,
            "logger": record.name,
        }
        return json.dumps(
            structured_record
        )  # no newline needed, I guess the file handler will add it
        # return json.dumps(record.__dict__)

    @override
    def formatTime(self, record: logging.LogRecord, datefmt: str | None = None) -> str:
        return datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(
            timespec="microseconds"
        )


def setup_console_handler() -> None:

    # Create console handler
    console_handler = logging.StreamHandler()

    # Create and set the custom formatter depending on the type of tty
    formatter: logging.Formatter | None = None
    if sys.stdout.isatty():
        formatter = TextLogFormatter(colorize=True)
    else:
        formatter = JSONLFormatter()
    console_handler.setFormatter(formatter)

    # Add the handler to the root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(console_handler)


def setup_regular_log_file_handler() -> None:
    # Create logs directory if it doesn't exist
    # https://docs.python.org/3.13/library/os.html#os.makedirs
    settings = get_settings()
    os.makedirs(settings.log_dir, exist_ok=True)

    # Create date-based rotating file handler (rotates daily at midnight, keep 5 backups)
    file_handler = TimedRotatingFileHandler(
        # f"logs/{settings.log_file}.txt",
        settings.log_dir / f"{settings.log_file}.txt",
        when="midnight",
        interval=1,
        backupCount=5,
    )

    # Create formatter without colors for file output
    file_formatter = TextLogFormatter(colorize=False)
    file_handler.setFormatter(file_formatter)

    # Add the file handler to the root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)


def setup_jsonl_log_file_handler() -> None:
    # Create logs directory if it doesn't exist
    # https://docs.python.org/3.13/library/os.html#os.makedirs
    settings = get_settings()
    os.makedirs(settings.log_dir, exist_ok=True)

    # Create date-based rotating file handler (rotates daily at midnight, keep 5 backups)
    file_handler = RotatingFileHandler(
        settings.log_dir / f"{settings.log_file}.jsonl",
        maxBytes=1 * 1_000_000,
        backupCount=5,
    )  # 1 MiB max size, 5 backups

    # Create formatter without colors for file output
    file_formatter = JSONLFormatter()
    file_handler.setFormatter(file_formatter)

    # Add the file handler to the root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)


def setup_handlers() -> None:
    """
    Set up logging configuration:
    - Remove all existing handlers
    - Add console handler with custom formatter with custom local timestamp forms and colorized
    - Add date-based rotating file handler with same formatter but no colors (rotates daily at midnight, keeps 5 backups)

    Args:
        log_level: The log level to set (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Get the root logger
    root_logger = logging.getLogger()

    # Remove all existing handlers
    while root_logger.hasHandlers():
        root_logger.removeHandler(root_logger.handlers[0])

    settings = get_settings()

    setup_console_handler()

    setup_regular_log_file_handler()

    setup_jsonl_log_file_handler()

    # Set log level from settings.toml
    log_level = settings.log_level
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    root_logger.setLevel(numeric_level)

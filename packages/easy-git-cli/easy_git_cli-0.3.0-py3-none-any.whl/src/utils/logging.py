import logging
import os
import sys
from pathlib import Path


def configure_logging():
    """Sets up logging to a file and to stdout."""
    debug = os.getenv("DEBUG", "False").lower() == "true"
    log_file_path = os.getenv("LOG_FILE_PATH", "logs/easy-git-cli.log")
    log_dir = Path(log_file_path).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("easy-git-cli")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_log_level = logging.DEBUG if debug else logging.WARNING
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(file_log_level)
    file_handler.setFormatter(formatter)

    stream_log_level = logging.DEBUG if debug else logging.CRITICAL
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(stream_log_level)
    stream_handler.setFormatter(formatter)

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    logger.info(
        f"Logging initialized. Debug: {os.getenv("DEBUG", "False").upper()}, File Log Level: {logging.getLevelName(file_log_level)}, Stream Log Level: {logging.getLevelName(stream_log_level)}"
    )
    return logger


def get_logger(name: str = "easy-git-cli") -> logging.Logger:
    """Returns a logger for a specific file/module."""
    return logging.getLogger(name)

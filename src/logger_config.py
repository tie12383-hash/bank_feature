"""Logger configuration module."""

import logging
import os


def setup_logger(name: str, log_file: str, level: int = logging.DEBUG) -> logging.Logger:
    """Set up a logger with file handler and formatter."""
    os.makedirs('logs', exist_ok=True)

    logger = logging.getLogger(name)

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    logger.setLevel(level)

    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8', delay=True)
    file_handler.setLevel(level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


utils_logger = setup_logger('utils', 'logs/utils.log')
masks_logger = setup_logger('masks', 'logs/masks.log')

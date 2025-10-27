"""Tests for logging functionality."""

import os
import logging
import pytest
from src.logger_config import setup_logger
from src.masks import get_mask_card_number, get_mask_account
from src.utils import read_json_file


class TestLogging:
    """Test class for logging functionality."""

    def test_logger_creation(self) -> None:
        """Test that loggers are properly created."""
        test_logger = setup_logger('test_logger', 'logs/test.log')

        assert isinstance(test_logger, logging.Logger)
        assert test_logger.name == 'test_logger'
        assert test_logger.level == logging.DEBUG
        assert len(test_logger.handlers) == 1

        for handler in test_logger.handlers:
            handler.close()
        if os.path.exists('logs/test.log'):
            os.unlink('logs/test.log')

    def test_masks_logging_success(self) -> None:
        """Test successful masking operations generate logs."""
        if os.path.exists('logs/masks.log'):
            os.unlink('logs/masks.log')

        card_mask = get_mask_card_number(1234567890123456)
        account_mask = get_mask_account(12345678901234567890)

        from src.logger_config import masks_logger
        for handler in masks_logger.handlers:
            handler.close()

        assert os.path.exists('logs/masks.log')

        with open('logs/masks.log', 'r', encoding='utf-8') as f:
            log_content = f.read()

        assert 'Starting card number masking for' in log_content
        assert 'Successfully masked card number' in log_content
        assert 'Starting account number masking for' in log_content
        assert 'Successfully masked account number' in log_content

    def test_masks_logging_errors(self) -> None:
        """Test error cases in masking generate error logs."""
        os.makedirs('logs', exist_ok=True)
        log_file_path = 'logs/masks.log'
        if os.path.exists(log_file_path):
            os.unlink(log_file_path)

        from src.logger_config import masks_logger
        for handler in masks_logger.handlers[:]:
            handler.close()
            masks_logger.removeHandler(handler)

        file_handler = logging.FileHandler(log_file_path, mode='w', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        masks_logger.addHandler(file_handler)
        masks_logger.setLevel(logging.DEBUG)

        try:
            get_mask_card_number(12345)
        except ValueError:
            pass

        try:
            get_mask_account(123)
        except ValueError:
            pass

        for handler in masks_logger.handlers:
            handler.flush()
            handler.close()

        assert os.path.exists(log_file_path)

        with open(log_file_path, 'r', encoding='utf-8') as f:
            log_content = f.read()

        assert 'ERROR' in log_content
        assert 'must contain' in log_content

    def test_utils_logging(self) -> None:
        """Test utils module logging."""
        if os.path.exists('logs/utils.log'):
            os.unlink('logs/utils.log')

        result = read_json_file('nonexistent.json')

        from src.logger_config import utils_logger
        for handler in utils_logger.handlers:
            handler.close()

        assert os.path.exists('logs/utils.log')

        with open('logs/utils.log', 'r', encoding='utf-8') as f:
            log_content = f.read()

        assert 'utils' in log_content
        assert 'ERROR' in log_content
        assert 'not found' in log_content.lower()
"""Tests for masks module."""

from typing import List, Tuple

import pytest  # type: ignore

from src.masks import get_mask_account, get_mask_card_number


@pytest.fixture
def valid_card_numbers() -> List[Tuple[int, str]]:
    """Fixture providing test card numbers and expected results."""
    return [
        (7000792289606361, "7000 79** **** 6361"),
        (1596837868705199, "1596 83** **** 5199"),
        (7158300734726758, "7158 30** **** 6758"),
    ]


@pytest.fixture
def valid_account_numbers() -> List[Tuple[int, str]]:
    """Fixture providing test account numbers and expected results."""
    return [
        (73654108430135874305, "**4305"),
        (64686473678894779589, "**9589"),
        (35383033474447895560, "**5560"),
    ]


class TestMaskFunctions:
    """Test class for mask functions."""

    def test_get_mask_card_number_valid(self, valid_card_numbers: List[Tuple[int, str]]) -> None:
        """Test card number masking with valid data."""
        for card_number, expected in valid_card_numbers:
            result = get_mask_card_number(card_number)
            assert result == expected

    def test_get_mask_account_valid(self, valid_account_numbers: List[Tuple[int, str]]) -> None:
        """Test account number masking with valid data."""
        for account_number, expected in valid_account_numbers:
            result = get_mask_account(account_number)
            assert result == expected

    def test_get_mask_card_number_invalid_short(self) -> None:
        """Test card number masking with short number."""
        with pytest.raises(ValueError):
            get_mask_card_number(123456789)

    def test_get_mask_card_number_invalid_long(self) -> None:
        """Test card number masking with long number."""
        with pytest.raises(ValueError):
            get_mask_card_number(12345678901234567890)

    def test_get_mask_account_invalid_short(self) -> None:
        """Test account number masking with short number."""
        with pytest.raises(ValueError):
            get_mask_account(123)

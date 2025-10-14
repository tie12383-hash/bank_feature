"""Tests for masks module."""

import pytest
from src.masks import get_mask_account, get_mask_card_number


@pytest.fixture
def valid_card_numbers():
    """Fixture providing test card numbers and expected results."""
    return [
        (7000792289606361, "7000 79** **** 6361"),
        (1596837868705199, "1596 83** **** 5199"),
        (7158300734726758, "7158 30** **** 6758"),
    ]


@pytest.fixture
def valid_account_numbers():
    """Fixture providing test account numbers and expected results."""
    return [
        (73654108430135874305, "**4305"),
        (64686473678894779589, "**9589"),
        (35383033474447895560, "**5560"),
    ]


class TestMaskFunctions:
    """Test class for mask functions."""

    @pytest.mark.parametrize("card_number, expected", [
        (7000792289606361, "7000 79** **** 6361"),
        (1596837868705199, "1596 83** **** 5199"),
        (1234567890123456, "1234 56** **** 3456"),
    ])
    def test_get_mask_card_number_valid(self, card_number, expected):
        """Test card number masking with valid data using parametrization."""
        assert get_mask_card_number(card_number) == expected

    @pytest.mark.parametrize("account_number, expected", [
        (73654108430135874305, "**4305"),
        (64686473678894779589, "**9589"),
        (12345678901234567890, "**7890"),
    ])
    def test_get_mask_account_valid(self, account_number, expected):
        """Test account number masking with valid data using parametrization."""
        assert get_mask_account(account_number) == expected

    @pytest.mark.parametrize("invalid_card_number, expected_message", [
        (123456789, "Card number must contain 16 digits"),
        (12345678901234567890, "Card number must contain 16 digits"),
    ])
    def test_get_mask_card_number_invalid(self, invalid_card_number, expected_message):
        """Test card number masking with invalid data."""
        with pytest.raises(ValueError, match=expected_message):
            get_mask_card_number(invalid_card_number)

    @pytest.mark.parametrize("invalid_account_number", [123, 12, 1])
    def test_get_mask_account_invalid(self, invalid_account_number):
        """Test account number masking with invalid data."""
        with pytest.raises(ValueError):
            get_mask_account(invalid_account_number)
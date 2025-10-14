"""Tests for widget module."""

import pytest
from src.widget import get_date, mask_account_card


@pytest.fixture
def card_data():
    """Fixture providing test card data."""
    return [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
    ]


@pytest.fixture
def account_data():
    """Fixture providing test account data."""
    return [
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("Счет 35383033474447895560", "Счет **5560"),
    ]


@pytest.fixture
def date_data():
    """Fixture providing test date data."""
    return [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-31T23:59:59.999999", "31.12.2023"),
        ("2020-01-01T00:00:00.000000", "01.01.2020"),
    ]


class TestWidgetFunctions:
    """Test class for widget functions."""

    @pytest.mark.parametrize("input_data, expected", [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Счет 64686473678894779589", "Счет **9589"),
    ])
    def test_mask_account_card(self, input_data, expected):
        """Test account and card masking with parametrization."""
        assert mask_account_card(input_data) == expected

    @pytest.mark.parametrize("input_date, expected", [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-31T23:59:59.999999", "31.12.2023"),
        ("2020-01-01T00:00:00.000000", "01.01.2020"),
    ])
    def test_get_date_valid(self, input_date, expected):
        """Test date conversion function with valid data."""
        assert get_date(input_date) == expected

    @pytest.mark.parametrize("invalid_input", [
        "Invalid Card 123",
        "Card 123456789012345",
        "Счет 123",
        "",
    ])
    def test_mask_account_card_invalid(self, invalid_input):
        """Test account_card function with invalid data."""
        with pytest.raises((ValueError, IndexError)):
            mask_account_card(invalid_input)
"""Tests for widget module."""

from typing import List, Tuple

import pytest  # type: ignore

from src.widget import get_date, mask_account_card


@pytest.fixture
def card_data() -> List[Tuple[str, str]]:
    """Fixture providing test card data."""
    return [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
    ]


@pytest.fixture
def account_data() -> List[Tuple[str, str]]:
    """Fixture providing test account data."""
    return [
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("Счет 35383033474447895560", "Счет **5560"),
    ]


@pytest.fixture
def date_data() -> List[Tuple[str, str]]:
    """Fixture providing test date data."""
    return [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-31T23:59:59.999999", "31.12.2023"),
        ("2020-01-01T00:00:00.000000", "01.01.2020"),
    ]


class TestWidgetFunctions:
    """Test class for widget functions."""

    def test_mask_account_card_cards(self, card_data: List[Tuple[str, str]]) -> None:
        """Test card masking in account_card function."""
        for input_data, expected in card_data:
            result = mask_account_card(input_data)
            assert result == expected

    def test_mask_account_card_accounts(self, account_data: List[Tuple[str, str]]) -> None:
        """Test account masking in account_card function."""
        for input_data, expected in account_data:
            result = mask_account_card(input_data)
            assert result == expected

    def test_get_date_valid(self, date_data: List[Tuple[str, str]]) -> None:
        """Test date conversion function with valid data."""
        for input_date, expected in date_data:
            result = get_date(input_date)
            assert result == expected

    def test_mask_account_card_invalid(self) -> None:
        """Test account_card function with invalid data."""
        with pytest.raises((ValueError, IndexError)):
            mask_account_card("Invalid Card 123")

    def test_get_date_invalid(self) -> None:
        """Test date conversion with invalid data."""
        with pytest.raises((ValueError, IndexError)):
            get_date("invalid-date")

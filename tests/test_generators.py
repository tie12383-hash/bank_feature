"""Tests for generators module."""

from typing import List, Dict, Any
import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Fixture providing sample transactions data."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]


@pytest.fixture
def empty_transactions() -> List[Dict[str, Any]]:
    """Fixture providing empty transactions list."""
    return []


@pytest.fixture
def transactions_without_currency() -> List[Dict[str, Any]]:
    """Fixture providing transactions without currency information."""
    return [
        {
            "id": 1,
            "description": "Test transaction",
            "operationAmount": {"amount": "100.00"},
        },
        {
            "id": 2,
            "description": "Another transaction",
            "operationAmount": {"currency": {"name": "USD"}},  # Missing code
        },
    ]


class TestFilterByCurrency:
    """Test class for filter_by_currency function."""

    def test_filter_usd_currency(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Test filtering USD transactions."""
        usd_transactions = filter_by_currency(sample_transactions, "USD")
        usd_list = list(usd_transactions)

        assert len(usd_list) == 3
        assert all(
            transaction["operationAmount"]["currency"]["code"] == "USD"
            for transaction in usd_list
        )

    def test_filter_rub_currency(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Test filtering RUB transactions."""
        rub_transactions = filter_by_currency(sample_transactions, "RUB")
        rub_list = list(rub_transactions)

        assert len(rub_list) == 2
        assert all(
            transaction["operationAmount"]["currency"]["code"] == "RUB"
            for transaction in rub_list
        )

    def test_filter_nonexistent_currency(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Test filtering with non-existent currency code."""
        eur_transactions = filter_by_currency(sample_transactions, "EUR")
        eur_list = list(eur_transactions)

        assert len(eur_list) == 0

    def test_filter_empty_list(self, empty_transactions: List[Dict[str, Any]]) -> None:
        """Test filtering empty transactions list."""
        result = filter_by_currency(empty_transactions, "USD")
        assert list(result) == []

    def test_filter_transactions_without_currency(
            self, transactions_without_currency: List[Dict[str, Any]]
    ) -> None:
        """Test filtering transactions without currency information."""
        result = filter_by_currency(transactions_without_currency, "USD")
        assert list(result) == []

    def test_iterator_behavior(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Test that function returns iterator with proper behavior."""
        usd_transactions = filter_by_currency(sample_transactions, "USD")

        first_transaction = next(usd_transactions)
        assert first_transaction["id"] == 939719570

        second_transaction = next(usd_transactions)
        assert second_transaction["id"] == 142264268


class TestTransactionDescriptions:
    """Test class for transaction_descriptions function."""

    def test_get_all_descriptions(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Test getting all transaction descriptions."""
        descriptions = transaction_descriptions(sample_transactions)
        descriptions_list = list(descriptions)

        expected_descriptions = [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Перевод организации",
        ]

        assert descriptions_list == expected_descriptions

    def test_empty_transactions(self, empty_transactions: List[Dict[str, Any]]) -> None:
        """Test getting descriptions from empty list."""
        descriptions = transaction_descriptions(empty_transactions)
        assert list(descriptions) == []

    def test_generator_behavior(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Test that function returns generator with proper behavior."""
        descriptions = transaction_descriptions(sample_transactions)

        first_description = next(descriptions)
        assert first_description == "Перевод организации"

        second_description = next(descriptions)
        assert second_description == "Перевод со счета на счет"

    @pytest.mark.parametrize("index, expected_description", [
        (0, "Перевод организации"),
        (1, "Перевод со счета на счет"),
        (4, "Перевод организации"),
    ])
    def test_specific_descriptions(
            self, sample_transactions: List[Dict[str, Any]], index: int, expected_description: str
    ) -> None:
        """Test specific transaction descriptions using parametrization."""
        descriptions = transaction_descriptions(sample_transactions)

        for _ in range(index):
            next(descriptions)

        assert next(descriptions) == expected_description


class TestCardNumberGenerator:
    """Test class for card_number_generator function."""

    @pytest.mark.parametrize("start, end, expected_count, expected_first, expected_last", [
        (1, 5, 5, "0000 0000 0000 0001", "0000 0000 0000 0005"),
        (9999, 10001, 3, "0000 0000 0000 9999", "0000 0000 0001 0001"),
        (9999999999999999, 9999999999999999, 1, "9999 9999 9999 9999", "9999 9999 9999 9999"),
    ])
    def test_card_number_generator_ranges(
            self, start: int, end: int, expected_count: int, expected_first: str, expected_last: str
    ) -> None:
        """Test card number generator with different ranges using parametrization."""
        generator = card_number_generator(start, end)
        numbers = list(generator)

        assert len(numbers) == expected_count
        assert numbers[0] == expected_first
        assert numbers[-1] == expected_last

    def test_single_number(self) -> None:
        """Test generator with single number."""
        generator = card_number_generator(42, 42)
        numbers = list(generator)

        assert len(numbers) == 1
        assert numbers[0] == "0000 0000 0000 0042"

    def test_format_correctness(self) -> None:
        """Test that card numbers are properly formatted."""
        generator = card_number_generator(1234567890123456, 1234567890123456)
        number = next(generator)

        assert len(number) == 19
        assert number.count(" ") == 3
        parts = number.split(" ")
        assert all(len(part) == 4 for part in parts)
        assert all(part.isdigit() for part in parts)

    def test_generator_behavior(self) -> None:
        """Test that function returns generator with proper behavior."""
        generator = card_number_generator(1, 3)

        assert next(generator) == "0000 0000 0000 0001"
        assert next(generator) == "0000 0000 0000 0002"
        assert next(generator) == "0000 0000 0000 0003"

        with pytest.raises(StopIteration):
            next(generator)

    def test_edge_cases(self) -> None:
        """Test edge cases for card number generation."""

        generator = card_number_generator(0, 0)
        assert next(generator) == "0000 0000 0000 0000"

        generator = card_number_generator(9999999999999998, 9999999999999999)
        numbers = list(generator)
        assert numbers == ["9999 9999 9999 9998", "9999 9999 9999 9999"]
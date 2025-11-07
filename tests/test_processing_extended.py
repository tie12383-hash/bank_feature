"""Extended tests for processing module with new functions."""

from typing import List, Dict, Any
import pytest
from src.processing import filter_by_description, count_transactions_by_category


class TestExtendedProcessing:
    """Test class for extended processing functions."""

    @pytest.fixture
    def sample_transactions(self) -> List[Dict[str, Any]]:
        """Sample transactions for testing."""
        return [
            {
                "id": 1,
                "description": "Перевод организации",
                "state": "EXECUTED",
                "date": "2024-01-01T10:00:00"
            },
            {
                "id": 2,
                "description": "Перевод со счета на счет",
                "state": "EXECUTED",
                "date": "2024-01-02T11:00:00"
            },
            {
                "id": 3,
                "description": "Открытие вклада",
                "state": "EXECUTED",
                "date": "2024-01-03T12:00:00"
            },
            {
                "id": 4,
                "description": "Перевод организации",
                "state": "CANCELED",
                "date": "2024-01-04T13:00:00"
            },
            {
                "id": 5,
                "state": "EXECUTED",
                "date": "2024-01-05T14:00:00"
            }
        ]

    def test_filter_by_description_exact_match(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Test filtering by exact description match."""
        result = filter_by_description(sample_transactions, "Перевод организации")
        assert len(result) == 2
        assert all("Перевод организации" in t["description"] for t in result if t.get("description"))

    def test_filter_by_description_partial_match(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Test filtering by partial description match."""
        result = filter_by_description(sample_transactions, "Перевод")
        assert len(result) == 3
        assert all("Перевод" in t["description"] for t in result if t.get("description"))

    def test_filter_by_description_case_insensitive(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Test case insensitive filtering."""
        result = filter_by_description(sample_transactions, "перевод")
        assert len(result) == 3

    def test_filter_by_description_no_match(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Test filtering with no matches."""
        result = filter_by_description(sample_transactions, "Несуществующий")
        assert len(result) == 0

    def test_filter_by_description_empty_string(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Test filtering with empty search string."""
        result = filter_by_description(sample_transactions, "")
        assert len(result) == len(sample_transactions)

    def test_filter_by_description_no_description_field(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Test filtering when some transactions lack description."""
        result = filter_by_description(sample_transactions, "Перевод")
        assert len(result) == 3

    def test_count_transactions_by_category(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Test counting transactions by category."""
        categories = ["Перевод организации", "Открытие вклада", "Несуществующая категория"]
        result = count_transactions_by_category(sample_transactions, categories)

        assert result.get("Перевод организации", 0) == 2
        assert result.get("Открытие вклада", 0) == 1
        assert result.get("Несуществующая категория", 0) == 0

    def test_count_transactions_empty_categories(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Test counting with empty categories list."""
        result = count_transactions_by_category(sample_transactions, [])
        assert result == {}

    def test_count_transactions_no_matching_categories(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Test counting with no matching categories."""
        result = count_transactions_by_category(sample_transactions, ["Несуществующая категория"])
        assert result.get("Несуществующая категория", 0) == 0

    def test_regex_special_characters(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Test filtering with regex special characters."""
        result = filter_by_description(sample_transactions, "Перевод[")
        assert isinstance(result, list)


class TestIntegration:
    """Integration tests for the complete workflow."""

    def test_complete_workflow(self) -> None:
        """Test complete workflow from filtering to display."""
        from src.processing import filter_by_state, sort_by_date, filter_by_description
        from src.utils import filter_ruble_transactions

        transactions = [
            {
                "id": 1,
                "description": "Перевод организации",
                "state": "EXECUTED",
                "date": "2024-01-01T10:00:00",
                "operationAmount": {
                    "amount": "1000.0",
                    "currency": {"code": "RUB"}
                }
            },
            {
                "id": 2,
                "description": "Перевод другу",
                "state": "EXECUTED",
                "date": "2024-01-02T11:00:00",
                "operationAmount": {
                    "amount": "50.0",
                    "currency": {"code": "USD"}
                }
            }
        ]

        executed = filter_by_state(transactions, "EXECUTED")
        assert len(executed) == 2

        sorted_transactions = sort_by_date(executed, descending=False)
        assert sorted_transactions[0]["id"] == 1

        filtered_by_desc = filter_by_description(sorted_transactions, "организации")
        assert len(filtered_by_desc) == 1

        ruble_only = filter_ruble_transactions(filtered_by_desc)
        assert len(ruble_only) == 1
        assert ruble_only[0]["operationAmount"]["currency"]["code"] == "RUB"
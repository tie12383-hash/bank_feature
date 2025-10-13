"""Tests for processing module."""

from typing import Any, Dict, List

import pytest  # type: ignore

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_operations() -> List[Dict[str, Any]]:
    """Fixture providing sample operations data."""
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 123456789, "state": "PENDING", "date": "2020-01-01T00:00:00.000000"},
        {"id": 987654321, "state": "FAILED", "date": "2019-12-31T23:59:59.999999"},
    ]


@pytest.fixture
def operations_with_same_dates() -> List[Dict[str, Any]]:
    """Fixture providing operations with same dates."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 2, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 3, "state": "CANCELED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 4, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    ]


@pytest.fixture
def operations_without_state() -> List[Dict[str, Any]]:
    """Fixture providing operations without state field."""
    return [
        {"id": 1, "date": "2019-07-03T18:35:29.512364"},
        {"id": 2, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 3, "date": "2018-09-12T21:27:25.241689"},
    ]


def all_operations_executed(operations: List[Dict[str, Any]]) -> bool:
    """Check if all operations are executed."""
    return all(operation.get("state") == "EXECUTED" for operation in operations)


def dates_sorted_descending(operations: List[Dict[str, Any]]) -> bool:
    """Check if dates are sorted in descending order."""
    dates = [operation["date"] for operation in operations]
    return dates == sorted(dates, reverse=True)


class TestProcessingFunctions:
    """Test class for processing functions."""

    def test_filter_by_state_default(self, sample_operations: List[Dict[str, Any]]) -> None:
        """Test state filtering with default state."""
        result = filter_by_state(sample_operations)
        assert len(result) == 2
        assert all(op["state"] == "EXECUTED" for op in result)

    def test_filter_by_state_canceled(self, sample_operations: List[Dict[str, Any]]) -> None:
        """Test state filtering with CANCELED state."""
        result = filter_by_state(sample_operations, "CANCELED")
        assert len(result) == 2
        assert all(op["state"] == "CANCELED" for op in result)

    def test_filter_empty_list(self) -> None:
        """Test filtering empty operations list."""
        result = filter_by_state([], "EXECUTED")
        assert result == []

    def test_filter_operations_without_state(self, operations_without_state: List[Dict[str, Any]]) -> None:
        """Test filtering operations without state field."""
        result = filter_by_state(operations_without_state, "EXECUTED")
        assert len(result) == 1
        assert result[0]["id"] == 2

    def test_sort_by_date_descending(self, sample_operations: List[Dict[str, Any]]) -> None:
        """Test date sorting in descending order."""
        result = sort_by_date(sample_operations, True)
        assert result[0]["date"] == "2020-01-01T00:00:00.000000"
        assert result[-1]["date"] == "2018-06-30T02:08:58.425572"

    def test_sort_by_date_ascending(self, sample_operations: List[Dict[str, Any]]) -> None:
        """Test date sorting in ascending order."""
        result = sort_by_date(sample_operations, False)
        assert result[0]["date"] == "2018-06-30T02:08:58.425572"
        assert result[-1]["date"] == "2020-01-01T00:00:00.000000"

    def test_sort_operations_same_dates(self, operations_with_same_dates: List[Dict[str, Any]]) -> None:
        """Test sorting operations with same dates."""
        result = sort_by_date(operations_with_same_dates, True)
        assert [op["id"] for op in result] == [1, 2, 4, 3]

    def test_sort_empty_list(self) -> None:
        """Test sorting empty operations list."""
        result = sort_by_date([], True)
        assert result == []

    def test_combination_filter_and_sort(self, sample_operations: List[Dict[str, Any]]) -> None:
        """Test combination of filtering and sorting operations."""
        executed_operations = filter_by_state(sample_operations, "EXECUTED")
        sorted_operations = sort_by_date(executed_operations, True)

        assert len(sorted_operations) == 2
        assert all_operations_executed(sorted_operations)
        assert dates_sorted_descending(sorted_operations)

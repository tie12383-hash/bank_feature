"""Tests for processing module."""

from typing import List, Dict, Any
import pytest
from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_operations():
    """Fixture providing sample operations data."""
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 123456789, "state": "PENDING", "date": "2020-01-01T00:00:00.000000"},
    ]


class TestProcessingFunctions:
    """Test class for processing functions."""

    @pytest.mark.parametrize("state, expected_count", [
        ("EXECUTED", 2),
        ("CANCELED", 2),
        ("PENDING", 1),
        ("UNKNOWN", 0),
    ])
    def test_filter_by_state(self, sample_operations, state, expected_count):
        """Test state filtering with different states using parametrization."""
        result = filter_by_state(sample_operations, state)
        assert len(result) == expected_count
        if expected_count > 0:
            assert all(op["state"] == state for op in result)

    @pytest.mark.parametrize("descending, expected_first_id", [
        (True, 123456789),  # Latest date
        (False, 939719570),  # Earliest date
    ])
    def test_sort_by_date(self, sample_operations, descending, expected_first_id):
        """Test date sorting with different orders."""
        result = sort_by_date(sample_operations, descending)
        assert result[0]["id"] == expected_first_id

    def test_combination_filter_and_sort(self, sample_operations):
        """Test combination of filtering and sorting operations."""
        # Filter executed operations
        executed_operations = filter_by_state(sample_operations, "EXECUTED")

        # Sort by date descending
        sorted_operations = sort_by_date(executed_operations, True)

        # Verify results
        assert len(sorted_operations) == 2
        assert all(op["state"] == "EXECUTED" for op in sorted_operations)
        assert sorted_operations[0]["date"] > sorted_operations[1]["date"]
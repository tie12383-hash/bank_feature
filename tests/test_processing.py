"""Tests for processing module."""

from src.processing import filter_by_state, sort_by_date


def test_filter_by_state() -> None:
    """Test state filtering function."""
    test_data = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    # Test with default state (EXECUTED)
    result = filter_by_state(test_data)
    assert len(result) == 2
    assert all(op["state"] == "EXECUTED" for op in result)

    # Test with explicit CANCELED state
    result = filter_by_state(test_data, "CANCELED")
    assert len(result) == 2
    assert all(op["state"] == "CANCELED" for op in result)


def test_sort_by_date() -> None:
    """Test date sorting function."""
    test_data = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    # Test descending sort (default)
    result_desc = sort_by_date(test_data)
    assert result_desc[0]["date"] == "2019-07-03T18:35:29.512364"
    assert result_desc[-1]["date"] == "2018-06-30T02:08:58.425572"

    # Test ascending sort
    result_asc = sort_by_date(test_data, False)
    assert result_asc[0]["date"] == "2018-06-30T02:08:58.425572"
    assert result_asc[-1]["date"] == "2019-07-03T18:35:29.512364"

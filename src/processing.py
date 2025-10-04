"""Module for processing bank operations data."""

from typing import List, Dict, Any


def filter_by_state(
    operations: List[Dict[str, Any]], state: str = "EXECUTED"
) -> List[Dict[str, Any]]:
    """
    Filter operations by state.

    Args:
        operations: List of dictionaries with operations
        state: State for filtering (default 'EXECUTED')

    Returns:
        Filtered list of operations
    """
    return [op for op in operations if op.get("state") == state]


def sort_by_date(
    operations: List[Dict[str, Any]], descending: bool = True
) -> List[Dict[str, Any]]:
    """
    Sort operations by date.

    Args:
        operations: List of dictionaries with operations
        descending: Sort order (True - descending, False - ascending)

    Returns:
        Sorted list of operations
    """
    return sorted(
        operations,
        key=lambda x: x["date"],
        reverse=descending,
    )

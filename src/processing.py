"""Module for processing bank operations data."""

import re
from collections import Counter
from typing import Any, Dict, List


def filter_by_state(operations: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Filter operations by state."""
    return [op for op in operations if op.get("state") == state]


def sort_by_date(operations: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """Sort operations by date."""
    return sorted(
        operations,
        key=lambda x: x["date"],
        reverse=descending,
    )


def filter_by_description(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """Filter transactions by description using regular expressions."""
    if not search_string:
        return transactions

    try:
        pattern = re.compile(search_string, re.IGNORECASE)
        return [
            transaction for transaction in transactions
            if transaction.get('description') and pattern.search(transaction['description'])
        ]
    except re.error:
        search_lower = search_string.lower()
        return [
            transaction for transaction in transactions
            if transaction.get('description') and search_lower in transaction['description'].lower()
        ]


def count_transactions_by_category(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """Count transactions by category."""
    category_counter: Counter[str] = Counter()

    for transaction in transactions:
        description = transaction.get('description', '')
        if description in categories:
            category_counter[description] += 1

    return dict(category_counter)

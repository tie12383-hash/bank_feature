"""Utility functions for working with JSON files and transaction data."""

import json
from typing import Any, Dict, List, Optional


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """Read transaction data from JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data
        else:
            return []

    except (FileNotFoundError, json.JSONDecodeError):
        return []
    except Exception:
        return []


def filter_executed_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filter only executed transactions."""
    return [transaction for transaction in transactions if transaction.get("state") == "EXECUTED"]


def get_transaction_amount(transaction: Dict[str, Any]) -> Optional[float]:
    """Extract amount from transaction."""
    try:
        operation_amount = transaction.get("operationAmount", {})
        amount_str = operation_amount.get("amount", "0")
        return float(amount_str)
    except (ValueError, TypeError):
        return None

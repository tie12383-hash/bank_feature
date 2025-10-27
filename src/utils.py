"""Utility functions for working with JSON files and transaction data."""

import json
import os
from typing import List, Dict, Any, Optional
from .logger_config import utils_logger


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Read transaction data from JSON file.

    Args:
        file_path: Path to the JSON file

    Returns:
        List of transaction dictionaries. Returns empty list if file is empty,
        doesn't contain a list, or file is not found.

    Example:
        >>> transactions = read_json_file("data/operations.json")
        >>> len(transactions)
        5
    """
    utils_logger.debug(f"Attempting to read JSON file: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Check if data is a list
        if isinstance(data, list):
            utils_logger.info(f"Successfully read {len(data)} transactions from {file_path}")
            return data
        else:
            utils_logger.warning(f"JSON file {file_path} does not contain a list. Returning empty list.")
            return []

    except FileNotFoundError:
        utils_logger.error(f"JSON file not found: {file_path}")
        return []
    except json.JSONDecodeError as e:
        utils_logger.error(f"Invalid JSON format in file {file_path}: {str(e)}")
        return []
    except Exception as e:
        utils_logger.error(f"Unexpected error reading file {file_path}: {str(e)}")
        return []


def filter_executed_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter only executed transactions.

    Args:
        transactions: List of transaction dictionaries

    Returns:
        List of executed transactions only

    Example:
        >>> executed = filter_executed_transactions(transactions)
    """
    utils_logger.debug(f"Filtering executed transactions from {len(transactions)} total transactions")

    executed_transactions = [
        transaction for transaction in transactions
        if transaction.get('state') == 'EXECUTED'
    ]

    utils_logger.info(
        f"Filtered {len(executed_transactions)} executed transactions "
        f"from {len(transactions)} total transactions"
    )

    return executed_transactions


def get_transaction_amount(transaction: Dict[str, Any]) -> Optional[float]:
    """
    Extract amount from transaction.

    Args:
        transaction: Transaction dictionary

    Returns:
        Amount as float or None if not found
    """
    transaction_id = transaction.get('id', 'unknown')
    utils_logger.debug(f"Extracting amount from transaction ID: {transaction_id}")

    try:
        operation_amount = transaction.get('operationAmount', {})
        amount_str = operation_amount.get('amount', '0')
        amount = float(amount_str)

        utils_logger.debug(f"Successfully extracted amount {amount} from transaction {transaction_id}")
        return amount

    except (ValueError, TypeError) as e:
        utils_logger.error(
            f"Failed to extract amount from transaction {transaction_id}: "
            f"amount_str='{operation_amount.get('amount')}', error: {str(e)}"
        )
        return None
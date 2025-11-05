"""Module for working with transaction data using generators."""

from typing import Dict, Any, Iterator, List, Generator


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    Filter transactions by currency code and return an iterator.
    """
    for transaction in transactions:
        operation_amount = transaction.get("operationAmount", {})
        currency = operation_amount.get("currency", {})
        if currency.get("code") == currency_code:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[str, None, None]:
    """
    Generate transaction descriptions one by one.
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """
    Generate card numbers in the format XXXX XXXX XXXX XXXX.
    """
    for number in range(start, end + 1):

        card_number_str = str(number).zfill(16)

        formatted_number = " ".join(
            card_number_str[i: i + 4] for i in range(0, 16, 4)
        )
        yield formatted_number
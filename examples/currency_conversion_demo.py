"""Demonstration of currency conversion functionality."""

import os
from src.utils import read_json_file, filter_executed_transactions
from src.external_api import convert_amount_to_rubles


def main() -> None:
    """Demonstrate currency conversion functionality."""
    print("=== Currency Conversion Demo ===\n")

    transactions = read_json_file("data/operations.json")
    print(f"Loaded {len(transactions)} transactions from JSON file")

    executed_transactions = filter_executed_transactions(transactions)
    print(f"Found {len(executed_transactions)} executed transactions\n")

    print("Executed transactions (amounts in RUB):")
    print("-" * 50)

    total_rub = 0.0
    for transaction in executed_transactions:
        amount_rub = convert_amount_to_rubles(transaction)
        total_rub += amount_rub

        operation_amount = transaction.get('operationAmount', {})
        original_amount = operation_amount.get('amount', '0')
        currency = operation_amount.get('currency', {}).get('code', 'RUB')

        print(f"ID: {transaction['id']}")
        print(f"Description: {transaction['description']}")
        print(f"Original: {original_amount} {currency}")
        print(f"Converted: {amount_rub:.2f} RUB")
        print(f"Date: {transaction['date']}")
        print("-" * 30)

    print(f"\nTotal amount in RUB: {total_rub:.2f}")

    api_key = os.getenv('EXCHANGE_RATE_API_KEY')
    if not api_key:
        print("\n⚠️  Note: EXCHANGE_RATE_API_KEY not set. Using fallback rates.")
        print("   To enable real-time conversion, add your API key to .env file")


if __name__ == "__main__":
    main()
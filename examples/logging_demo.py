"""Demonstration of logging functionality."""

import os
import sys

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.masks import get_mask_card_number, get_mask_account
from src.utils import read_json_file, filter_executed_transactions, get_transaction_amount


def main() -> None:
    """Demonstrate logging functionality."""
    print("=== Logging Demonstration ===\n")

    # Clean up previous log files
    if os.path.exists('logs/utils.log'):
        os.remove('logs/utils.log')
    if os.path.exists('logs/masks.log'):
        os.remove('logs/masks.log')

    print("1. Testing masks module logging:")
    print("-" * 40)

    try:
        # Successful card masking
        card_mask = get_mask_card_number(1234567890123456)
        print(f"Card mask: {card_mask}")

        # Successful account masking
        account_mask = get_mask_account(12345678901234567890)
        print(f"Account mask: {account_mask}")

        # Error case - invalid card number
        try:
            get_mask_card_number(12345)
        except ValueError as e:
            print(f"Expected error: {e}")

        # Error case - invalid account number
        try:
            get_mask_account(123)
        except ValueError as e:
            print(f"Expected error: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")

    print("\n2. Testing utils module logging:")
    print("-" * 40)

    # Test reading existing JSON file
    transactions = read_json_file("data/operations.json")
    print(f"Read {len(transactions)} transactions")

    # Test filtering
    executed = filter_executed_transactions(transactions)
    print(f"Filtered to {len(executed)} executed transactions")

    # Test amount extraction
    if executed:
        amount = get_transaction_amount(executed[0])
        print(f"Extracted amount from first transaction: {amount}")

    # Test reading non-existent file
    empty_result = read_json_file("nonexistent.json")
    print(f"Result for non-existent file: {empty_result}")

    print("\n3. Log files created:")
    print("-" * 40)

    if os.path.exists('logs/utils.log'):
        print("✅ logs/utils.log")
        with open('logs/utils.log', 'r') as f:
            print("Utils log content:")
            for line in f.readlines()[-5:]:  # Show last 5 lines
                print(f"  {line.strip()}")

    if os.path.exists('logs/masks.log'):
        print("\n✅ logs/masks.log")
        with open('logs/masks.log', 'r') as f:
            print("Masks log content:")
            for line in f.readlines()[-5:]:  # Show last 5 lines
                print(f"  {line.strip()}")

    print("\n=== Logging Demo Complete ===")


if __name__ == "__main__":
    main()
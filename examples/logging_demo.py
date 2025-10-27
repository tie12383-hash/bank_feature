"""Demonstration of logging functionality."""

import os
import sys
import logging
import time

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.masks import get_mask_card_number, get_mask_account
from src.utils import read_json_file, filter_executed_transactions, get_transaction_amount


def clear_logs() -> None:
    """Safely clear log files by closing handlers first."""
    # Get all loggers
    loggers = [logging.getLogger('utils'), logging.getLogger('masks')]

    # Close all handlers for these loggers
    for logger in loggers:
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

    # Give time for files to be released
    time.sleep(0.1)

    # Now safely remove log files
    log_files = ['logs/utils.log', 'logs/masks.log']
    for log_file in log_files:
        if os.path.exists(log_file):
            try:
                os.remove(log_file)
                print(f"Cleared: {log_file}")
            except PermissionError:
                print(f"Could not clear {log_file} - file might be in use")


def main() -> None:
    """Demonstrate logging functionality."""
    print("=== Logging Demonstration ===\n")

    # Clear previous log files safely
    clear_logs()

    # Re-import modules to recreate loggers with clean files
    import importlib
    import src.masks
    import src.utils
    importlib.reload(src.masks)
    importlib.reload(src.utils)

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
    if transactions:
        executed = filter_executed_transactions(transactions)
        print(f"Filtered to {len(executed)} executed transactions")

        # Test amount extraction
        if executed:
            amount = get_transaction_amount(executed[0])
            print(f"Extracted amount from first transaction: {amount}")
    else:
        print("No transactions found in operations.json")
        executed = []

    # Test reading non-existent file
    empty_result = read_json_file("nonexistent.json")
    print(f"Result for non-existent file: {empty_result}")

    print("\n3. Log files created:")
    print("-" * 40)

    # Close handlers before reading log files
    for logger_name in ['utils', 'masks']:
        logger = logging.getLogger(logger_name)
        for handler in logger.handlers[:]:
            handler.close()

    time.sleep(0.1)  # Ensure files are released

    if os.path.exists('logs/utils.log'):
        print("✅ logs/utils.log")
        try:
            with open('logs/utils.log', 'r', encoding='utf-8') as f:
                print("Utils log content:")
                lines = f.readlines()
                for line in lines[-5:]:  # Show last 5 lines
                    print(f"  {line.strip()}")
        except PermissionError:
            print("  Could not read utils.log - file is locked")

    if os.path.exists('logs/masks.log'):
        print("\n✅ logs/masks.log")
        try:
            with open('logs/masks.log', 'r', encoding='utf-8') as f:
                print("Masks log content:")
                lines = f.readlines()
                for line in lines[-5:]:  # Show last 5 lines
                    print(f"  {line.strip()}")
        except PermissionError:
            print("  Could not read masks.log - file is locked")

    print("\n=== Logging Demo Complete ===")


if __name__ == "__main__":
    main()
"""Demonstration of generators module functionality."""

from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


def main() -> None:
    """Demonstrate generators module functionality."""
    print("=== Generators Module Demo ===\n")

    transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод с организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
    ]

    print("1. Filter by Currency (USD):")
    print("-" * 30)
    usd_transactions = filter_by_currency(transactions, "USD")
    for _ in range(2):
        transaction = next(usd_transactions)
        print(f"ID: {transaction['id']}, Amount: {transaction['operationAmount']['amount']} USD")

    print("\n2. Transaction Descriptions:")
    print("-" * 30)
    descriptions = transaction_descriptions(transactions)
    for _ in range(3):
        print(next(descriptions))

    print("\n3. Card Number Generator:")
    print("-" * 30)
    for card_number in card_number_generator(1, 5):
        print(card_number)


if __name__ == "__main__":
    main()
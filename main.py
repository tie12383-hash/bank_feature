"""Main module for bank transactions processing."""

from typing import List, Dict, Any
from src.processing import (
    filter_by_state,
    sort_by_date,
    filter_by_description
)
from src.utils import (
    read_json_file,
    filter_ruble_transactions,
    get_user_input
)
from src.file_reader import read_csv_file, read_excel_file
from src.widget import get_date, mask_account_card


def get_amount_display(transaction: Dict[str, Any]) -> str:
    """Get formatted amount string for display."""
    try:
        from src.external_api import get_transaction_amount_in_rubles
        amount_rub = get_transaction_amount_in_rubles(transaction)
        return f"{amount_rub:.2f} руб."
    except ImportError:
        operation_amount = transaction.get("operationAmount", {})
        amount = operation_amount.get("amount", "0")
        currency = operation_amount.get("currency", {})
        currency_code = currency.get("code", "RUB")
        return f"{amount} {currency_code}"


def display_transaction(transaction: Dict[str, Any]) -> None:
    """Display a single transaction in formatted way."""
    date = get_date(transaction['date'])
    description = transaction.get('description', 'N/A')

    from_account = mask_account_card(transaction.get('from', 'N/A')) if transaction.get('from') else None
    to_account = mask_account_card(transaction.get('to', 'Счет **XXXX'))

    amount_display = get_amount_display(transaction)

    print(f"{date} {description}")
    if from_account:
        print(f"{from_account} -> {to_account}")
    else:
        print(f"{to_account}")
    print(f"Сумма: {amount_display}\n")


def display_transactions_summary(transactions: List[Dict[str, Any]]) -> None:
    """Display summary of transactions."""
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\nВсего банковских операций в выборке: {len(transactions)}\n")

    for transaction in transactions:
        display_transaction(transaction)


def get_file_reader_choice() -> tuple[str, callable]:
    """Get user choice for file type and return appropriate reader function."""
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    file_choice = get_user_input("Ваш выбор: ", ["1", "2", "3"])

    file_types = {
        "1": ("JSON", read_json_file),
        "2": ("CSV", read_csv_file),
        "3": ("XLSX", read_excel_file)
    }

    file_type, reader_function = file_types[file_choice]
    print(f"\nДля обработки выбран {file_type}-файл.")
    return file_type, reader_function


def get_transactions_from_file(reader_function: callable) -> List[Dict[str, Any]]:
    """Get transactions from file using the provided reader function."""
    while True:
        file_path = get_user_input("Введите путь к файлу: ")
        if not file_path.strip():
            print("Путь к файлу не может быть пустым. Попробуйте снова.")
            continue

        transactions = reader_function(file_path)

        if not transactions:
            print("Не удалось загрузить транзакции из файла. Проверьте путь и формат файла.")
            retry = get_user_input("Хотите попробовать другой файл? (Да/Нет): ", ["да", "нет"])
            if retry.lower() == "нет":
                return []
            continue

        print(f"Загружено {len(transactions)} транзакций.")
        return transactions


def get_status_filter() -> str:
    """Get status filter from user with validation."""
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        status = get_user_input(
            "\nВведите статус, по которому необходимо выполнить фильтрацию.\n"
            f"Доступные для фильтровки статусы: {', '.join(valid_statuses)}\n"
            "Ваш выбор: "
        ).upper()

        if status in valid_statuses:
            return status
        print(f'Статус операции "{status}" недоступен.')


def apply_sorting(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Apply sorting to transactions based on user preference."""
    sort_choice = get_user_input("\nОтсортировать операции по дате? (Да/Нет): ", ["да", "нет"])

    if sort_choice.lower() == "да":
        order_choice = get_user_input(
            "Отсортировать по возрастанию или по убыванию? ",
            ["по возрастанию", "по убыванию"]
        )
        descending = order_choice.lower() == "по убыванию"
        transactions = sort_by_date(transactions, descending)
        order_text = "убыванию" if descending else "возрастанию"
        print(f"Операции отсортированы по дате (по {order_text})")

    return transactions


def apply_currency_filter(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Apply currency filter to transactions."""
    ruble_choice = get_user_input("\nВыводить только рублевые транзакции? (Да/Нет): ", ["да", "нет"])

    if ruble_choice.lower() == "да":
        transactions = filter_ruble_transactions(transactions)
        print("Оставлены только рублевые транзакции")

    return transactions


def apply_description_filter(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Apply description filter to transactions."""
    desc_choice = get_user_input(
        "\nОтфильтровать список транзакций по определенному слову в описании? (Да/Нет): ",
        ["да", "нет"]
    )

    if desc_choice.lower() == "да":
        search_word = get_user_input("Введите слово для поиска в описании: ")
        if search_word.strip():
            original_count = len(transactions)
            transactions = filter_by_description(transactions, search_word)
            print(f"Найдено {len(transactions)} транзакций с словом '{search_word}' в описании")
        else:
            print("Пустая строка поиска. Пропускаем фильтрацию по описанию.")

    return transactions


def main() -> None:
    """Main function with user interface for bank transactions processing."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    try:
        file_type, reader_function = get_file_reader_choice()

        transactions = get_transactions_from_file(reader_function)
        if not transactions:
            return

        status = get_status_filter()
        filtered_transactions = filter_by_state(transactions, status)
        print(f'\nОперации отфильтрованы по статусу: "{status}"')

        if not filtered_transactions:
            print("Не найдено ни одной транзакции с выбранным статусом.")
            return

        filtered_transactions = apply_sorting(filtered_transactions)
        filtered_transactions = apply_currency_filter(filtered_transactions)
        filtered_transactions = apply_description_filter(filtered_transactions)

        print("\nРаспечатываю итоговый список транзакций...")
        display_transactions_summary(filtered_transactions)

    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
    except Exception as e:
        print(f"\nПроизошла непредвиденная ошибка: {e}")
        print("Пожалуйста, попробуйте запустить программу снова.")


if __name__ == "__main__":
    main()

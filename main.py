"""Main module for bank transactions processing."""

from src.processing import (
    filter_by_state,
    sort_by_date,
    filter_by_description,
    count_transactions_by_category
)
from src.utils import (
    read_json_file,
    filter_ruble_transactions,
    get_user_input
)
from src.file_reader import read_csv_file, read_excel_file
from src.widget import get_date, mask_account_card
from src.external_api import get_transaction_amount_in_rubles


def display_transaction(transaction: dict) -> None:
    """Display a single transaction in formatted way."""
    date = get_date(transaction['date'])
    description = transaction.get('description', 'N/A')

    from_account = mask_account_card(transaction.get('from', 'N/A'))
    to_account = mask_account_card(transaction.get('to', 'N/A'))

    amount_rub = get_transaction_amount_in_rubles(transaction)

    print(f"{date} {description}")
    if transaction.get('from'):
        print(f"{from_account} -> {to_account}")
    else:
        print(f"{to_account}")
    print(f"Сумма: {amount_rub:.2f} руб.\n")


def main() -> None:
    """Main function with user interface for bank transactions processing."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
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

    file_path = get_user_input("Введите путь к файлу: ")
    transactions = reader_function(file_path)

    if not transactions:
        print("Не удалось загрузить транзакции из файла.")
        return

    print(f"Загружено {len(transactions)} транзакций.")

    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status = get_user_input(
            "Введите статус, по которому необходимо выполнить фильтрацию. \n"
            f"Доступные для фильтровки статусы: {', '.join(valid_statuses)}\n"
            "Ваш выбор: "
        ).upper()

        if status in valid_statuses:
            break
        print(f'Статус операции "{status}" недоступен.\n')

    filtered_transactions = filter_by_state(transactions, status)
    print(f'Операции отфильтрованы по статусу "{status}"')

    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    sort_choice = get_user_input("Отсортировать операции по дате? Да/Нет: ", ["да", "нет"])
    if sort_choice.lower() == "да":
        order_choice = get_user_input("Отсортировать по возрастанию или по убыванию? ", ["по возрастанию", "по убыванию"])
        descending = order_choice.lower() == "по убыванию"
        filtered_transactions = sort_by_date(filtered_transactions, descending)
        print(f"Операции отсортированы по дате ({order_choice})")

    ruble_choice = get_user_input("Выводить только рублевые транзакции? Да/Нет: ", ["да", "нет"])
    if ruble_choice.lower() == "да":
        filtered_transactions = filter_ruble_transactions(filtered_transactions)
        print("Оставлены только рублевые транзакции")

    desc_choice = get_user_input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ", ["да", "нет"])
    if desc_choice.lower() == "да":
        search_word = get_user_input("Введите слово для поиска в описании: ")
        original_count = len(filtered_transactions)
        filtered_transactions = filter_by_description(filtered_transactions, search_word)
        print(f"Найдено {len(filtered_transactions)} транзакций с словом '{search_word}' в описании")

    print("\nРаспечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(filtered_transactions)}\n")

    if filtered_transactions:
        for transaction in filtered_transactions:
            display_transaction(transaction)
    else:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")


if __name__ == "__main__":
    main()

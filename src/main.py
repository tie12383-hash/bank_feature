"""Main application module for bank_feature."""

import json
import logging
from typing import Any, Dict

from .utils import load_transactions_from_excel
from .views import main_page_data, events_page_data
from .services import (
    profitable_cashback_categories,
    investment_bank,
    simple_search,
    search_by_phone_numbers,
    search_person_transfers
)
from .reports import (
    spending_by_category,
    spending_by_weekday,
    spending_by_workday
)

logger = logging.getLogger(__name__)


class BankFeatureApp:
    """Main application class for bank_feature."""

    def __init__(self, data_file: str = "data/operations.xlsx"):
        """
        Initialize bank_feature application.

        Args:
            data_file: Path to transactions data file
        """
        self.data_file = data_file
        self.transactions_df = None
        self.transactions_list = None

    def load_data(self) -> None:
        """Load transaction data for bank_feature."""
        try:
            self.transactions_df = load_transactions_from_excel(self.data_file)

            # Convert DataFrame to list of dictionaries for services
            self.transactions_list = self.transactions_df.to_dict('records')

            logger.info("Data loaded successfully for bank_feature")
        except Exception as e:
            logger.error(f"Error loading data for bank_feature: {str(e)}")
            raise

    def generate_main_page(self, datetime_str: str) -> Dict[str, Any]:
        """
        Generate main page data for bank_feature.

        Args:
            datetime_str: Datetime string in format 'YYYY-MM-DD HH:MM:SS'

        Returns:
            Main page data as dictionary
        """
        return main_page_data(datetime_str, self.transactions_df)

    def generate_events_page(
        self,
        date_str: str,
        period: str = "M"
    ) -> Dict[str, Any]:
        """
        Generate events page data for bank_feature.

        Args:
            date_str: Date string in format 'YYYY-MM-DD'
            period: Period type (W, M, Y, ALL)

        Returns:
            Events page data as dictionary
        """
        return events_page_data(date_str, self.transactions_df, period)

    def analyze_cashback_categories(self, year: int, month: int) -> Dict[str, float]:
        """
        Analyze profitable cashback categories for bank_feature.

        Args:
            year: Year for analysis
            month: Month for analysis

        Returns:
            Cashback analysis results
        """
        return profitable_cashback_categories(self.transactions_list, year, month)

    def calculate_investment_bank(self, month: str, limit: int) -> float:
        """
        Calculate investment bank amount for bank_feature.

        Args:
            month: Month in format 'YYYY-MM'
            limit: Rounding limit

        Returns:
            Investment amount
        """
        return investment_bank(month, self.transactions_list, limit)

    def perform_simple_search(self, query: str) -> list:
        """
        Perform simple search in transactions for bank_feature.

        Args:
            query: Search query

        Returns:
            Search results
        """
        return simple_search(query, self.transactions_list)

    def find_phone_transactions(self) -> list:
        """Find transactions with phone numbers for bank_feature."""
        return search_by_phone_numbers(self.transactions_list)

    def find_person_transfers(self) -> list:
        """Find person-to-person transfers for bank_feature."""
        return search_person_transfers(self.transactions_list)

    def generate_category_report(self, category: str, date: str = None) -> Any:
        """
        Generate spending by category report for bank_feature.

        Args:
            category: Category to analyze
            date: Reference date

        Returns:
            Report results
        """
        return spending_by_category(self.transactions_df, category, date)

    def generate_weekday_report(self, date: str = None) -> Any:
        """
        Generate spending by weekday report for bank_feature.

        Args:
            date: Reference date

        Returns:
            Report results
        """
        return spending_by_weekday(self.transactions_df, date)

    def generate_workday_report(self, date: str = None) -> Any:
        """
        Generate workday/weekend spending report for bank_feature.

        Args:
            date: Reference date

        Returns:
            Report results
        """
        return spending_by_workday(self.transactions_df, date)


def main():
    """Main function to demonstrate bank_feature functionality."""
    app = BankFeatureApp()

    try:
        # Load data
        app.load_data()

        # Generate main page data
        main_data = app.generate_main_page("2024-03-15 14:30:00")
        print("Main Page Data:")
        print(json.dumps(main_data, ensure_ascii=False, indent=2))
        print("\n" + "="*50 + "\n")

        # Generate events page data
        events_data = app.generate_events_page("2024-03-15", "M")
        print("Events Page Data:")
        print(json.dumps(events_data, ensure_ascii=False, indent=2))
        print("\n" + "="*50 + "\n")

        # Analyze cashback categories
        cashback_data = app.analyze_cashback_categories(2024, 3)
        print("Cashback Analysis:")
        print(json.dumps(cashback_data, ensure_ascii=False, indent=2))
        print("\n" + "="*50 + "\n")

        # Generate reports
        category_report = app.generate_category_report("Супермаркеты")
        print("Category Report:")
        print(category_report)

    except Exception as e:
        logger.error(f"Error in bank_feature application: {str(e)}")
        print(f"Application error: {e}")


if __name__ == "__main__":
    main()

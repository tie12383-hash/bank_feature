"""Reports for transaction analysis for bank_feature."""

import json
import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Dict, Optional

import pandas as pd

logger = logging.getLogger(__name__)


def report_decorator(filename: Optional[str] = None):
    """
    Decorator for saving report results to file for bank_feature.

    Args:
        filename: Output filename (optional)
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # Generate filename if not provided
            output_file = filename or f"report_{func.__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    if isinstance(result, pd.DataFrame):
                        json.dump(result.to_dict('records'), f, ensure_ascii=False, indent=2)
                    else:
                        json.dump(result, f, ensure_ascii=False, indent=2)

                logger.info(f"Report saved to {output_file}")
            except Exception as e:
                logger.error(f"Error saving report to {output_file}: {str(e)}")

            return result

        return wrapper

    return decorator


@report_decorator
def spending_by_category(
        transactions: pd.DataFrame,
        category: str,
        date: Optional[str] = None
) -> pd.DataFrame:
    """
    Analyze spending by category for last 3 months for bank_feature.

    Args:
        transactions: DataFrame with transactions
        category: Category to analyze
        date: Reference date (default: current date)

    Returns:
        DataFrame with spending analysis
    """
    logger.info(f"Analyzing spending for category: {category}")

    try:
        # Set reference date
        if date is None:
            ref_date = datetime.now()
        else:
            ref_date = datetime.strptime(date, '%Y-%m-%d')

        # Calculate date range (last 3 months)
        start_date = (ref_date.replace(day=1) - timedelta(days=1)).replace(day=1)
        start_date = start_date.replace(day=1)

        # Filter transactions
        mask = (
                (transactions['date'] >= start_date) &
                (transactions['date'] <= ref_date) &
                (transactions['category'] == category) &
                (transactions['amount'] < 0)
        )

        filtered_df = transactions[mask].copy()
        filtered_df['amount'] = filtered_df['amount'].abs()

        # Group by month
        filtered_df['month'] = filtered_df['date'].dt.strftime('%Y-%m')
        monthly_spending = filtered_df.groupby('month')['amount'].sum().reset_index()

        return monthly_spending

    except Exception as e:
        logger.error(f"Error analyzing spending by category: {str(e)}")
        return pd.DataFrame()


@report_decorator
def spending_by_weekday(
        transactions: pd.DataFrame,
        date: Optional[str] = None
) -> pd.DataFrame:
    """
    Analyze average spending by weekday for last 3 months for bank_feature.

    Args:
        transactions: DataFrame with transactions
        date: Reference date (default: current date)

    Returns:
        DataFrame with weekday spending analysis
    """
    logger.info("Analyzing spending by weekday")

    try:
        # Set reference date
        if date is None:
            ref_date = datetime.now()
        else:
            ref_date = datetime.strptime(date, '%Y-%m-%d')

        # Calculate date range (last 3 months)
        start_date = (ref_date.replace(day=1) - timedelta(days=1)).replace(day=1)
        start_date = start_date.replace(day=1)

        # Filter transactions
        mask = (
                (transactions['date'] >= start_date) &
                (transactions['date'] <= ref_date) &
                (transactions['amount'] < 0)
        )

        filtered_df = transactions[mask].copy()
        filtered_df['amount'] = filtered_df['amount'].abs()

        # Add weekday
        filtered_df['weekday'] = filtered_df['date'].dt.day_name()

        # Calculate average spending by weekday
        weekday_spending = filtered_df.groupby('weekday')['amount'].mean().reset_index()

        # Order weekdays
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_spending['weekday'] = pd.Categorical(
            weekday_spending['weekday'], categories=weekday_order, ordered=True
        )
        weekday_spending = weekday_spending.sort_values('weekday')

        return weekday_spending

    except Exception as e:
        logger.error(f"Error analyzing spending by weekday: {str(e)}")
        return pd.DataFrame()


@report_decorator
def spending_by_workday(
        transactions: pd.DataFrame,
        date: Optional[str] = None
) -> pd.DataFrame:
    """
    Analyze average spending on workdays vs weekends for bank_feature.

    Args:
        transactions: DataFrame with transactions
        date: Reference date (default: current date)

    Returns:
        DataFrame with workday/weekend spending analysis
    """
    logger.info("Analyzing spending by workday/weekend")

    try:
        # Set reference date
        if date is None:
            ref_date = datetime.now()
        else:
            ref_date = datetime.strptime(date, '%Y-%m-%d')

        # Calculate date range (last 3 months)
        start_date = (ref_date.replace(day=1) - timedelta(days=1)).replace(day=1)
        start_date = start_date.replace(day=1)

        # Filter transactions
        mask = (
                (transactions['date'] >= start_date) &
                (transactions['date'] <= ref_date) &
                (transactions['amount'] < 0)
        )

        filtered_df = transactions[mask].copy()
        filtered_df['amount'] = filtered_df['amount'].abs()

        # Classify as workday or weekend
        filtered_df['is_weekend'] = filtered_df['date'].dt.weekday >= 5
        filtered_df['day_type'] = filtered_df['is_weekend'].map({
            True: 'weekend',
            False: 'workday'
        })

        # Calculate average spending
        day_type_spending = filtered_df.groupby('day_type')['amount'].mean().reset_index()

        return day_type_spending

    except Exception as e:
        logger.error(f"Error analyzing spending by workday: {str(e)}")
        return pd.DataFrame()
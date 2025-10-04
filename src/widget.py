"""Module for working with bank operations widget."""

from .masks import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str) -> str:
    """
    Mask card or account number in the provided string.

    Args:
        account_info: String with card or account information
                     (e.g., "Visa Platinum 7000792289606361")

    Returns:
        String with masked number
    """
    # Split string into parts
    parts = account_info.split()

    # Last element is the number
    number_str = parts[-1]

    # Everything before last element is the name
    name = " ".join(parts[:-1])

    # Determine type by name and apply appropriate masking
    if name.lower() == "счет":
        masked_number = get_mask_account(int(number_str))
    else:
        masked_number = get_mask_card_number(int(number_str))

    return f"{name} {masked_number}"


def get_date(date_string: str) -> str:
    """
    Convert date from ISO format to DD.MM.YYYY format.

    Args:
        date_string: Date in format "2024-03-11T02:26:18.671407"

    Returns:
        Date in format "11.03.2024"
    """
    # Split date and time
    date_part = date_string.split("T")[0]

    # Parse date components
    year, month, day = date_part.split("-")

    return f"{day}.{month}.{year}"

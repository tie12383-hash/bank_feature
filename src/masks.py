"""Module for masking bank cards and accounts."""


def get_mask_card_number(card_number: int) -> str:
    """
    Mask a bank card number.

    Args:
        card_number: Card number as integer

    Returns:
        Masked number in format 'XXXX XX** **** XXXX'

    Raises:
        ValueError: If card number doesn't contain 16 digits
    """
    str_number = str(card_number)
    if len(str_number) != 16:
        raise ValueError("Card number must contain 16 digits")
    return f"{str_number[:4]} {str_number[4:6]}** **** {str_number[-4:]}"


def get_mask_account(account_number: int) -> str:
    """
    Mask a bank account number.

    Args:
        account_number: Account number as integer

    Returns:
        Masked number in format '**XXXX'

    Raises:
        ValueError: If account number contains less than 4 digits
    """
    str_number = str(account_number)
    if len(str_number) < 4:
        raise ValueError("Account number must contain at least 4 digits")
    return f"**{str_number[-4:]}"

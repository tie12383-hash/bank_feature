"""Module for masking bank cards and accounts."""

from .logger_config import masks_logger


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
    masks_logger.debug(f"Starting card number masking for: {card_number}")

    str_number = str(card_number)
    if len(str_number) != 16:
        error_msg = "Card number must contain 16 digits"
        masks_logger.error(f"{error_msg}. Provided: {len(str_number)} digits")
        raise ValueError(error_msg)

    masked_number = f"{str_number[:4]} {str_number[4:6]}** **** {str_number[-4:]}"
    masks_logger.info(f"Successfully masked card number: {masked_number}")

    return masked_number


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
    masks_logger.debug(f"Starting account number masking for: {account_number}")

    str_number = str(account_number)
    if len(str_number) < 4:
        error_msg = "Account number must contain at least 4 digits"
        masks_logger.error(f"{error_msg}. Provided: {len(str_number)} digits")
        raise ValueError(error_msg)

    masked_number = f"**{str_number[-4:]}"
    masks_logger.info(f"Successfully masked account number: {masked_number}")

    return masked_number

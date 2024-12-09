"""Convert string values to numbers."""
from typing import Optional, Union


def str_to_number(value: str) -> Optional[Union[int, float]]:
    """Convert string to number (int or float).

    Args:
        value: String value to convert

    Returns:
        int or float if conversion successful, None if failed

    Examples:
        >>> str_to_number("123")
        123
        >>> str_to_number("12.34")
        12.34
        >>> str_to_number("abc")
        None
    """
    try:
        # Try converting to int first
        return int(value)
    except ValueError:
        try:
            # Try converting to float
            return float(value)
        except ValueError:
            return None

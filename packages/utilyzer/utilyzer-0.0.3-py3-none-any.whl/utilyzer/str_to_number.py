"""Convert string values to numbers."""

from typing import Any, Optional, Union


def str_to_number(value: Any) -> Optional[Union[int, float]]:
    """Convert value to number (int or float).

    Args:
        value: Value to convert, can be string or numeric type

    Returns:
        int or float if conversion successful, None if failed

    Examples:
        >>> str_to_number("123")
        123
        >>> str_to_number(123)
        123
        >>> str_to_number("12.34")
        12.34
        >>> str_to_number(None)
        None
        >>> str_to_number("abc")
        None
    """
    # Handle None case
    if value is None:
        return None

    # If already a number, return as is
    if isinstance(value, (int, float)):
        return value

    # Convert to string if not already
    if not isinstance(value, str):
        try:
            value = str(value)
        except (TypeError, ValueError):
            return None

    # Remove whitespace
    value = value.strip()

    # Handle empty string
    if not value:
        return None

    try:
        # Try converting to int first
        return int(value)
    except ValueError:
        try:
            # Try converting to float
            return float(value)
        except ValueError:
            return None

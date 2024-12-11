"""Utils related to pandas DataFrame operations for Widgets."""

import pandas as pd


def only_negative_or_positive_values(column: pd.DataFrame) -> bool:
    """Check if all values in column are negative or positive.

    Args:
        column: column to check

    Returns:
        bool: True if all values are negative or positive, False otherwise.
    """
    non_na_column = column.dropna()
    return bool(non_na_column.lt(0).all() or non_na_column.gt(0).all())


def only_positive_values(column: pd.DataFrame) -> bool:
    """Check if all values in column are positive.

    Args:
        column: column to check

    Returns:
        bool: True if all values are positive, False otherwise.
    """
    non_na_column = column.dropna()
    return bool(non_na_column.gt(0).all())


def only_negative_values(column: pd.DataFrame) -> bool:
    """Check if all values in column are negative.

    Args:
        column: column to check

    Returns:
        bool: True if all values are negative, False otherwise.
    """
    return column.lt(0).all()


def only_integers(column: pd.DataFrame) -> bool:
    """Check if all values in column are integers.

    Args:
        column: column to check

    Returns:
        bool: True if all values are integers, False otherwise.
    """
    return column.apply(lambda x: float(x).is_integer()).all()


def are_values_relative(
    column: pd.DataFrame, upper_limit: float, lower_limit: float, percentage_limit: int
) -> bool:
    """Check if values in column are relative to a range. Used to deduce percentages.

    Args:
        column: column to check
        upper_limit: upper limit of range
        lower_limit: lower limit of range
        percentage_limit: percentage limit of range

    Returns:
        bool: True if all values are relative, False otherwise.
    """
    winsorized_values = column.clip(
        column.quantile(lower_limit),
        column.quantile(upper_limit),
    )
    range_check = (winsorized_values >= -percentage_limit) & (
        winsorized_values <= percentage_limit
    )
    return ~only_integers(column) and range_check.all()

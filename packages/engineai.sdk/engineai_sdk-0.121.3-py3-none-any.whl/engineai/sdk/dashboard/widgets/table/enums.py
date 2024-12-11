"""Enums for Table Grid Widget."""

import enum

from engineai.sdk.dashboard.enum.align import HorizontalAlignment

__all__ = ["HorizontalAlignment"]


class SummaryRowPosition(enum.Enum):
    """Enum with summary row position options."""

    TOP = "TOP"
    BOTTOM = "BOTTOM"


class SummaryOperation(enum.Enum):
    """Enum with summary operations."""

    SUM = "SUM"
    AVG = "AVG"
    MIN = "MIN"
    MAX = "MAX"
    COUNT = "COUNT"
    COUNT_UNIQUE = "COUNT_UNIQUE"

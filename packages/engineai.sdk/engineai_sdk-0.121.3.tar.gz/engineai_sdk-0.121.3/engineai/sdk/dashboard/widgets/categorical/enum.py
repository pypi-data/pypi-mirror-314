"""Categorical chart enums."""

import enum


class ChartDirection(enum.Enum):
    """Options for directions of categorical chart.

    Attributes:
        VERTICAL: Chart with a vertical direction.
        HORIZONTAL: Chart with a horizontal direction.
    """

    VERTICAL = "VERTICAL"
    HORIZONTAL = "HORIZONTAL"

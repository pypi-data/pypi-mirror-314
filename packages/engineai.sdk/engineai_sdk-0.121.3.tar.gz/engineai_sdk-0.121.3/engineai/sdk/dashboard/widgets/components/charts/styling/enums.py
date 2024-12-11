"""Enums for Timeseries series styling."""

import enum


class DashStyle(enum.Enum):
    """Enum to specify dash style of lines.

    Attributes:
        SOLID: Solid line.
        DOT: Dotted line.
        DASH: Dashed line.
        SHORT_DASH: Short dashed line.
        LONG_DASH: Long dashed line.
        SHORT_DASH_DOT: Short dashed dotted line.
        LONG_DASH_DOT: Long dashed dotted line.

    """

    SOLID = "SOLID"
    DOT = "DOT"
    DASH = "DASH"
    SHORT_DASH = "SHORT_DASH"
    LONG_DASH = "LONG_DASH"
    SHORT_DASH_DOT = "SHORT_DASH_DOT"
    LONG_DASH_DOT = "LONG_DASH_DOT"


class MarkerSymbol(enum.Enum):
    """Enum to specify marker symbol.

    Attributes:
        CROSS: Cross symbol.
        TRIANGLE: Triangle symbol.
        CIRCLE: Circle symbol.
        DIAMOND: Diamond symbol.
        SQUARE: Square symbol.
        TRIANGLE_DOWN: Triangle down symbol.
    """

    CROSS = "CROSS"
    TRIANGLE = "TRIANGLE"
    CIRCLE = "CIRCLE"
    DIAMOND = "DIAMOND"
    SQUARE = "SQUARE"
    TRIANGLE_DOWN = "TRIANGLE_DOWN"

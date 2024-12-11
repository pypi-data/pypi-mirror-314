"""Spec for Tile Widget Orientation Enum."""

import enum


class Orientation(enum.Enum):
    """Options for orientation of Tile Widget.

    Attributes:
        VERTICAL (str): Vertical orientation.
        HORIZONTAL (str): Horizontal orientation.
    """

    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"

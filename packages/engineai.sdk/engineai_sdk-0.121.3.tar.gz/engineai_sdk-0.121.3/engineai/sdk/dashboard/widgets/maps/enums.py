"""Specs for Position and Region."""

import enum


class LegendPosition(enum.Enum):
    """Legend positioning options on map.

    Options for positioning the legend on the map,
    including top, left, right, and bottom.

    Attributes:
        TOP: Legend is placed on the top of the map.
        LEFT: Legend is placed on the left side of the map.
        RIGHT: Legend is placed on the right side of the map.
        BOTTOM: Legend is placed on the bottom of the map.
    """

    TOP = "TOP"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    BOTTOM = "BOTTOM"


class Region(enum.Enum):
    """Region options for map.

    Options for defining the region of the map,
    such as world, Europe, USA, and North America.

    Attributes:
        WORLD: World region.
        EUROPE: Europe region.
        USA: USA region.
        NORTH_AMERICA: North America region.
        SAUDI_ARABIA: Saudi Arabia region.
    """

    WORLD = "WORLD"
    EUROPE = "EUROPE"
    USA = "USA"
    NORTH_AMERICA = "NORTH_AMERICA"
    SAUDI_ARABIA = "SAUDI_ARABIA"

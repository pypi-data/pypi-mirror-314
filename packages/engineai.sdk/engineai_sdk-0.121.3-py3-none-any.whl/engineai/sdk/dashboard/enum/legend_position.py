"""Legend position enum."""

import enum


class LegendPosition(enum.Enum):
    """Chart legend position options.

    Options for positions of charts legend.

    Attributes:
        RIGHT (str): Legend is placed to the right of the chart.
        BOTTOM (str): Legend is placed below the chart.
        RIGHT_GROUPED (str): Legend is placed to the right of the chart
            and grouped with other legends.
        BOTTOM_GROUPED (str): Legend is placed below the chart
            and grouped with other legends.
        NEXT_TO_DATA (str): Legend is placed next to the data.
    """

    RIGHT = "RIGHT"
    BOTTOM = "BOTTOM"
    RIGHT_GROUPED = "RIGHT_GROUPED"
    BOTTOM_GROUPED = "BOTTOM_GROUPED"
    NEXT_TO_DATA = "NEXT_TO_DATA"

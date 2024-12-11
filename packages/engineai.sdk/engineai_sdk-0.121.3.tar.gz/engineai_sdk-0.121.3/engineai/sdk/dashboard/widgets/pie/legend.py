"""Spec for Legend position and respective build."""

import enum
from typing import Any
from typing import Dict


class LegendPosition(enum.Enum):
    """Legend position options.

    Options for positioning the legend on the pie chart,
    including right, bottom, and next to the data.

    Attributes:
        RIGHT: Legend is placed on the right side of the chart.
        BOTTOM: Legend is placed on the bottom of the chart.
        NEXT_TO_DATA: Legend is placed next to the data.
    """

    RIGHT = "RIGHT"
    BOTTOM = "BOTTOM"
    NEXT_TO_DATA = "NEXT_TO_DATA"


def build_legend(legend: LegendPosition) -> Dict[str, Any]:
    """Builds spec for dashboard API.

    Returns:
        Input object for Dashboard API
    """
    return {
        "position": legend.value,
    }

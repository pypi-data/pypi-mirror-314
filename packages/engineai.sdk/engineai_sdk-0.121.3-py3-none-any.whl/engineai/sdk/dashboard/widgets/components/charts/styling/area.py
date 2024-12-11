"""Spec to style an area series."""

from typing import Optional

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.styling.color.typing import ColorSpec
from engineai.sdk.dashboard.templated_string import TemplatedStringItem

from .base import BaseChartSeriesStyling
from .enums import MarkerSymbol


class AreaSeriesStyling(BaseChartSeriesStyling):
    """Customize appearance of filled areas in Charts.

    Specify styling options for an area series within a Chart
    widget to customize the appearance of filled areas on the chart.
    """

    @type_check
    def __init__(
        self,
        *,
        color_spec: ColorSpec,
        data_column: Optional[TemplatedStringItem] = None,
        marker_symbol: MarkerSymbol = MarkerSymbol.CIRCLE,
    ) -> None:
        """Constructor for AreaSeriesStyling.

        Args:
            color_spec: spec for coloring area.
            data_column: name of column in pandas dataframe(s) used for color spec if
                a gradient is used. Optional for single colors.
            marker_symbol: symbol for marker in tooltips and legends.

        Raises:
            ChartStylingMissingDataColumnError: if color_spec is
                ColorDiscreteMap/ColorGradient and data_column
                has not been specified
        """
        super().__init__(
            color_spec=color_spec, data_column=data_column, marker_symbol=marker_symbol
        )

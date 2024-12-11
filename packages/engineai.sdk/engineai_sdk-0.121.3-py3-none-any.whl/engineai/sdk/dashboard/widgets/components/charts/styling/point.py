"""Spec to style a point series."""

from typing import Optional

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.styling.color.typing import ColorSpec
from engineai.sdk.dashboard.templated_string import TemplatedStringItem

from .base import BaseChartSeriesStyling
from .enums import MarkerSymbol


class PointSeriesStyling(BaseChartSeriesStyling):
    """Customize appearance of data points in Chart.

    Specify styling options for a point series within a Chart
    widget to customize the appearance of individual
    data points on the chart.
    """

    @type_check
    def __init__(
        self,
        *,
        color_spec: ColorSpec,
        data_column: Optional[TemplatedStringItem] = None,
        marker_symbol: MarkerSymbol = MarkerSymbol.CIRCLE,
    ) -> None:
        """Constructor for PointSeriesStyling.

        Args:
            color_spec: spec for coloring columns.
            data_column: name of column in pandas dataframe(s) used for color spec if
                a gradient is used. Optional for single colors.
            marker_symbol: symbol for each point.

        Raises:
            ChartStylingMissingDataColumnError: if a data_column is not defined when
                color_spec is a ColorDiscreteMap or ColorGradient
        """
        super().__init__(
            color_spec=color_spec, data_column=data_column, marker_symbol=marker_symbol
        )

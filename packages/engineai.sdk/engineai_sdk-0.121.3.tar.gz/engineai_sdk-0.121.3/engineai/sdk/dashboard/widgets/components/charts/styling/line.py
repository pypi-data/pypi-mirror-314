"""Spec to style a line series."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union
from typing import get_args

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.styling import color
from engineai.sdk.dashboard.styling.color.typing import ColorSpec
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.items.styling.exceptions import (
    ItemStylingValidationError,
)
from engineai.sdk.dashboard.widgets.components.items.styling.exceptions import (
    StylingInvalidDashValuesError,
)

from .base import BaseChartSeriesStyling
from .enums import DashStyle
from .enums import MarkerSymbol


class LineSeriesStyling(BaseChartSeriesStyling):
    """Customize appearance of lines in Chart.

    Specify styling options for a line series within a Chart widget
    to customize the appearance of the lines connecting data points on the chart.
    """

    @type_check
    def __init__(
        self,
        *,
        color_spec: Optional[ColorSpec] = None,
        data_column: Optional[TemplatedStringItem] = None,
        dash_style: Union[DashStyle, TemplatedStringItem] = DashStyle.SOLID,
        marker_symbol: MarkerSymbol = MarkerSymbol.CIRCLE,
        width: int = 2,
    ) -> None:
        """Constructor for LineSeriesStyling.

        Args:
            color_spec: spec for coloring area.
            data_column: name of column in pandas dataframe(s) used for color spec if
                a gradient is used. Optional for single colors.
            dash_style: dash style of line.
            marker_symbol: symbol for marker in tooltips and legends.
            width: width of line.

        Raises:
            ChartStylingMissingDataColumnError: if a data_column is not defined when
                color_spec is a ColorDiscreteMap or ColorGradient
        """
        super().__init__(
            color_spec=color_spec or color.Palette.MINT_GREEN,
            data_column=data_column,
            marker_symbol=marker_symbol,
        )
        self.__dash_style = dash_style
        self.__width = width

    def validate(
        self,
        *,
        data: pd.DataFrame,
    ) -> None:
        """Validate data."""
        super().validate(data=data)
        self.__validate_dash_style_data(data)

    def __validate_dash_style_data(self, data: pd.DataFrame) -> None:
        if isinstance(self.__dash_style, str):
            if self.__dash_style not in data.columns:
                raise ItemStylingValidationError(
                    class_name=self.__class__.__name__,
                    column_name="dash_style",
                    column_value=self.__dash_style,
                )
            if (
                not data[self.__dash_style]
                .isin([x.value for x in list(DashStyle)])
                .all()
            ):
                raise StylingInvalidDashValuesError(
                    class_name=self.__class__.__name__,
                    column_name="dash_style",
                    column_value=self.__dash_style,
                )

    def _build_extra_fields(self) -> Dict[str, Any]:
        result = {"width": self.__width}

        if isinstance(self.__dash_style, DashStyle):
            result["dashStyle"] = self.__dash_style.value
        elif isinstance(self.__dash_style, get_args(TemplatedStringItem)):
            result["dashStyleKey"] = build_templated_strings(items=self.__dash_style)
            result["dashStyle"] = DashStyle.SOLID.value

        return result

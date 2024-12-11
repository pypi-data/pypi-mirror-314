"""Specification for styling a column chart."""

from typing import Optional
from typing import Union

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.styling.color.typing import ColorSpec

from .base import TableSparklineColumnStylingBase


class ColumnChartStyling(TableSparklineColumnStylingBase):
    """Styling options for column chart column.

    Specify the styling options for a column chart column in
    the table widget, including color and data key.
    """

    @type_check
    def __init__(
        self,
        *,
        color_spec: ColorSpec,
        data_key: Optional[Union[str, WidgetField]] = None,
    ) -> None:
        """Constructor for ColumnChartStyling.

        Args:
            data_key: Dictionary key, stored in data, that is used for chart.
                By default, will use values of column to which styling is applied.
            color_spec: spec for color of column chart.
        """
        super().__init__(
            data_column=data_key,
            color_spec=color_spec,
        )

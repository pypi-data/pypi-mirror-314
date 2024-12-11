"""Specification for styling the stacked bar column."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.styling.color import DiscreteMap
from engineai.sdk.dashboard.styling.color.spec import build_color_spec

from .base import TableSparklineColumnStylingBase


class StackedBarStyling(TableSparklineColumnStylingBase):
    """Styling options for stacked bar column.

    Specify the styling options for a stacked bar column in
    the table widget, including color, data column, and total display.
    """

    @type_check
    def __init__(
        self,
        *,
        color_spec: DiscreteMap,
        data_column: Optional[Union[str, WidgetField]] = None,
    ) -> None:
        """Constructor for StackedBarStyling.

        Args:
            data_column: id of column which values are used for chart.
            color_spec: spec for discrete color map of stacked bar column chart.
        """
        super().__init__(
            data_column=data_column,
            color_spec=color_spec,
        )

    def _build_color_spec(self) -> Dict[str, Any]:
        return (
            {
                "colorSpec": build_color_spec(spec=self.color_spec),
            }
            if self.color_spec is not None
            else {}
        )

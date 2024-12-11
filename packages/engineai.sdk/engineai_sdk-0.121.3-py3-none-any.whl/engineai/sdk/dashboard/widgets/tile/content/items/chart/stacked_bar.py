"""Spec for Tile Widget Stacked Bat Chart Item."""

from typing import Any
from typing import Dict
from typing import Mapping
from typing import Optional
from typing import Union

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting.number import NumberFormatting
from engineai.sdk.dashboard.styling.color.palette import Palette
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.items.styling import (
    StackedBarChartItemStyling,
)

from .base import BaseTileChartItem


class StackedBarChartItem(BaseTileChartItem):
    """Spec for Tile Stack Bar Chart Item."""

    _API_CHART_TYPE = "stackedBar"

    @type_check
    def __init__(
        self,
        *,
        data_column: TemplatedStringItem,
        bar_label_key: TemplatedStringItem,
        styling: Optional[Union[Palette, StackedBarChartItemStyling]] = None,
        formatting: Optional[NumberFormatting] = None,
        label: Optional[TemplatedStringItem] = None,
        required: bool = True,
    ) -> None:
        """Construct spec for the TileColumnChartItem class.

        Args:
            data_column: key in data that will have the values used by the item.
            bar_label_key: key in data that will have the labels used by each bar.
            styling: styling spec for item charts.
            formatting: formatting spec.
            label: str that will label the item values.
            required: Flag to make Number item mandatory. If required is True
                and no Data the widget will show an error. If
                required is False and no Data, the item is not shown.
        """
        super().__init__(
            styling=(
                StackedBarChartItemStyling(color_spec=styling)
                if isinstance(styling, Palette)
                else (
                    StackedBarChartItemStyling(color_spec=Palette.AQUA_GREEN)
                    if styling is None
                    else styling
                )
            ),
            data_column=data_column,
            formatting=formatting,
            label=label,
            required=required,
        )
        self.__bar_label_key = bar_label_key

    def validate(self, data: Dict[str, Any]) -> None:
        """Validates Tile Item.

        Args:
            widget_id (str): id of Tile Widget.
            data (Dict[str, Any]): Dict where the data is present.
        """
        super().validate(data)
        if (
            isinstance(self._data_column, str)
            and isinstance(data[self._data_column], list)
            and isinstance(self.__bar_label_key, str)
            and isinstance(data[self.__bar_label_key], list)
        ) and len(data[self._data_column]) != len(data[self.__bar_label_key]):
            msg = (
                f"Data column and bar label key must have the same length. "
                f"Data column length: {len(data[self._data_column])}. "
                f"Bar label key length: {len(data[self.__bar_label_key])}."
            )
            raise ValueError(msg)

    def _build_extra_chart_inputs(self) -> Mapping[str, Any]:
        return {"barLabelKey": build_templated_strings(items=self.__bar_label_key)}

"""Spec for Widget Stacked Bar Chart Tooltip."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.templated_string import DataField
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.charts.tooltip.base import (
    TooltipItemFormatter,
)
from engineai.sdk.dashboard.widgets.components.charts.tooltip.item import (
    build_tooltip_item,
)
from engineai.sdk.dashboard.widgets.components.charts.typing import TooltipItem

from .tooltip import ChartTooltip


class StackedBarTooltipItem(AbstractFactory):
    """Spec for Widget Stacked Bar Chart Tooltip Item."""

    def __init__(self, data_key: TemplatedStringItem, item: TooltipItem) -> None:
        """Construct for StackedBarTooltipItem class.

        Args:
            data_key: key in object that contains the data.
            item: tooltip item spec.
        """
        self.__data_key = data_key
        self.__item = item

    def build(self) -> Any:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "dataKey": build_templated_strings(items=self.__data_key),
            "item": build_tooltip_item(self.__item),
        }


class StackedBarTooltip(ChartTooltip):
    """Spec for Widget Stacked Bar Chart Tooltip."""

    def __init__(
        self,
        title: Union[str, DataField],
        items: List[StackedBarTooltipItem],
        formatting: Optional[TooltipItemFormatter] = None,
        show_total: bool = False,
    ) -> None:
        """Construct for StackedBarTooltip class.

        Args:
            title: header title spec.
            items: list of items in tooltip.
            formatting: header tooltip formatting.
            show_total: flag to show total in tooltip.
        """
        super().__init__(title=title, formatting=formatting)
        self.__items = items
        self.__show_total = show_total

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Any: Input object for Dashboard API
        """
        return {
            "header": self._header.build(),
            "items": [item.build() for item in self.__items],
            "showTotal": self.__show_total,
        }

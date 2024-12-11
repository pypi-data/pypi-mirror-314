"""Spec for Base Tile Chart Items."""

from typing import Any
from typing import Dict
from typing import Mapping
from typing import Optional
from typing import Union

from engineai.sdk.dashboard.formatting.number import NumberFormatting
from engineai.sdk.dashboard.templated_string import DataField
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.items.styling import AreaChartItemStyling
from engineai.sdk.dashboard.widgets.components.items.styling import (
    ColumnChartItemStyling,
)
from engineai.sdk.dashboard.widgets.components.items.styling import LineChartItemStyling
from engineai.sdk.dashboard.widgets.components.items.styling import (
    StackedBarChartItemStyling,
)
from engineai.sdk.dashboard.widgets.tile.content.items.base import BaseTileContentItem

TileChartStyling = Union[
    AreaChartItemStyling,
    LineChartItemStyling,
    ColumnChartItemStyling,
    StackedBarChartItemStyling,
]


class BaseTileChartItem(BaseTileContentItem):
    """Spec for Base Tile Chart Items."""

    _INPUT_KEY = "chart"

    _API_CHART_TYPE: Optional[str] = None

    def __init__(
        self,
        *,
        styling: TileChartStyling,
        data_column: TemplatedStringItem,
        formatting: Optional[NumberFormatting] = None,
        label: Optional[Union[TemplatedStringItem, DataField]] = None,
        required: bool = True,
    ) -> None:
        """Construct spec for the BaseTileChartItem class.

        Args:
            styling: styling spec for item charts.
            data_column: key in data that will have the values used by the item.
            formatting: formatting spec.
            label: str that will label the item values.
            required: Flag to make Number item mandatory. If required is True
                and no Data the widget will show an error. If
                required is False and no Data, the item is not shown.
        """
        super().__init__(
            data_column=data_column,
            formatting=formatting if formatting is not None else NumberFormatting(),
            label=label,
            required=required,
        )
        self.__styling = styling

    def prepare(self) -> None:
        """Prepares styling spec for dashboard API."""
        if self.__styling is not None:
            self.__styling.prepare(self._data_column)

    @property
    def _api_chart_type(self) -> str:
        """Returns API Type."""
        if self._API_CHART_TYPE is None:
            msg = (
                f"Class {self.__class__.__name__} does not have the variable "
                f"`_API_CHART_TYPE` initialized. Please add the proper value "
                f"or overwrite this method {self.__class__.__name__}._api_chart_type."
            )
            raise ValueError(msg)
        return self._API_CHART_TYPE

    def _build_configuration(self) -> Dict[str, Any]:
        """Builds configuration spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {self._api_chart_type: self._build_chart()}

    def _build_extra_chart_inputs(self) -> Mapping[str, Any]:
        """Builds extra inputs for chart spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {}

    def _build_chart(self) -> Dict[str, Any]:
        """Builds chart spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            "valueKey": build_templated_strings(items=self._data_column),
            "styling": self.__styling.build(),
            "label": self._label.build() if self._label else None,
            **self._build_extra_chart_inputs(),
        }

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "configuration": self._build_configuration(),
            "formatting": self._formatting.build(),
            "required": self._required,
        }

    def validate(self, data: Dict[str, Any]) -> None:
        """Validates Tile Item.

        Args:
            widget_id (str): id of Tile Widget.
            data (Dict[str, Any]): Dict where the data is present.
        """
        super().validate(data=data)
        if self.__styling is not None:
            self.__styling.validate(data=data, column_name="data_key")

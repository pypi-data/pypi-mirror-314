"""Spec for Pie Tooltip."""

from typing import Any
from typing import Dict
from typing import Optional

import pandas as pd

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.charts.tooltip.item import (
    build_tooltip_item,
)
from engineai.sdk.dashboard.widgets.components.charts.typing import TooltipItems
from engineai.sdk.dashboard.widgets.utils import build_data


class Tooltip(AbstractFactory):
    """Spec for Pie Tooltip."""

    def __init__(
        self,
        category_column: TemplatedStringItem,
        tooltips: Optional[TooltipItems] = None,
    ) -> None:
        """Constructor for Pie Tooltip.

        Args:
            category_column: name of column in pandas dataframe(s)
                that has category info within the pie.
            tooltips: tooltip items to be displayed at Chart level.
        """
        self._tooltips = (
            tooltips
            if isinstance(tooltips, list)
            else []
            if tooltips is None
            else [tooltips]
        )
        self._category_column = category_column
        self._dependency_id: str = " "
        self._json_data: Any = None

    def prepare(self, dependency_id: str, json_data: Any = None) -> None:
        """Prepare Widget Spec to be validated.

        Args:
            dependency_id: widget dependency id.
            json_data: json data object.
        """
        self._dependency_id = dependency_id
        self._json_data = json_data

    def validate(
        self,
        data: pd.DataFrame,
    ) -> None:
        """Validate tooltips.

        Args:
            data: data associated to path
        """
        for tooltip in self._tooltips:
            tooltip.validate(data=data)

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            "items": [build_tooltip_item(item=item) for item in self._tooltips],
            "data": build_data(path=self._dependency_id, json_data=self._json_data),
            "categoryIdKey": build_templated_strings(items=self._category_column),
        }

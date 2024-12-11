"""Spec for Pie Series."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting.number import NumberFormatting
from engineai.sdk.dashboard.links.abstract import AbstractFactoryLinkItemsHandler
from engineai.sdk.dashboard.styling.color import Palette
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.charts.tooltip.item import (
    build_tooltip_item,
)
from engineai.sdk.dashboard.widgets.components.charts.typing import TooltipItem
from engineai.sdk.dashboard.widgets.components.charts.typing import TooltipItems
from engineai.sdk.dashboard.widgets.pie.exceptions import PieValidateValueError
from engineai.sdk.dashboard.widgets.utils import build_data

from .styling import SeriesStyling


class BaseSeries(AbstractFactoryLinkItemsHandler):
    """Spec for BaseSeries."""

    _INPUT_KEY: Optional[str] = None

    @type_check
    def __init__(
        self,
        *,
        name: TemplatedStringItem,
        category_column: TemplatedStringItem,
        data_column: TemplatedStringItem,
        formatting: Optional[NumberFormatting] = None,
        styling: Optional[Union[Palette, SeriesStyling]] = None,
        tooltips: Optional[TooltipItems] = None,
    ) -> None:
        """Construct spec for Pie Series.

        Args:
            name: name for the Pie series.
            category_column: name of column in pandas dataframe(s) that has category
                info within the pie.
            data_column: name of column in pandas dataframe(s) that has pie data.
            formatting: spec for number formatting.
            styling: spec for pie series styling.
            tooltips: tooltip items to be displayed at Series level.
        """
        super().__init__()
        self._name = name
        self._category_column = category_column
        self._data_column = data_column
        self._formatting = formatting if formatting else NumberFormatting()
        self._styling = (
            styling
            if isinstance(styling, SeriesStyling)
            else (
                SeriesStyling(color_spec=styling)
                if isinstance(styling, Palette)
                else styling
            )
        )
        self._tooltip_items: List[TooltipItem] = (
            tooltips
            if isinstance(tooltips, list)
            else ([tooltips] if tooltips is not None else [])
        )
        self._dependency_id: str = " "
        self._json_data: Any = None

    @property
    def _input_key(self) -> str:
        """Returns styling Input Key argument value."""
        if self._INPUT_KEY is None:
            msg = f"Class {self.__class__.__name__}._INPUT_KEY not defined."
            raise NotImplementedError(msg)
        return self._INPUT_KEY

    @property
    def category_column(self) -> TemplatedStringItem:
        """Returns column used for id of destination node.

        Returns:
            TemplatedStringItem: column used for id of destination node
        """
        return self._category_column

    def _validate_field(
        self,
        data: pd.DataFrame,
        field: str,
        item: Optional[TemplatedStringItem] = None,
    ) -> None:
        if item is not None and str(item) not in data.columns:
            raise PieValidateValueError(
                subclass=self.__class__.__name__,
                argument=field,
                value=str(item),
            )

    def prepare(self, dependency_id: str, json_data: Any = None) -> None:
        """Prepare Widget Spec to be validated.

        Args:
            dependency_id: widget dependency id.
            json_data: json data object.
        """
        self._dependency_id = dependency_id
        self._json_data = json_data

        if self._styling is not None:
            self._styling.prepare(self._data_column)

    def validate(
        self,
        *,
        data: pd.DataFrame,
    ) -> None:
        """Validates Pie Series Widget and the inner components specs."""
        self._validate_field(
            data=data,
            field="data_column",
            item=self._data_column,
        )
        for tooltip in self._tooltip_items:
            tooltip.validate(data=data)

        if self._styling is not None:
            self._styling.validate(data=data)

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            self._input_key: self._build_series(),
        }

    def _build_series(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            "name": build_templated_strings(items=self._name),
            "valueKey": build_templated_strings(items=self._data_column),
            "formatting": self._formatting.build(),
            "data": build_data(path=self._dependency_id, json_data=self._json_data),
            "styling": self._styling.build() if self._styling is not None else None,
            "tooltipItems": [
                build_tooltip_item(item=item) for item in self._tooltip_items
            ],
            **self._build_category_key(),
        }

    def _build_category_key(self) -> Dict[str, Any]:
        return {
            "categoryIdKey": build_templated_strings(items=self._category_column),
        }

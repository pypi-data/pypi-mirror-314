"""Spec for a Base Series class of a Categorical widget."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import TypeVar
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.links.typing import GenericLink
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.charts.series.base import ChartSeriesBase
from engineai.sdk.dashboard.widgets.components.charts.tooltip.item import (
    build_tooltip_item,
)
from engineai.sdk.dashboard.widgets.components.charts.typing import TooltipItem

from ..exceptions import CategoricalValidateDataColumnNotFoundError

CategoricalSeriesT = TypeVar(  # pylint: disable=typevar-name-incorrect-variance
    "CategoricalSeriesT", bound="CategoricalBaseSeries", covariant=True
)


class CategoricalBaseSeries(ChartSeriesBase):
    """Spec for a Base Series class of a Categorical widget."""

    _INPUT_KEY: Optional[str] = None

    @type_check
    def __init__(
        self,
        *,
        data_column: Optional[Union[str, GenericLink]] = None,
        name: Optional[Union[str, GenericLink]] = None,
        show_in_legend: bool = True,
        required: bool = True,
        visible: bool = True,
        tooltips: Optional[List[TooltipItem]] = None,
    ) -> None:
        """Construct CategoricalBaseSeries.

        Args:
            data_column: name of column in pandas dataframe(s) used for the values
                of this series for the Y Axis.
            name: series name (shown in legend and tooltip).
            show_in_legend: whether to show series in legend or not.
            required: Flag to make the Series mandatory. If required == True
                and no Data the widget will show an error. If required==False and no
                Data, the widget hides the Series.
            visible: Flag to make the Series visible when chart is loaded.
            tooltips: Tooltip items to show in the series.
        """
        super().__init__(name=name, data_column=data_column)
        self._data_column = data_column
        self._category_data_column: Union[str, GenericLink] = ""
        self._show_in_legend = show_in_legend
        self._tooltip_items = tooltips if tooltips is not None else []
        self._required = required
        self._visible = visible
        self._styling: Optional[Any] = None

    @property
    def _input_key(self) -> str:
        """Returns styling Input Key argument value."""
        if self._INPUT_KEY is None:
            msg = f"Class {self.__class__.__name__}._INPUT_KEY not defined."
            raise NotImplementedError(msg)
        return self._INPUT_KEY

    def _build_extra_inputs(self) -> Dict[str, Any]:
        return {}

    def prepare(
        self,
        data_column: Union[str, GenericLink],
    ) -> None:
        """Prepare the Series for use.

        Args:
            data_column (Union[str, GenericLink]): data column for the Series.
            index (int): index of the Series in the Chart.
            chart_length (int): id of the dependency where this Series is used.
            palette (Optional[PaletteTypes]): palette for the Series.
                Defaults to None.
        """
        self._category_data_column = data_column
        if self._styling is not None:
            self._styling.prepare(self._data_column)

    def validate(self, data: pd.DataFrame, **kwargs: Any) -> None:
        """Validate Series elements and Data.

        Args:
            data: Data associated with the Series.

        Raises:
            ValueError:
                - if missing dependency for each band or line.
        """
        self._validate_data_column(
            widget_data=data,
            kwargs=kwargs,
            data_column=self._data_column,
            data_column_name="data_column",
        )

        for item in self._tooltip_items:
            item.validate(data=data)

    def _validate_data_column(
        self,
        widget_data: pd.DataFrame,
        kwargs: Any,
        data_column: Optional[Union[str, GenericLink]],
        data_column_name: str,
    ) -> None:
        if isinstance(data_column, WidgetField):
            data_column.validate(
                data=widget_data,
                storage=kwargs["storage"],
                data_column_name=data_column_name,
            )
        elif isinstance(data_column, str) and data_column not in widget_data.columns:
            raise CategoricalValidateDataColumnNotFoundError(
                series_class_name=self.__class__.__name__,
                column_value=data_column,
                column_name=data_column_name,
            )

    def _build_series(self) -> Dict[str, Any]:
        return {
            "name": build_templated_strings(items=self.name),
            "styling": self._styling.build() if self._styling else None,
            "categoryIdKey": build_templated_strings(items=self._category_data_column),
            "showInLegend": self._show_in_legend,
            "required": self._required,
            "isVisible": self._visible,
            "tooltipItems": [
                build_tooltip_item(item=item) for item in self._tooltip_items
            ],
            **self._build_extra_inputs(),
            **self.__build_value_key(),
        }

    def __build_value_key(self) -> Dict[str, Any]:
        return (
            {"valueKey": build_templated_strings(items=self._data_column)}
            if self._data_column is not None
            else {}
        )

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            self._input_key: self._build_series(),
        }

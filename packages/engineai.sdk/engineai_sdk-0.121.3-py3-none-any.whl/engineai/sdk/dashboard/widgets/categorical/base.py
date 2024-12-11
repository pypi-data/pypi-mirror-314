"""Spec for Base Categorical widget."""

from typing import Any
from typing import List
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.data.decorator import DataSource
from engineai.sdk.dashboard.data.http import Http
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.enum.legend_position import LegendPosition
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.widgets.base import Widget
from engineai.sdk.dashboard.widgets.base import WidgetTitleType
from engineai.sdk.dashboard.widgets.categorical.axis.typing import ValueAxisSeries
from engineai.sdk.dashboard.widgets.categorical.chart import Chart
from engineai.sdk.dashboard.widgets.components.charts.tooltip.item import TooltipItem

from .axis.category import CategoryAxis
from .axis.value import ValueAxis
from .enum import ChartDirection


class CategoricalBase(Widget):
    """Spec for Base Categorical widget."""

    _WIDGET_API_TYPE = "categoricalCartesian"
    _DEPENDENCY_ID = "__CATEGORICAL_DATA_DEPENDENCY__"

    @type_check
    def __init__(
        self,
        *,
        data: Union[DataSource, pd.DataFrame, Http],
        category_axis: Union[str, WidgetField, CategoryAxis] = "category",
        value_axis: Optional[Union[ValueAxisSeries, ValueAxis]] = None,
        secondary_value_axis: Optional[Union[ValueAxisSeries, ValueAxis]] = None,
        widget_id: Optional[str] = None,
        legend_position: Optional[LegendPosition] = None,
        title: Optional[WidgetTitleType] = None,
        enable_toolbar: bool = True,
        direction: ChartDirection = ChartDirection.VERTICAL,
        tooltips: Optional[List[TooltipItem]] = None,
    ) -> None:
        """Construct spec for a Categorical widget.

        Args:
            data: data source for the widget.
            category_axis: spec for category axis.
            value_axis: spec for main value axis.
            secondary_value_axis: Spec for secondary value axis.
            widget_id: unique widget id in a dashboard.
            legend_position: legend of Categorical widget.
            title: title of widget can be either a string (fixed value) or determined
                by a value from another widget using a WidgetField.
            enable_toolbar: Enable/Disable toolbar flag.
            direction: option to set the direction for series in the Chart.
            tooltips: list of tooltip items to be displayed on hover.
        """
        super().__init__(widget_id=widget_id, data=data)
        self._title = title
        self._chart = Chart(
            data=data if isinstance(data, pd.DataFrame) else None,
            category_axis=category_axis,
            value_axis=value_axis,
            secondary_value_axis=secondary_value_axis,
            direction=direction,
            tooltips=tooltips,
        )
        self._legend_position = legend_position
        self._enable_toolbar = enable_toolbar

    def _validate_dataframe(self, data: pd.DataFrame, **kwargs: Any) -> None:
        self._chart.validate(data=data, **kwargs)

    def _prepare(self, **kwargs: object) -> None:
        self._chart.prepare(dependency_id=self.dependency_id)
        self._json_data = kwargs.get("json_data")

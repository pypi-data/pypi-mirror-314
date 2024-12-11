"""Spec for Categorical widget."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.data.decorator import DataSource
from engineai.sdk.dashboard.data.http import Http
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.enum import LegendPosition
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.base import WidgetTitleType
from engineai.sdk.dashboard.widgets.categorical.axis.typing import ValueAxisSeries
from engineai.sdk.dashboard.widgets.components.charts.toolbar import build_chart_toolbar
from engineai.sdk.dashboard.widgets.components.charts.tooltip.item import TooltipItem
from engineai.sdk.dashboard.widgets.utils import build_data

from .axis.category import CategoryAxis
from .axis.value import ValueAxis
from .base import CategoricalBase
from .enum import ChartDirection


class Categorical(CategoricalBase):
    """Spec for Categorical widget."""

    @type_check
    def __init__(
        self,
        data: Union[DataSource, pd.DataFrame, Http],
        *,
        category_axis: Union[str, WidgetField, CategoryAxis] = "category",
        value_axis: Optional[Union[ValueAxisSeries, ValueAxis]] = None,
        secondary_value_axis: Optional[Union[ValueAxisSeries, ValueAxis]] = None,
        widget_id: Optional[str] = None,
        legend_position: LegendPosition = LegendPosition.BOTTOM,
        title: Optional[WidgetTitleType] = None,
        enable_toolbar: bool = True,
        direction: ChartDirection = ChartDirection.VERTICAL,
        tooltips: Optional[List[TooltipItem]] = None,
    ) -> None:
        """Construct spec for a Categorical widget.

        Args:
            data: data source for the widget.
            widget_id: unique widget id in a dashboard.
            category_axis: spec for category axis.
            value_axis: spec for main value axis.
            secondary_value_axis: Spec for secondary value axis.
            legend_position: legend of Categorical widget.
            title: title of widget can be either a string (fixed value) or determined
                by a value from another widget using a WidgetField.
            enable_toolbar: Enable/Disable toolbar flag.
            direction: option to set the direction
                for series in the Chart.
            tooltips: list of tooltip items.

        Examples:
            ??? example "Create a minimal Categorical widget"
                ```python linenums="1"
                import pandas as pd
                from engineai.sdk.dashboard import dashboard
                from engineai.sdk.dashboard.widgets import categorical
                data = pd.DataFrame(
                    [
                        {"category": "CAT 1", "value": 100, "value_2": 1999},
                        {"category": "CAT 2", "value": 200, "value_2": 2999},
                    ]
                )
                categorical_widget = categorical.Categorical(data=data)
                dashboard.Dashboard(content=categorical_widget)
                ```
        """
        super().__init__(
            widget_id=widget_id,
            data=data,
            category_axis=category_axis,
            value_axis=value_axis,
            secondary_value_axis=secondary_value_axis,
            legend_position=legend_position,
            title=title,
            enable_toolbar=enable_toolbar,
            direction=direction,
            tooltips=tooltips,
        )

    def _build_widget_input(self) -> Dict[str, Any]:
        return {
            "title": (
                build_templated_strings(items=self._title) if self._title else None
            ),
            "data": build_data(path=self.dependency_id),
            "chart": self._chart.build(),
            "legend": {"position": self._legend_position.value},
            "toolbar": build_chart_toolbar(enable=self._enable_toolbar),
        }

    def validate(self, data: pd.DataFrame, **kwargs: Any) -> None:
        """Validates widget spec.

        Args:
            data: pandas DataFrame where
                the data is present.

        Raises:
            ChartSeriesNotFoundError: If a series is not found.
        """
        self._validate_dataframe(data=data, **kwargs)

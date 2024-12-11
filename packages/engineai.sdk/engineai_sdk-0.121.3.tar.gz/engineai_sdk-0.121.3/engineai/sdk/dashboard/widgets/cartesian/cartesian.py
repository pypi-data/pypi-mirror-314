"""Spec for Cartesian widget."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.data import DataSource
from engineai.sdk.dashboard.data.http import Http
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links.typing import GenericLink
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.base import Widget
from engineai.sdk.dashboard.widgets.base import WidgetTitleType
from engineai.sdk.dashboard.widgets.cartesian.axis.typing import YAxisSeries
from engineai.sdk.dashboard.widgets.cartesian.axis.y_axis import YAxis
from engineai.sdk.dashboard.widgets.components.charts.toolbar import build_chart_toolbar
from engineai.sdk.dashboard.widgets.utils import build_data

from .chart import Chart
from .chart import XAxis
from .legend import Legend
from .legend import LegendPosition


class Cartesian(Widget):
    """Spec for Cartesian widget."""

    _DEPENDENCY_ID = "__CARTESIAN_DATA_DEPENDENCY__"
    _WIDGET_API_TYPE = "continuousCartesian"

    @type_check
    def __init__(
        self,
        data: Union[DataSource, pd.DataFrame, Http],
        *,
        widget_id: Optional[str] = None,
        x_axis: Union[str, GenericLink, XAxis],
        left_y_axis: Optional[Union[YAxisSeries, YAxis]] = None,
        right_y_axis: Optional[Union[YAxisSeries, YAxis]] = None,
        legend_position: LegendPosition = LegendPosition.BOTTOM,
        title: WidgetTitleType = "",
        enable_toolbar: bool = True,
    ) -> None:
        """Constructor for Cartesian widget.

        Args:
            data: data to be used by widget. Accepts Storages as well as raw data.
            widget_id: unique widget id in a dashboard.
            x_axis: spec for X Axis.
            left_y_axis: spec for left Y Axis.
            right_y_axis: spec for right Y Axis
            legend_position: location of position relative to data, charts.
            title: title of widget can be either a string (fixed value) or determined
                by a value from another widget using a WidgetLink.
            enable_toolbar: Enable/Disable toolbar flag.

        Examples:
            ??? example "Create a minimal Cartesian widget"
                ```py linenums="1"
                import pandas as pd
                from engineai.sdk.dashboard.dashboard import Dashboard
                from engineai.sdk.dashboard.widgets import cartesian

                data = pd.DataFrame(
                    {
                        "x1": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
                        "y1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                    }
                )

                cartesian_widget = cartesian.Cartesian(
                    data=data,
                    x_axis="x1",
                )

                Dashboard(content=cartesian_widget)
                ```
        """
        super().__init__(widget_id=widget_id, data=data)
        self._chart = (
            Chart(
                data=data,
                x_axis=x_axis,
                left_y_axis=left_y_axis,
                right_y_axis=right_y_axis,
            )
            if isinstance(data, pd.DataFrame)
            else Chart(
                x_axis=x_axis,
                left_y_axis=left_y_axis,
                right_y_axis=right_y_axis,
            )
        )
        self._title = title
        self._legend = Legend(position=legend_position)
        self._enable_toolbar = enable_toolbar
        self._json_data = None

    def validate(self, data: pd.DataFrame, **_: Any) -> None:
        """Validates widget spec.

        Args:
            data: pandas DataFrame where the data is present.
        """
        self._chart.validate(data=data)

    def _build_widget_input(self) -> Dict[str, Any]:
        return {
            "title": (
                build_templated_strings(items=self._title) if self._title else None
            ),
            "chart": self._chart.build(),
            "legend": self._legend.build(),
            "toolbar": build_chart_toolbar(enable=self._enable_toolbar),
            "data": build_data(self.dependency_id, self._json_data),
        }

    def _prepare(self, **kwargs: object) -> None:
        """Method that prepares the spec to be built."""
        self._chart.prepare()
        self._json_data = kwargs.get("json_data")

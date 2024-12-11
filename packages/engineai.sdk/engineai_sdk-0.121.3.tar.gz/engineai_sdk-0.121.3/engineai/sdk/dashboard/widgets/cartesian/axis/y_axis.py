"""Specs for Y Axis of a  Cartesian chart."""

from typing import Any
from typing import List
from typing import Mapping
from typing import Optional
from typing import Set
from typing import Union
from typing import get_args

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting import AxisNumberFormatting
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.widgets.cartesian.axis.typing import YAxisSeries
from engineai.sdk.dashboard.widgets.cartesian.series.line import LineSeries
from engineai.sdk.dashboard.widgets.cartesian.series.typing import CartesianSeries
from engineai.sdk.dashboard.widgets.components.charts.axis.scale import AxisScale
from engineai.sdk.dashboard.widgets.components.charts.exceptions import (
    ChartSeriesNameAlreadyExistsError,
)

from .base import CartesianBaseAxis


class YAxis(CartesianBaseAxis):
    """Specs for Y Axis of a Cartesian chart."""

    @type_check
    def __init__(
        self,
        series: YAxisSeries,
        *,
        title: Union[str, WidgetField] = "Y",
        enable_crosshair: bool = False,
        formatting: Optional[AxisNumberFormatting] = None,
        scale: Optional[AxisScale] = None,
    ) -> None:
        """Construct y axis for a Cartesian chart.

        Args:
            series: Add series to Y axis.
            title: axis title.
            enable_crosshair: whether to enable crosshair that follows either
                the mouse pointer or the hovered point.
            formatting: formatting spec for axis labels.
            scale: Y Axis scale.

        Examples:
            ??? example "Create a minimal Cartesian widget with YAxis"
                ```py linenums="1"
                import pandas as pd
                from engineai.sdk.dashboard.dashboard import Dashboard
                from engineai.sdk.dashboard.widgets import cartesian

                data = pd.DataFrame(
                    {
                        "x1": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
                        "y1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                        "y2": [3, 6, 9, 12, 15, 18, 21, 24, 27, 30],
                    }
                )

                cartesian_widget = cartesian.Cartesian(
                    data=data,
                    x_axis="x1",
                    left_y_axis="y1",
                    right_y_axis="y2",
                )

                Dashboard(content=cartesian_widget)
                ```
        """
        super().__init__(
            title=title,
            enable_crosshair=enable_crosshair,
            formatting=formatting,
            scale=scale,
        )
        self.__series_names: Set[str] = set()
        self.__series: List[CartesianSeries] = []
        self._set_series(series)

    def __len__(self) -> int:
        """Returns number of series in axis.

        Returns:
            int: number of series in axis.
        """
        return len(self.__series)

    @property
    def series(self) -> List[CartesianSeries]:
        """Returns the list of Series in Axis.

        Returns:
            List[CartesianSeries]: list of Series.
        """
        return self.__series

    def _set_str_series(self, series: str) -> None:
        if series in self.__series_names:
            raise ChartSeriesNameAlreadyExistsError(
                class_name=self.__class__.__name__,
                series_name=series,
            )
        self.__series_names.add(series)
        self.__series.append(LineSeries(data_column=series))

    def _set_cartesian_series(self, series: CartesianSeries) -> None:
        if isinstance(series.name, str):
            if series.name in self.__series_names:
                raise ChartSeriesNameAlreadyExistsError(
                    class_name=self.__class__.__name__,
                    series_name=series.name,
                )
            self.__series_names.add(series.name)
        self.__series.append(series)

    def _set_series(self, series: YAxisSeries) -> None:
        if isinstance(series, str):
            self._set_str_series(series)
        elif isinstance(series, WidgetField):
            self.__series.append(LineSeries(data_column=series))
        elif isinstance(series, list):
            for serie in series:
                self._set_series(serie)
        elif isinstance(series, get_args(CartesianSeries)):
            self._set_cartesian_series(series)

    def prepare(self, x_column: TemplatedStringItem, offset: int = 0) -> None:
        """Prepare layout for building."""
        for index, element in enumerate(self.__series):
            element.prepare(
                x_column=x_column,
                index=index + offset,
            )

    def _axis_validate(self, *, data: pd.DataFrame) -> None:
        """Validate cartesian y axis series."""
        for series in self.__series:
            series.validate(data=data)

    def _build_extra_axis(self) -> Mapping[str, Any]:
        series_spec = [series.build() for series in self.__series]

        return {"series": series_spec}

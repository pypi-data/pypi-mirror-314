"""Specs for y axis of a Timeseries chart."""

import warnings
from typing import Any
from typing import List
from typing import Mapping
from typing import Optional
from typing import Union
from typing import cast

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting import AxisNumberFormatting
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.widgets.components.charts.axis.scale import AxisScale
from engineai.sdk.dashboard.widgets.components.charts.band.band import AxisBand
from engineai.sdk.dashboard.widgets.components.charts.line.line import AxisLine
from engineai.sdk.dashboard.widgets.timeseries.series.typing import LineSeries
from engineai.sdk.dashboard.widgets.timeseries.series.typing import TimeseriesSeries

from .base import BaseTimeseriesYAxis


class YAxis(BaseTimeseriesYAxis):
    """Specify y-axis appearance & behavior in Timeseries chart.

    Construct specifications for the y-axis of a Timeseries chart with
    a range of options to customize its appearance and behavior.
    """

    _INPUT_KEY = "standard"

    @type_check
    def __init__(
        self,
        *,
        series: Optional[List[Union[str, TimeseriesSeries]]] = None,
        formatting: Optional[AxisNumberFormatting] = None,
        title: Union[str, WidgetField] = "",
        enable_crosshair: bool = False,
        scale: Optional[AxisScale] = None,
        line: Optional[AxisLine] = None,
        band: Optional[AxisBand] = None,
    ) -> None:
        """Constructor for YAxis.

        Args:
            series: series to be added to the y axis.
            formatting: formatting spec for axis labels.
            title: axis title.
            enable_crosshair: whether to enable crosshair that follows either
                the mouse pointer or the hovered point.
            scale: y axis scale, one of
                AxisScaleSymmetric, AxisScaleDynamic,
                AxisScalePositive, AxisScaleNegative.
            line: line spec for y axis.
            band: band spec for y axis.
        """
        super().__init__(
            formatting=formatting,
            title=title,
            enable_crosshair=enable_crosshair,
            scale=scale,
            line=line,
            band=band,
        )
        self.__set_series(series)

    def __set_series(
        self, series: Optional[List[Union[str, TimeseriesSeries]]]
    ) -> None:
        """Set series for y axis."""
        self.__series: List[TimeseriesSeries] = []
        if series is not None:
            self._add_series(
                self.__series,
                *[
                    (
                        LineSeries(data_column=element)
                        if isinstance(element, str)
                        else element
                    )
                    for element in series
                ],
            )

    def __len__(self) -> int:
        """Returns number of series in axis.

        Returns:
            int: number of series in axis.
        """
        return len(self.__series)

    def _validate_series(self, *, data: pd.DataFrame) -> None:
        """Validate timeseries y axis series."""
        for series in self.__series:
            series.validate(data=data)

    def add_series(self, *series: TimeseriesSeries) -> "YAxis":
        """Add series to y axis.

        Returns:
            YAxis: reference to this axis to facilitate inline manipulation.

        """
        warnings.warn(
            "add_series is deprecated and will be removed in a future release."
            "Please use `series` parameter instead.",
            DeprecationWarning,
        )
        return cast(YAxis, self._add_series(self.__series, *series))

    def prepare(self, date_column: TemplatedStringItem, offset: int = 0) -> None:
        """Prepare layout for building."""
        for index, element in enumerate(self.__series):
            element.prepare(
                date_column=date_column,
                index=index + offset,
            )

    def _build_extra_y_axis(self) -> Mapping[str, Any]:
        """Method that generates the input for a specific y axis."""
        return {"series": [series.build() for series in self.__series]}

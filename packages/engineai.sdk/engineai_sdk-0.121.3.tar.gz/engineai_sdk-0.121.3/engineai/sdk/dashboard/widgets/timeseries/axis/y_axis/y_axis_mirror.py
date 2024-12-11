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


class MirrorYAxis(BaseTimeseriesYAxis):
    """Customize appearance & behavior of mirror y-axis in Timeseries chart.

    Construct specifications for the mirror y-axis of a Timeseries
    chart with a range of options to customize its appearance and behavior.
    """

    _INPUT_KEY = "mirror"

    @type_check
    def __init__(
        self,
        *,
        top_series: Optional[List[Union[str, TimeseriesSeries]]] = None,
        bottom_series: Optional[List[Union[str, TimeseriesSeries]]] = None,
        formatting: Optional[AxisNumberFormatting] = None,
        title: Union[str, WidgetField] = "",
        enable_crosshair: bool = False,
        scale: Optional[AxisScale] = None,
        line: Optional[AxisLine] = None,
        band: Optional[AxisBand] = None,
    ) -> None:
        """Constructor for MirrorYAxis.

        Args:
            top_series: series to be added to the top y axis.
            bottom_series: series to be added to the bottom y axis.
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
        self.__set_series(top_series, bottom_series)

    def __set_series(
        self,
        top_series: Optional[List[Union[str, TimeseriesSeries]]],
        bottom_series: Optional[List[Union[str, TimeseriesSeries]]],
    ) -> None:
        """Set series for y axis."""
        self.__top_series: List[TimeseriesSeries] = []
        self.__bottom_series: List[TimeseriesSeries] = []
        if top_series is not None:
            self._add_series(
                self.__top_series,
                *[
                    (
                        LineSeries(data_column=element)
                        if isinstance(element, str)
                        else element
                    )
                    for element in top_series
                ],
            )
        if bottom_series is not None:
            self._add_series(
                self.__bottom_series,
                *[
                    (
                        LineSeries(data_column=element)
                        if isinstance(element, str)
                        else element
                    )
                    for element in bottom_series
                ],
            )

    def __len__(self) -> int:
        """Get number of series for this axis."""
        return len(self.__top_series) + len(self.__bottom_series)

    def _validate_series(self, *, data: pd.DataFrame) -> None:
        """Validate timeseries y axis series."""
        for series in self.__top_series:
            series.validate(data=data)
        for series in self.__bottom_series:
            series.validate(data=data)

    def add_top_series(self, *series: TimeseriesSeries) -> "MirrorYAxis":
        """Add series to top y axis.

        Returns:
            MirrorYAxis: reference to this axis to facilitate inline manipulation.

        Raises:
            TimeseriesAxisEmptyDefinitionError: when no series data are added
            ChartSeriesNameAlreadyExistsError: when series have duplicated names
        """
        warnings.warn(
            "add_top_series is deprecated and will be removed in a future release."
            "Please use `top_series` parameter instead.",
            DeprecationWarning,
        )
        return cast(MirrorYAxis, self._add_series(self.__top_series, *series))

    def add_bottom_series(self, *series: TimeseriesSeries) -> "MirrorYAxis":
        """Add series to top y axis.

        Returns:
            MirrorYAxis: reference to this axis to facilitate inline manipulation.

        Raises:
            TimeseriesAxisEmptyDefinitionError: when no series data are added
            ChartSeriesNameAlreadyExistsError: when series have duplicated names
        """
        warnings.warn(
            "add_bottom_series is deprecated and will be removed in a future release."
            "Please use `bottom_series` parameter instead.",
            DeprecationWarning,
        )
        return cast(MirrorYAxis, self._add_series(self.__bottom_series, *series))

    def prepare(self, date_column: TemplatedStringItem, offset: int = 0) -> None:
        """Prepare layout for building."""
        for index, element in enumerate(self.__top_series):
            element.prepare(
                date_column=date_column,
                index=index + offset,
            )

        for index, element in enumerate(self.__bottom_series):
            element.prepare(
                date_column=date_column,
                index=index + offset,
            )

    def _build_extra_y_axis(self) -> Mapping[str, Any]:
        """Method that generates the input for a specific y axis."""
        return {
            "topSeries": [series.build() for series in self.__top_series],
            "bottomSeries": [series.build() for series in self.__bottom_series],
        }

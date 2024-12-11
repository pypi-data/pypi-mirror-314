"""Specs for Value Axis of a Categorical chart."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Set
from typing import Union
from typing import get_args

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting import AxisNumberFormatting
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.links.abstract import AbstractFactoryLinkItemsHandler
from engineai.sdk.dashboard.links.typing import GenericLink
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.categorical.axis.typing import ValueAxisSeries
from engineai.sdk.dashboard.widgets.categorical.exceptions import (
    CategoricalNoSeriesDefinedError,
)
from engineai.sdk.dashboard.widgets.categorical.series.column import ColumnSeries
from engineai.sdk.dashboard.widgets.categorical.series.typing import CategoricalSeries
from engineai.sdk.dashboard.widgets.components.charts.axis.scale import AxisScale
from engineai.sdk.dashboard.widgets.components.charts.axis.scale import AxisScaleDynamic
from engineai.sdk.dashboard.widgets.components.charts.axis.scale import build_axis_scale
from engineai.sdk.dashboard.widgets.components.charts.band.band import AxisBand
from engineai.sdk.dashboard.widgets.components.charts.exceptions import (
    ChartSeriesNameAlreadyExistsError,
)
from engineai.sdk.dashboard.widgets.components.charts.line.line import AxisLine


class ValueAxis(AbstractFactoryLinkItemsHandler):
    """Specs for Value Axis of a Categorical chart."""

    @type_check
    def __init__(
        self,
        *,
        series: ValueAxisSeries,
        formatting: Optional[AxisNumberFormatting] = None,
        title: Optional[Union[str, GenericLink]] = None,
        enable_crosshair: bool = False,
        scale: Optional[AxisScale] = None,
        line: Optional[AxisLine] = None,
        band: Optional[AxisBand] = None,
    ) -> None:
        """Construct Value Axis for a Categorical chart.

        Args:
            series: series to be added to the axis.
            formatting: formatting spec for axis labels.
            title: axis title.
            scale: y axis scale, one of AxisScaleDynamic, AxisScaleSymmetric,
                AxisScalePositive, AxisScaleNegative.
            enable_crosshair: whether to enable crosshair that follows either
                the mouse pointer or the hovered point.
                Defaults to False.
            line: line to be added to the axis.
            band: band to be added to the axis.
        """
        super().__init__()
        self.__enable_crosshair = enable_crosshair
        self.__formatting = formatting or AxisNumberFormatting()
        self.__title = title
        self.__series_names: Set[str] = set()
        self.__series: List[CategoricalSeries] = []
        self.__scale = scale or AxisScaleDynamic()
        self.__line = line
        self.__band = band
        self._set_series(series)

    def __len__(self) -> int:
        """Returns number of series in axis.

        Returns:
            int: number of series in axis.
        """
        return len(self.__series)

    def _set_str_series(self, series: str) -> None:
        if series in self.__series_names:
            raise ChartSeriesNameAlreadyExistsError(
                class_name=self.__class__.__name__,
                series_name=series,
            )
        self.__series_names.add(series)
        self.__series.append(ColumnSeries(data_column=series))

    def _set_categorical_series(self, series: CategoricalSeries) -> None:
        """Add series to Value Axis."""
        if series.name in self.__series_names:
            raise ChartSeriesNameAlreadyExistsError(
                class_name=self.__class__.__name__,
                series_name=series.name,
            )

        if isinstance(series.name, str):
            self.__series_names.add(series.name)
        self.__series.append(series)

    def _set_series(self, series: ValueAxisSeries) -> None:
        if isinstance(series, str):
            self._set_str_series(series)
        elif isinstance(series, WidgetField):
            self.__series.append(ColumnSeries(data_column=series))
        elif isinstance(series, (list, Sequence)):
            for serie in series:
                self._set_series(serie)
        elif isinstance(series, get_args(CategoricalSeries)):
            self._set_categorical_series(series)

    def __build_series(self) -> List[Any]:
        return [series.build() for series in self.__series]

    def prepare(
        self,
        data_column: Union[str, GenericLink],
    ) -> None:
        """Prepare Value Axis elements.

        Args:
            data_column: data column for the Series.
            palette: palette to be used by chart.
            value_axis_length: number of series from other axis.
        """
        for series in self.__series:
            series.prepare(
                data_column=data_column,
            )

    def validate(self, data: pd.DataFrame, **kwargs: Any) -> None:
        """Validate Value Axis elements and Data.

        Args:
            data: Data associated to the chart.
        """
        if len(self.__series) == 0:
            raise CategoricalNoSeriesDefinedError
        for elem in self.__series:
            elem.validate(data=data, **kwargs)

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "enableCrosshair": self.__enable_crosshair,
            "bands": [self.__band.build()] if self.__band is not None else [],
            "lines": [self.__line.build()] if self.__line is not None else [],
            "scale": build_axis_scale(scale=self.__scale),
            "formatting": self.__formatting.build(),
            "title": (
                build_templated_strings(items=self.__title) if self.__title else None
            ),
            "series": self.__build_series(),
        }

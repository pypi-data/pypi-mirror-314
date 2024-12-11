"""Spec for Base Map Geo class."""

from typing import Any
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar
from typing import Union

import pandas as pd
from pandas.api.types import is_datetime64_dtype
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_object_dtype
from pandas.api.types import is_string_dtype

from engineai.sdk.dashboard.data.decorator import DataSource
from engineai.sdk.dashboard.data.http import Http
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.base import Widget
from engineai.sdk.dashboard.widgets.base import WidgetTitleType
from engineai.sdk.dashboard.widgets.chart_utils import get_object_columns_tooltip
from engineai.sdk.dashboard.widgets.components.charts.tooltip.datetime import (
    DatetimeTooltipItem,
)
from engineai.sdk.dashboard.widgets.components.charts.tooltip.item import (
    build_tooltip_item,
)
from engineai.sdk.dashboard.widgets.components.charts.tooltip.number import (
    NumberTooltipItem,
)
from engineai.sdk.dashboard.widgets.components.charts.tooltip.text import (
    TextTooltipItem,
)
from engineai.sdk.dashboard.widgets.components.charts.typing import TooltipItems
from engineai.sdk.dashboard.widgets.components.playback.playback import Playback
from engineai.sdk.dashboard.widgets.maps.color_axis import ColorAxis
from engineai.sdk.dashboard.widgets.maps.enums import LegendPosition
from engineai.sdk.dashboard.widgets.maps.enums import Region
from engineai.sdk.dashboard.widgets.maps.exceptions import MapColumnDataNotFoundError
from engineai.sdk.dashboard.widgets.maps.geo.styling.styling import MapStyling
from engineai.sdk.dashboard.widgets.maps.series.numeric import NumericSeries
from engineai.sdk.dashboard.widgets.maps.series.series import MapSeries
from engineai.sdk.dashboard.widgets.maps.series.series import build_map_series
from engineai.sdk.dashboard.widgets.utils import build_data
from engineai.sdk.dashboard.widgets.utils import get_tooltips

T = TypeVar("T", pd.DataFrame, Dict[str, Any])


class BaseMapGeo(Generic[T], Widget):
    """Spec for Base MapGeo widget."""

    _WIDGET_API_TYPE = "mapGeo"
    _DEPENDENCY_ID = "__MAP_GEO_DATA_DEPENDENCY__"

    @type_check
    def __init__(
        self,
        data: Union[DataSource, T, Http],
        *,
        series: Optional[MapSeries] = None,
        region_column: str = "region",
        widget_id: Optional[str] = None,
        title: Optional[WidgetTitleType] = None,
        color_axis: Optional[ColorAxis] = None,
        legend_position: LegendPosition = LegendPosition.BOTTOM,
        styling: Optional[MapStyling] = None,
        region: Region = Region.WORLD,
        tooltips: Optional[TooltipItems] = None,
        playback: Optional[Playback] = None,
    ) -> None:
        """Construct spec for the Base Map Geo class.

        Args:
            data: data source for the widget.
            series: Series to be added to y axis.
            region_column: key to match region code in DS.
            widget_id: unique widget id in a dashboard.
            title: title of widget can be either a string (fixed value) or determined
                by a value from another widget using a WidgetField.
            styling: styling for the map.
            legend_position: location of position relative to data, maps.
            color_axis: color axis spec.
            region: sets the region os the Map.
            tooltips: tooltip items to be displayed at Chart level.
            playback: playback spec for the map.
        """
        super().__init__(data=data, widget_id=widget_id)
        self._title = title
        self._legend_position = legend_position
        self._color_axis = color_axis if color_axis else ColorAxis()
        self._styling = styling if styling is not None else MapStyling()
        self._series: List[MapSeries] = [series] if series else [NumericSeries()]
        self._region = region
        self._region_column = region_column
        self._extra_tooltip_items = get_tooltips(tooltips)
        self._auto_generate_tooltips(
            data=data, series=series, region_column=region_column
        )
        self._playback = playback
        self._json_data = None

    def validate(self, data: pd.DataFrame, **_: Any) -> None:
        """Validates widget spec.

        Args:
            data: pandas DataFrame where
                the data is present.

        Raises:
            TooltipItemColumnNotFoundError: if column(s) of tooltip(s) were not found
            MapColumnDataNotFoundError: if column(s) supposed to contain data were not
                found.
        """
        self._validate_map_data(data=data)
        self._validate_series(data=data)

    def _prepare(self, **kwargs: object) -> None:
        for num, series in enumerate(self._series):
            series.prepare(
                num,
                self._region_column,
                self.dependency_id,
                kwargs.get("json_data"),
            )
        if self._playback is not None:
            self._playback.prepare()

        self._json_data = kwargs.get("json_data")

    def _validate_map_data(self, data: T) -> None:
        """Validates data for map widget spec."""
        iterable = iter([data]) if isinstance(data, pd.DataFrame) else data.values()
        for value in iterable:
            if (
                isinstance(value, pd.DataFrame)
                and self._region_column not in value.columns
            ):
                raise MapColumnDataNotFoundError(column_data=self._region_column)

            if self._extra_tooltip_items and isinstance(value, pd.DataFrame):
                for tooltips in self._extra_tooltip_items:
                    tooltips.validate(data=value)

    def _validate_series(self, data: T) -> None:
        """Validates styling for map series spec."""
        if isinstance(data, pd.DataFrame):
            for series in self._series:
                series.validate(data=data)

    def _build_extra_inputs(self) -> Dict[str, Any]:
        return {}

    def _build_series(self) -> Dict[str, Any]:
        """Builds series spec."""
        return [build_map_series(series=series) for series in self._series]

    def _build_tooltips(self) -> Dict[str, Any]:
        """Builds tooltip spec."""
        if self._extra_tooltip_items:
            return {
                "regionKey": self._region_column,
                "data": build_data(path=self.dependency_id, json_data=self._json_data),
                "items": (
                    [
                        build_tooltip_item(item=tooltip)
                        for tooltip in self._extra_tooltip_items
                    ]
                    if self._extra_tooltip_items
                    else []
                ),
            }
        return None

    def _build_widget_input(self) -> Dict[str, Any]:
        """Method to build map widget."""
        return {
            "title": (
                build_templated_strings(items=self._title) if self._title else None
            ),
            "colorAxis": self._color_axis.build(),
            "legend": {"position": self._legend_position.value},
            "series": self._build_series(),
            "region": self._region.value,
            "styling": self._styling.build(),
            "tooltip": self._build_tooltips(),
            **self._build_extra_inputs(),
        }

    def _auto_generate_tooltips(
        self,
        data: Union[DataSource, T],
        series: Optional[MapSeries],
        region_column: str,
    ) -> None:
        if series is not None or region_column != "region":
            return
        if isinstance(data, pd.DataFrame):
            self._validate_map_data(data)
            self._validate_series(data)
            aux_data = data.drop(["region", "value"], axis=1)
            for column_name in aux_data.columns:
                if is_numeric_dtype(aux_data[column_name]):
                    self._extra_tooltip_items.append(
                        NumberTooltipItem(data_column=str(column_name))
                    )
                elif is_datetime64_dtype(aux_data[column_name]):
                    self._extra_tooltip_items.append(
                        DatetimeTooltipItem(data_column=str(column_name))
                    )
                elif is_object_dtype(aux_data[column_name]):
                    tooltip_item = get_object_columns_tooltip(
                        column_data=aux_data[column_name], column_name=str(column_name)
                    )
                    if tooltip_item is not None:
                        self._extra_tooltip_items.append(tooltip_item)
                elif is_string_dtype(aux_data[column_name]):
                    self._extra_tooltip_items.append(
                        TextTooltipItem(data_column=str(column_name))
                    )

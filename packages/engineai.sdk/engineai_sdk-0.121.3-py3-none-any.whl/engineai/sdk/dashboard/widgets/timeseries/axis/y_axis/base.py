"""Specs for y axis of a Timeseries chart."""

from abc import abstractmethod
from typing import Any
from typing import List
from typing import Mapping
from typing import Optional
from typing import Set
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting import AxisNumberFormatting
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.links.abstract import AbstractFactoryLinkItemsHandler
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.charts.axis.scale import AxisScale
from engineai.sdk.dashboard.widgets.components.charts.axis.scale import AxisScaleDynamic
from engineai.sdk.dashboard.widgets.components.charts.axis.scale import build_axis_scale
from engineai.sdk.dashboard.widgets.components.charts.band.band import AxisBand
from engineai.sdk.dashboard.widgets.components.charts.exceptions import (
    ChartSeriesNameAlreadyExistsError,
)
from engineai.sdk.dashboard.widgets.components.charts.line.line import AxisLine

from ...exceptions import TimeseriesAxisEmptyDefinitionError
from ...series.typing import TimeseriesSeries


class BaseTimeseriesYAxis(AbstractFactoryLinkItemsHandler):
    """Specs for y axis of a Timeseries chart."""

    _INPUT_KEY: Optional[str] = None

    @type_check
    def __init__(
        self,
        *,
        formatting: Optional[AxisNumberFormatting] = None,
        title: Union[str, WidgetField] = "",
        enable_crosshair: bool = False,
        scale: Optional[AxisScale] = None,
        line: Optional[AxisLine] = None,
        band: Optional[AxisBand] = None,
    ) -> None:
        """Construct y axis for a Timeseries chart.

        Args:
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
        super().__init__()
        self.__enable_crosshair = enable_crosshair
        self.__line = line
        self.__band = band
        self.__formatting = (
            formatting if formatting is not None else AxisNumberFormatting()
        )

        self.__title = title
        self.__scale = scale if scale else AxisScaleDynamic()

        # used for getting a color from the index of each bands
        self.__series_names: Set[str] = set()

    @property
    def _input_key(self) -> str:
        """Returns styling Input Key argument value."""
        if self._INPUT_KEY is None:
            msg = f"Class {self.__class__.__name__}._INPUT_KEY not defined."
            raise NotImplementedError(msg)
        return self._INPUT_KEY

    def validate(
        self,
        *,
        data: pd.DataFrame,
    ) -> None:
        """Validate if dataframe has the required columns and dependencies for axis.

        Args:
            data (pd.DataFrame): pandas dataframe which will be used for table.

        Raises:
            ChartDependencyNotFoundError: when `datastore_id` does not exists on
                current datastores
        """
        self._validate_series(
            data=data,
        )
        self.__formatting.validate(data=data)

    @abstractmethod
    def _validate_series(
        self,
        *,
        data: pd.DataFrame,
    ) -> None:
        """Validate timeseries y axis series."""

    def _add_series(
        self, current_series: List[TimeseriesSeries], *series: TimeseriesSeries
    ) -> "BaseTimeseriesYAxis":
        """Auxiliary method to add series to top y axis.

        Returns:
            YAxis: reference to this axis to facilitate inline manipulation.

        Raises:
            TimeseriesAxisEmptyDefinitionError: when no series data are added
            ChartSeriesNameAlreadyExistsError: when series have duplicated names
        """
        if len(series) == 0:
            raise TimeseriesAxisEmptyDefinitionError

        for element in series:
            if element.name in current_series:
                raise ChartSeriesNameAlreadyExistsError(
                    class_name=self.__class__.__name__,
                    series_name=element.name,
                )
            if isinstance(element.name, str):
                self.__series_names.add(str(element.name))

        current_series.extend(series)

        return self

    @abstractmethod
    def prepare(self, date_column: TemplatedStringItem, offset: int = 0) -> None:
        """Prepare layout for building."""

    @abstractmethod
    def _build_extra_y_axis(self) -> Mapping[str, Any]:
        """Method that generates the input for a specific y axis."""

    def _build_axis(self) -> Mapping[str, Any]:
        """Method that generates the input for a specific axis."""
        return {
            "formatting": (
                self.__formatting.build() if self.__formatting is not None else None
            ),
            "title": build_templated_strings(
                items=self.__title if self.__title else ""
            ),
            "scale": build_axis_scale(scale=self.__scale),
            "enableCrosshair": self.__enable_crosshair,
            "bands": [self.__band.build()] if self.__band is not None else [],
            "lines": [self.__line.build()] if self.__line is not None else [],
            **self._build_extra_y_axis(),
        }

    def build(self) -> Mapping[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            self._input_key: self._build_axis(),
        }

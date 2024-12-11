"""Spec for navigator of a timeseries widget."""

from typing import Any
from typing import Dict
from typing import Optional

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links.abstract import AbstractFactoryLinkItemsHandler
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.base import WidgetTitleType

from .exceptions import TimeseriesNavigatorEmptyDefinitionError
from .series.typing import TimeseriesSeries


class Navigator(AbstractFactoryLinkItemsHandler):
    """Navigation of Timeseries data.

    Construct a navigator for a timeseries widget for efficient
    navigation and exploration of time-series data. Specify one or
    more series to be included in the navigator for easy visualization
    of trends and patterns across different metrics.
    """

    @type_check
    def __init__(
        self, *series: TimeseriesSeries, title: Optional[WidgetTitleType] = None
    ) -> None:
        """Constructor for Navigator.

        Args:
            title: title to be added to navigator
            series: series to be added to navigator
        """
        super().__init__()

        if len(series) == 0:
            raise TimeseriesNavigatorEmptyDefinitionError

        self.__series = series
        self.__title = title

    def prepare(self, date_column: TemplatedStringItem) -> None:
        """Method that prepares the spec to be build."""
        for index, series in enumerate(self.__series):
            series.prepare(date_column, index=index)

    def validate(self, *, data: pd.DataFrame) -> None:
        """Validate if dataframe that will be used for column contains required columns.

        Args:
            data: pandas dataframe which will be used for table

        """
        for series in self.__series:
            series.validate(data=data)

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        series_spec = [series.build() for series in self.__series]
        return {
            "series": series_spec,
            "title": build_templated_strings(items=self.__title),
        }

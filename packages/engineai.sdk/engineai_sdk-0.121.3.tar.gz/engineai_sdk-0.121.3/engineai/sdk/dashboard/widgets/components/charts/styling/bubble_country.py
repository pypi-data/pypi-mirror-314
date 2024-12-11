"""Spec to style a bubble series using country flags."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links.typing import GenericLink
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.charts.exceptions import (
    ChartStylingNoDataColumnError,
)


class BubbleCountrySeriesStyling(AbstractFactory):
    """Customize appearance of country bubble markers.

    Specify styling options for a bubble country series within a Chart widget
    to customize the appearance of bubble markers representing countries on the chart.
    """

    @type_check
    def __init__(
        self,
        *,
        country_column: TemplatedStringItem,
        max_size_percentage: Optional[Union[int, float]] = 0.5,
        min_size_percentage: Optional[Union[int, float]] = 0.2,
    ) -> None:
        """Constructor for BubbleCountrySeriesStyling.

        Args:
            country_column: name of column in pandas dataframe(s) with country codes.
            max_size_percentage: Percentage of the highest one of the plot width and
                height.
            min_size_percentage: Percentage of the smallest one of the plot width and
                height.
        """
        super().__init__()
        self.__country_column = country_column
        self.__max_size_percentage = max_size_percentage
        self.__min_size_percentage = min_size_percentage

    def validate(
        self,
        *,
        data: pd.DataFrame,
    ) -> None:
        """Validate if dataframe that will be used for column contains required columns.

        Args:
            data: pandas dataframe which will be used for table

        Raises:
            ChartStylingNoDataColumnError: if a specific column does not exists in data
        """
        if (
            isinstance(self.__country_column, str)
            and self.__country_column not in data.columns
        ):
            raise ChartStylingNoDataColumnError(
                class_name=self.__class__.__name__,
                data_column=self.__country_column,
            )

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "country": {
                "countryKey": build_templated_strings(items=self.__country_column),
                "maxSizePercentage": self.__max_size_percentage,
                "minSizePercentage": self.__min_size_percentage,
            }
        }

    def prepare(
        self, data_column: Optional[Union[str, TemplatedStringItem, GenericLink]]
    ) -> None:
        """Prepare data column."""

"""Spec to style a bubble series as circles."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.styling.color.typing import ColorSpec
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.charts.exceptions import (
    ChartStylingNoDataColumnError,
)

from .base import BaseChartSeriesStyling


class BubbleCircleSeriesStyling(BaseChartSeriesStyling):
    """Customize appearance of bubble markers.

    Specify styling options for a bubble circle series within a Chart
    widget to customize the appearance of bubble markers on the chart.
    """

    @type_check
    def __init__(
        self,
        *,
        color_spec: ColorSpec,
        data_column: Optional[TemplatedStringItem] = None,
        label_column: Optional[TemplatedStringItem] = None,
        max_size_percentage: Optional[Union[int, float]] = 0.5,
        min_size_percentage: Optional[Union[int, float]] = 0.2,
    ) -> None:
        """Constructor for BubbleCircleSeriesStyling.

        Args:
            color_spec: spec for coloring bubble.
            data_column: name of column in pandas dataframe(s) used for color spec if
                a gradient is used. Optional for single colors.
            label_column: name of column in pandas dataframe(s) used for labeling the
                bubble.
            max_size_percentage: Percentage of the highest one of the plot width and
                height.
            min_size_percentage: Percentage of the smallest one of the plot width and
                height.

        Raises:
            ChartStylingMissingDataColumnError: if color_spec is
                ColorDiscreteMap/ColorGradient and data_column
                has not been specified
        """
        super().__init__(color_spec=color_spec, data_column=data_column)
        self.__label_column = label_column if label_column is None else label_column
        self.__max_size_percentage = max_size_percentage
        self.__min_size_percentage = min_size_percentage

    def validate(
        self,
        *,
        data: pd.DataFrame,
    ) -> None:
        """Validate if dataframe that will be used for column contains required columns.

        Args:
            data (DataFrame): pandas dataframe which will be used for table

        Raises:
            ChartStylingNoDataColumnError: if a specific column does not exists in data
        """
        super().validate(data=data)
        if self.__label_column is not None and self.__label_column not in data.columns:
            raise ChartStylingNoDataColumnError(
                class_name=self.__class__.__name__,
                data_column=self.__label_column,
            )

    def _build_extra_fields(self) -> Dict[str, Any]:
        return {
            "maxSizePercentage": self.__max_size_percentage,
            "minSizePercentage": self.__min_size_percentage,
            "labelKey": build_templated_strings(items=self.__label_column),
        }

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {"circle": super().build()}

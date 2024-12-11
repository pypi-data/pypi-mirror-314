"""Spec for charts in a Cartesian widget."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links.abstract import AbstractFactoryLinkItemsHandler
from engineai.sdk.dashboard.links.typing import GenericLink
from engineai.sdk.dashboard.widgets.cartesian.axis.typing import YAxisSeries
from engineai.sdk.dashboard.widgets.cartesian.exceptions import (
    CartesianMissingChartAxisError,
)

from .axis.x_axis import XAxis
from .axis.y_axis import YAxis


class Chart(AbstractFactoryLinkItemsHandler):
    """Spec for charts in a Cartesian widget."""

    @type_check
    def __init__(
        self,
        x_axis: Union[str, GenericLink, XAxis],
        *,
        data: Optional[pd.DataFrame] = None,
        left_y_axis: Optional[Union[YAxisSeries, YAxis]] = None,
        right_y_axis: Optional[Union[YAxisSeries, YAxis]] = None,
    ) -> None:
        """Construct a chart for a Cartesian widget.

        Args:
            data: Widget data.
            left_y_axis: spec for left Y Axis.
            x_axis: spec for X Axis.
            right_y_axis: spec for right Y Axis.
        """
        super().__init__()
        self.__data = data
        self.__x_axis = (
            x_axis if isinstance(x_axis, XAxis) else XAxis(data_column=x_axis)
        )
        self.__set_chart_y_axis(left_y_axis, right_y_axis)

    def __set_chart_y_axis(
        self,
        left_y_axis: Optional[Union[YAxisSeries, YAxis]] = None,
        right_y_axis: Optional[Union[YAxisSeries, YAxis]] = None,
    ) -> None:
        if left_y_axis is None and right_y_axis is None and self.__data is None:
            raise CartesianMissingChartAxisError

        if self.__data is not None and left_y_axis is None and right_y_axis is None:
            self.__left_y_axis: Optional[YAxis] = YAxis(
                series=self.__data.drop(
                    columns=self.__x_axis.data_column
                ).columns.to_list(),
            )
        else:
            self.__left_y_axis = (
                left_y_axis
                if isinstance(left_y_axis, YAxis)
                else (
                    YAxis(title="Left Y", series=left_y_axis)
                    if right_y_axis is not None and left_y_axis is not None
                    else (
                        YAxis(series=left_y_axis)
                        if left_y_axis is not None and right_y_axis is None
                        else None
                    )
                )
            )

        self.__right_y_axis = (
            right_y_axis
            if isinstance(right_y_axis, YAxis)
            else (
                YAxis(title="Right Y", series=right_y_axis)
                if right_y_axis is not None and left_y_axis is not None
                else (
                    YAxis(series=right_y_axis)
                    if right_y_axis is not None and left_y_axis is None
                    else None
                )
            )
        )

    def validate(
        self,
        *,
        data: pd.DataFrame,
    ) -> None:
        """Validate if chart has all dataframe columns and axis dependencies.

        Args:
            data: pandas dataframe which will be used for table.
        """
        # validate each axis
        self.__x_axis.validate(
            data=data,
        )
        if self.__left_y_axis is not None:
            self.__left_y_axis.validate(
                data=data,
            )
        if self.__right_y_axis is not None:
            self.__right_y_axis.validate(
                data=data,
            )

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API.
        """
        return {
            "xAxis": self.__x_axis.build(),
            "yAxisLeft": (
                [self.__left_y_axis.build()] if self.__left_y_axis is not None else []
            ),
            "yAxisRight": (
                [self.__right_y_axis.build()] if self.__right_y_axis is not None else []
            ),
        }

    def prepare(self) -> None:
        """Method that prepares the spec to be built."""
        if self.__left_y_axis is not None:
            self.__left_y_axis.prepare(self.__x_axis.data_column)
        if self.__right_y_axis is not None:
            self.__right_y_axis.prepare(
                self.__x_axis.data_column,
                offset=len(self.__left_y_axis) if self.__left_y_axis is not None else 0,
            )

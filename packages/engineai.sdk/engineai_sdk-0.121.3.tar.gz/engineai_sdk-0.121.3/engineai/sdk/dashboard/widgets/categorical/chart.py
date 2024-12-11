"""Spec for Charts in a Categorical widget."""

import datetime
from decimal import Decimal
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.links.abstract import AbstractFactoryLinkItemsHandler
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.categorical.axis.typing import ValueAxisSeries
from engineai.sdk.dashboard.widgets.categorical.enum import ChartDirection
from engineai.sdk.dashboard.widgets.categorical.exceptions import (
    CategoricalSeriesDataColumnNotNumericError,
)
from engineai.sdk.dashboard.widgets.categorical.exceptions import (
    CategoricalValidateDataColumnNotFoundError,
)
from engineai.sdk.dashboard.widgets.categorical.exceptions import (
    CategoricalValueAxisAndSecondaryAxisNotFoundError,
)
from engineai.sdk.dashboard.widgets.categorical.series.column import ColumnSeries
from engineai.sdk.dashboard.widgets.chart_utils import column_is_of_type
from engineai.sdk.dashboard.widgets.components.charts.tooltip import DatetimeTooltipItem
from engineai.sdk.dashboard.widgets.components.charts.tooltip import TextTooltipItem
from engineai.sdk.dashboard.widgets.components.charts.tooltip.item import TooltipItem
from engineai.sdk.dashboard.widgets.components.charts.tooltip.item import (
    build_tooltip_item,
)
from engineai.sdk.dashboard.widgets.utils import build_data

from .axis.category import CategoryAxis
from .axis.value import ValueAxis


class Chart(AbstractFactoryLinkItemsHandler):
    """Spec for Charts in a Categorical widget."""

    @type_check
    def __init__(
        self,
        *,
        data: Optional[pd.DataFrame] = None,
        category_axis: Union[str, WidgetField, CategoryAxis] = "category",
        value_axis: Optional[Union[ValueAxisSeries, ValueAxis]] = None,
        secondary_value_axis: Optional[Union[ValueAxisSeries, ValueAxis]] = None,
        direction: ChartDirection = ChartDirection.VERTICAL,
        tooltips: Optional[List[TooltipItem]] = None,
    ) -> None:
        """Construct a Chart for a Categorical widget.

        Args:
            data: data source for the widget.
            category_axis: spec for category axis.
            value_axis: spec for main value axis.
            secondary_value_axis: Spec for secondary value axis.
            direction: option to set the direction for series in the Chart.
            tooltips: Tooltip items to show in the tooltip.
        """
        super().__init__()
        self.__data = data
        self.__tooltips = tooltips
        self.__value_axis: Optional[ValueAxis] = self.__set_value_axis(value_axis)
        self.__secondary_value_axis: Optional[ValueAxis] = (
            self.__set_secondary_value_axis(secondary_value_axis)
        )
        self.__category_axis: CategoryAxis = self.__set_category_axis(
            category_axis, value_axis
        )
        self.__verify_axis()
        self.__direction = direction
        self._dependency_id = ""
        self._json_data = None

    def __verify_axis(self) -> None:
        if self.__value_axis is None and self.__secondary_value_axis is None:
            raise CategoricalValueAxisAndSecondaryAxisNotFoundError

    def __extract_series(self, data: pd.DataFrame) -> Tuple[Any, Any]:
        try:
            series = data.drop(columns=self.__category_axis.data_column)
        except KeyError as e:
            raise CategoricalValidateDataColumnNotFoundError(
                self.__class__.__name__,
                str(self.__category_axis.data_column),
                "data_column",
            ) from e

        if (
            not (series.dtypes == "int64").any()
            and not (series.dtypes == "float64").any()
        ):
            raise CategoricalSeriesDataColumnNotNumericError(
                series_class_name=self.__class__.__name__,
            )
        numeric_series = series.select_dtypes(include=["int64", "float64"])
        tooltip_series = series.select_dtypes(exclude=["int64", "float64"])

        return tooltip_series, numeric_series

    def __set_default_tooltips(self, value_series: pd.DataFrame) -> None:
        if not value_series.empty and self.__tooltips is None:
            self.__tooltips = []
            for column, column_data in value_series.items():
                if column_is_of_type(column_data, (int, str, float, Decimal)):
                    self.__tooltips.append(TextTooltipItem(data_column=column))
                elif column_is_of_type(column_data, (pd.Timestamp, datetime.date)):
                    self.__tooltips.append(DatetimeTooltipItem(data_column=column))

    def __set_category_axis(
        self,
        category_axis: Union[str, WidgetField, CategoryAxis],
        value_axis: Optional[Union[ValueAxisSeries, ValueAxis]] = None,
    ) -> CategoryAxis:
        if self.__data is not None and value_axis is None:
            self.__category_axis = (
                CategoryAxis(data_column=category_axis)
                if isinstance(category_axis, (str, WidgetField))
                else category_axis
            )
            tooltip_series, numeric_series = self.__extract_series(self.__data)

            self.__value_axis = ValueAxis(
                series=[ColumnSeries(data_column=series) for series in numeric_series]
            )
            self.__set_default_tooltips(tooltip_series)

        else:
            self.__category_axis = (
                category_axis
                if isinstance(category_axis, CategoryAxis)
                else CategoryAxis(data_column=category_axis)
            )
        return self.__category_axis

    def __set_value_axis(
        self,
        value_axis: Optional[Union[ValueAxisSeries, ValueAxis]] = None,
    ) -> Optional[ValueAxis]:
        axis: Optional[ValueAxis] = None
        if value_axis is not None:
            axis = (
                value_axis
                if isinstance(value_axis, ValueAxis)
                else (
                    ValueAxis(series=ColumnSeries(data_column=value_axis))
                    if isinstance(value_axis, (str, WidgetField))
                    else ValueAxis(series=value_axis)
                )
            )
        return axis

    def __set_secondary_value_axis(
        self,
        secondary_value_axis: Optional[Union[ValueAxisSeries, ValueAxis]] = None,
    ) -> Optional[ValueAxis]:
        axis: Optional[ValueAxis] = None
        if secondary_value_axis is not None:
            axis = (
                secondary_value_axis
                if isinstance(secondary_value_axis, ValueAxis)
                else (
                    ValueAxis(series=ColumnSeries(data_column=secondary_value_axis))
                    if isinstance(secondary_value_axis, (str, WidgetField))
                    else ValueAxis(series=secondary_value_axis)
                )
            )
        return axis

    def __build_tooltips(self) -> Optional[Dict[str, Any]]:
        return (
            {
                "data": build_data(path=self._dependency_id, json_data=self._json_data),
                "categoryIdKey": build_templated_strings(
                    items=self.__category_axis.data_column
                ),
                "items": [build_tooltip_item(item=item) for item in self.__tooltips],
            }
            if self.__tooltips
            else None
        )

    def validate(self, data: pd.DataFrame, **kwargs: Any) -> None:
        """Validate if Chart has all dataframe columns and axis dependencies.

        Args:
            data: Data associated with the series.

        Raises:
            CategoricalValueAxisAndSecondaryAxisNotFoundError: If no axis is defined.
        """
        self.__category_axis.validate(data=data, **kwargs)
        if self.__value_axis is not None:
            self.__value_axis.validate(data=data, **kwargs)
        if self.__secondary_value_axis is not None:
            self.__secondary_value_axis.validate(data=data, **kwargs)

    def prepare(self, dependency_id: str) -> None:
        """Prepares the Chart for use.

        Args:
            dependency_id: dependency ID of the Chart.
        """
        self._dependency_id = dependency_id

        if self.__value_axis:
            self.__value_axis.prepare(
                data_column=self.__category_axis.data_column,
            )

        if self.__secondary_value_axis:
            self.__secondary_value_axis.prepare(
                data_column=self.__category_axis.data_column,
            )

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "categoryAxis": self.__category_axis.build(),
            "valueAxis": [self.__value_axis.build()] if self.__value_axis else [],
            "valueAxisOpposite": (
                [self.__secondary_value_axis.build()]
                if self.__secondary_value_axis
                else []
            ),
            "tooltip": self.__build_tooltips(),
            "direction": self.__direction.value,
        }

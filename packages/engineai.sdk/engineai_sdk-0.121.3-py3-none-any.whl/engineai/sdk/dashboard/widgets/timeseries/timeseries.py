"""Spec for Timeseries widget."""

import math
import warnings
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union
from typing import cast

import pandas as pd

from engineai.sdk.dashboard import formatting
from engineai.sdk.dashboard.base import HEIGHT_ROUND_VALUE
from engineai.sdk.dashboard.data import DataSource
from engineai.sdk.dashboard.data.http import Http
from engineai.sdk.dashboard.data.manager.manager import StaticDataType
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.enum.legend_position import LegendPosition
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.base import Widget
from engineai.sdk.dashboard.widgets.base import WidgetTitleType
from engineai.sdk.dashboard.widgets.chart_utils import calculate_axis_ratios
from engineai.sdk.dashboard.widgets.chart_utils import process_scales
from engineai.sdk.dashboard.widgets.components.charts.toolbar import build_chart_toolbar
from engineai.sdk.dashboard.widgets.components.charts.typing import NumberTooltipItem
from engineai.sdk.dashboard.widgets.components.charts.typing import TextTooltipItem
from engineai.sdk.dashboard.widgets.utils import build_data

from .axis.y_axis.y_axis import YAxis
from .chart import Chart
from .exceptions import TimeseriesChartHeightOverflowError
from .exceptions import TimeseriesChartsEmptyDefinitionError
from .exceptions import TimeseriesChartsHeightNotUniformError
from .exceptions import TimeseriesChartsHeightSetError
from .exceptions import TimeseriesDataNoDatetimeIndexError
from .exceptions import TimeseriesDataWithoutColumnsError
from .exceptions import TimeseriesDateColumnNotFoundError
from .exceptions import TimeseriesDateColumnTypeError
from .exceptions import TimeseriesEmptyDateColumnError
from .exceptions import TimeseriesNoChartsDefinedError
from .exceptions import TimeseriesTooManyChartsError
from .legend import Legend
from .navigator import Navigator
from .period_selector.selector import PeriodSelector
from .series.line import LineSeries
from .series.typing import TimeseriesSeries

T = TypeVar("T", bound=Union[NumberTooltipItem, LineSeries])


class Timeseries(Widget):
    """Visualize charts, customize data, date, toolbar.

    Visualize multiple charts with date selector, navigator, legend.
    Customize data source, date column, toolbar. Enable or disable
    toolbar for enhanced user control.
    """

    _HEIGHT_TIMESERIES_PERIOD_SELECTOR = 0.32
    _HEIGHT_TIMESERIES_PERIOD_NAVIGATOR = 0.48
    _HEIGHT_TIMESERIES_LEGENDS_BOTTOM = 0.18
    _HEIGHT_TIMESERIES_LEGENDS_BOTTOM_GROUPED = 0.37
    _WIDGET_API_TYPE = "timeseries"
    _DEPENDENCY_ID = "__TIMESERIES_DATA_DEPENDENCY__"

    @type_check
    def __init__(
        self,
        data: Union[DataSource, pd.DataFrame, Http],
        *,
        charts: Optional[List[Union[str, TimeseriesSeries, Chart]]] = None,
        date_column: Optional[TemplatedStringItem] = None,
        widget_id: Optional[str] = None,
        period_selector: Optional[PeriodSelector] = None,
        title: Optional[WidgetTitleType] = None,
        legend: Optional[LegendPosition] = None,
        navigator: Optional[Union[Navigator, TimeseriesSeries]] = None,
        enable_toolbar: bool = True,
    ) -> None:
        """Constructor for Timeseries widget.

        Args:
            data: data to be used by widget. Accepts DataSource method as well as raw
                data.
            charts: list of charts to be added to the widget.
                Each element in the list is a new chart, with a maximum of 5 Charts.
            date_column: column that must be used as x axis date. This column must be
                of type datetime.
            widget_id: unique widget id in a dashboard.
            period_selector: selector for particular periods in a chart.
            title: title of widget can be either a string (fixed value) or determined
                by a value from another widget using a WidgetLink.
            legend: legend of timeseries widget.
            navigator: navigator added to the bottom of all charts to facilitate
                navigation.
            enable_toolbar: Enable/Disable toolbar flag.

        Examples:
            ??? example "Create a minimal timeseries widget"
                ```py linenums="1"
                import pandas as pd
                from engineai.sdk.dashboard.dashboard import Dashboard
                from engineai.sdk.dashboard.widgets import timeseries
                data = pd.DataFrame(
                    {
                        "value": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    },
                    index=pd.date_range("2020-01-01", "2020-01-10"),
                )
                Dashboard(content=timeseries.Timeseries(data=data))
                ```
        """
        super().__init__(widget_id=widget_id, data=data)
        self.__new_version = False
        self.__charts: List[Chart] = self.__set_charts(charts)
        self.__date_column = date_column
        self.__set_basic_timeseries(data=data)
        self.__period_selector = (
            period_selector if period_selector else PeriodSelector()
        )
        self.__set_navigator(navigator=navigator)
        self.__set_legend(legend=legend)
        self.__total_height: Union[int, float] = 0
        self.__title = title
        self._enable_toolbar = enable_toolbar
        self._json_data = None

    @property
    def date_column(self) -> TemplatedStringItem:
        """Get date column."""
        if self.__date_column is None:
            raise TimeseriesEmptyDateColumnError
        return self.__date_column

    def __set_charts(
        self, charts: Optional[List[Union[str, TimeseriesSeries, Chart]]]
    ) -> List[Chart]:
        result: List[Chart] = []

        if charts is not None:
            if len(charts) == 0:
                raise TimeseriesChartsEmptyDefinitionError

            if len(charts) > 5:
                raise TimeseriesTooManyChartsError(widget_id=self.widget_id)

            self.__new_version = True
            for item in charts:
                if isinstance(item, str):
                    result.append(Chart(left_y_axis=LineSeries(data_column=item)))
                elif isinstance(item, Chart):
                    result.append(item)
                else:
                    axis_position = {
                        (
                            "left_y_axis" if not item.is_right_axis else "right_y_axis"
                        ): item
                    }
                    result.append(Chart(**axis_position))

        return result

    def __set_basic_timeseries(
        self, data: Union[DataSource, pd.DataFrame, Http]
    ) -> None:
        """Set basic timeseries widget."""
        if self.__new_version:
            return
        if isinstance(data, pd.DataFrame):
            if len(data.columns) == 0:
                raise TimeseriesDataWithoutColumnsError

            self.__set_date_column(data=data)
            self.__adapt_timeseries(data=data)

        if self.__date_column == "":
            raise TimeseriesEmptyDateColumnError

    def __set_date_column(self, data: pd.DataFrame) -> None:
        if self.__date_column is None:
            if not isinstance(data.index, pd.DatetimeIndex):
                raise TimeseriesDataNoDatetimeIndexError
            self.__date_column = "__index"

    def __get_dataframe_columns(self, data: pd.DataFrame) -> List[str]:
        return [
            column
            for column in data.columns
            if (self.__is_numeric_column(data, column) and self.__date_column != column)
        ]

    @staticmethod
    def __is_numeric_column(data: pd.DataFrame, column_name: str) -> bool:
        try:
            pd.to_numeric(data[column_name], errors="raise")
        except (KeyError, ValueError, TypeError):
            return False
        return True

    def __adapt_timeseries(self, data: pd.DataFrame) -> None:
        scales = process_scales(data=data)

        ratios = calculate_axis_ratios(scales=scales)

        # create axis specs based on groups of scales

        axis_list: List[YAxis] = []
        tooltips: List[Union[NumberTooltipItem, TextTooltipItem]] = []
        if ratios:
            group_counter = 1
            for value in ratios.values():
                if group_counter <= 2:
                    group_counter += 1
                    decimals_col = self.__get_round_column(value[0])
                    axis = YAxis(
                        series=self.__create_timeseries_specs(
                            group=value,
                            scales=scales,
                            spec_class=LineSeries,
                        ),
                        formatting=formatting.AxisNumberFormatting(
                            decimals=int(scales[decimals_col].iloc[-1])
                        ),
                    )
                    axis_list.append(axis)
                else:
                    tooltips += self.__create_timeseries_specs(
                        group=value,
                        scales=scales,
                        spec_class=NumberTooltipItem,
                    )
                    tooltips += self.__set_tooltips(data=data)

            self.set_charts(
                Chart(
                    left_y_axis=axis_list[0],
                    right_y_axis=axis_list[1] if len(axis_list) > 1 else None,
                    tooltips=list(tooltips),
                )
            )
        else:
            self.set_series(*self.__get_dataframe_columns(data=data))

    def __get_round_column(self, column: str) -> str:
        return f"{column.lower().replace(' ', '_')}_round"

    def __create_timeseries_specs(
        self,
        group: List[str],
        scales: pd.DataFrame,
        spec_class: Type[T],
    ) -> List[T]:
        # This is an auxiliary method to create the axis specs based on specs class.
        result: List[T] = []

        for element in group:
            decimals_col = self.__get_round_column(element)

            current_spec: Dict[str, Any] = (
                {
                    "formatting": formatting.NumberFormatting(
                        decimals=int(scales[decimals_col].iloc[-1])
                    ),
                    "label": element.replace("_", " ").title(),
                }
                if spec_class == NumberTooltipItem
                else {}
            )

            result.append(
                spec_class(
                    data_column=element,
                    **current_spec,
                )
            )

        return result

    def __has_positive_and_negative_value(self, data: pd.Series) -> bool:
        return (data > 0).any() and (data < 0).any()

    def __set_tooltips(self, data: pd.DataFrame) -> List[TextTooltipItem]:
        return [
            TextTooltipItem(data_column=column)
            for column in data.columns
            if pd.api.types.is_string_dtype(data[column].dtype)
        ]

    def __set_legend(self, legend: Optional[LegendPosition]) -> None:
        self.__legend = (
            Legend(position=legend) if isinstance(legend, LegendPosition) else Legend()
        )

    def __set_navigator(
        self, navigator: Optional[Union[Navigator, TimeseriesSeries]]
    ) -> None:
        if navigator is None or isinstance(navigator, Navigator):
            self.__navigator = navigator
        else:
            self.__navigator = Navigator(navigator)

    @type_check
    def set_series(self, *items: Union[str, TimeseriesSeries]) -> "Timeseries":
        """Set series for timeseries chart, change type.

        Allows users to set series for a chart within a timeseries widget.
        Add multiple series to the same chart using this method, enabling the
        visualization of various data metrics on a single chart.

        Args:
            items: series to be added to timeseries widget, using this method you can
                add multiple series to the same chart. If you want to add multiple
                charts to the same widget, use set_charts method instead.

                By default, when adding a series, the series will be a line series,
                if you want to change the type of series, you can pass
                on series at your choice.

        Notes:
            If you use set_series method more than once, the previous series
            will be replaced by the new one, same behavior as set_charts method.
        """
        warnings.warn(
            "`set_series` method is deprecated and it will be removed in the future.",
            DeprecationWarning,
        )

        if len(items) == 0:
            raise TimeseriesChartsEmptyDefinitionError

        return self.set_charts(
            Chart(
                left_y_axis=self.__y_left_axis(*items),
                right_y_axis=self.__y_right_axis(*items),
            )
        )

    @staticmethod
    def __y_left_axis(*items: Union[str, TimeseriesSeries]) -> Optional[YAxis]:
        series: List[TimeseriesSeries] = []

        for item in items:
            if isinstance(item, str):
                series.append(LineSeries(data_column=item))
            elif not item.is_right_axis:
                series.append(item)

        return YAxis(series=series) if len(series) > 0 else None

    @staticmethod
    def __y_right_axis(*items: Union[str, TimeseriesSeries]) -> Optional[YAxis]:
        series: List[TimeseriesSeries] = [
            item
            for item in list(items)
            if not isinstance(item, str) and item.is_right_axis
        ]
        return YAxis(series=series) if len(series) > 0 else None

    @type_check
    def set_charts(self, *items: Union[str, TimeseriesSeries, Chart]) -> "Timeseries":
        """Set charts for timeseries widget.

        Allows the addition of one or more charts to a timeseries widget.
        Include multiple charts within the same widget using this method,
        allowing for the simultaneous visualization of
        diverse datasets or metrics

        Args:
            items: chart(s) to be added to timeseries widget, using this method you
                can add multiple charts to the same widget.

        Notes:
            If you use set_charts method more than once, the previous charts
            will be replaced by the new one, same behavior as set_series method.
        """
        warnings.warn(
            "`set_charts` method is deprecated and it will be removed in the future.",
            DeprecationWarning,
        )

        if len(items) == 0:
            raise TimeseriesChartsEmptyDefinitionError

        if len(items) > 5:
            raise TimeseriesTooManyChartsError(widget_id=self.widget_id)

        self.__total_height = 0
        self.__charts = []

        for item in items:
            self.__charts.append(self.__get_chart(item=item))

        return self

    def __get_chart(self, item: Union[str, TimeseriesSeries, Chart]) -> Chart:
        """Get chart."""
        if isinstance(item, str):
            chart = Chart(left_y_axis=LineSeries(data_column=item))
        elif isinstance(item, Chart):
            chart = item
        else:
            chart = (
                Chart(right_y_axis=item)
                if item.is_right_axis
                else Chart(left_y_axis=item)
            )

        self.__validate_chart(chart=chart)

        if chart.height_percentage is not None:
            self.__total_height += chart.height_percentage

        return chart

    def __validate_chart(self, chart: Chart) -> None:
        self.__validate_chart_height_percentage(chart=chart)
        self.__validate_total_height(chart=chart)

    def __validate_chart_height_percentage(self, chart: Chart) -> None:
        if (
            chart.height_percentage is not None
            and any(chart.height_percentage is None for chart in self.__charts)
            or chart.height_percentage is None
            and any(chart.height_percentage is not None for chart in self.__charts)
        ):
            raise TimeseriesChartsHeightSetError(widget_id=self.widget_id)

    def __validate_total_height(self, chart: Chart) -> None:
        if (
            chart.height_percentage is not None
            and chart.height_percentage + self.__total_height > 1
        ):
            raise TimeseriesChartHeightOverflowError(
                widget_id=self.widget_id,
                total_height=self.__total_height,
                height_percentage=chart.height_percentage,
            )

    def validate(self, data: pd.DataFrame, **_: Any) -> None:
        """Validates widget spec.

        Args:
            data: pandas DataFrame where the data is present.
        """
        self.__validate_date_column(data=data)
        self.__validate_dataframe(data=data)

    def __validate_date_column(self, data: pd.DataFrame) -> None:
        """Validates Timeseries date column.

        Args:
            data: pandas DataFrame where the data is present.
        """
        if isinstance(self.__date_column, str) and self.__date_column != "__index":
            if self.__date_column not in data.columns:
                raise TimeseriesDateColumnNotFoundError

            if not pd.api.types.is_datetime64_any_dtype(data[self.__date_column]):
                raise TimeseriesDateColumnTypeError(
                    current_type=str(type(data[self.__date_column].dtype))
                )

    def __validate_dataframe(
        self,
        *,
        data: pd.DataFrame,
    ) -> None:
        if self.__navigator:
            self.__navigator.validate(data=data)

        for chart in self.__charts:
            chart.validate(
                data=data,
            )

    def _prepare(self, **kwargs: object) -> None:
        """Method that prepares the spec to be built."""
        self.__period_selector.prepare()

        if len(self.__charts) == 0:
            raise TimeseriesNoChartsDefinedError(widget_id=self.widget_id)

        for chart in self.__charts:
            if chart.height_percentage is None:
                chart.height_percentage = 1 / len(self.__charts)
                self.__total_height += 1 / len(self.__charts)
            chart.prepare(cast(TemplatedStringItem, self.__date_column))

        if self.__navigator is not None:
            self.__navigator.prepare(cast(TemplatedStringItem, self.__date_column))

        if (
            any(c.height_percentage is not None for c in self.__charts)
            and self.__total_height < 0.99
        ):
            raise TimeseriesChartsHeightNotUniformError(
                self.widget_id, total_height=self.__total_height
            )

        self._json_data = kwargs.get("json_data")

    @property
    def height(self) -> float:
        """Calculates the automatic height for Timeseries widget."""
        height: Union[int, float] = sum(chart.height for chart in self.__charts)
        height += self._HEIGHT_TIMESERIES_PERIOD_SELECTOR

        if self.__legend.position == LegendPosition.BOTTOM:
            height += len(self.__charts) * self._HEIGHT_TIMESERIES_LEGENDS_BOTTOM
        elif self.__legend.position == LegendPosition.BOTTOM_GROUPED:
            height += self._HEIGHT_TIMESERIES_LEGENDS_BOTTOM_GROUPED

        height += self._HEIGHT_TIMESERIES_PERIOD_NAVIGATOR if self.__navigator else 0

        return round(
            int(math.ceil(height / self._WIDGET_HEIGHT_STEP))
            * self._WIDGET_HEIGHT_STEP,
            HEIGHT_ROUND_VALUE,
        )

    def _build_widget_input(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "title": (
                build_templated_strings(items=self.__title) if self.__title else None
            ),
            "charts": self._build_charts(),
            "data": build_data(path=self.dependency_id, json_data=self._json_data),
            "periodSelector": self.__period_selector.build(),
            "legend": self.__legend.build(),
            "navigator": self.__navigator.build() if self.__navigator else None,
            "toolbar": build_chart_toolbar(enable=self._enable_toolbar),
        }

    def _build_charts(self) -> List[Any]:
        return [chart.build() for chart in self.__charts]

    def post_process_data(self, data: StaticDataType) -> StaticDataType:
        """Post process data."""
        if self.date_column != "__index":
            data[f"__{self.date_column}"] = data[self.date_column]
            data = data.set_index(f"__{self.date_column}")
        return data

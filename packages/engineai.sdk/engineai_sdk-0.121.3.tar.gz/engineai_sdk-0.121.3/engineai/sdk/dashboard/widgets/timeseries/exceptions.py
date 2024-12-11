"""Specs for Errors Timeseries."""

from typing import Union

from engineai.sdk.dashboard.exceptions import BaseDataValidationError
from engineai.sdk.dashboard.exceptions import EngineAIDashboardError
from engineai.sdk.dashboard.widgets.exceptions import DashboardWidgetError


class TimeseriesError(DashboardWidgetError):
    """Timeseries Widget Base Exception."""

    CLASS_NAME = "Timeseries"


class TimeseriesValidateSeriesDataColumnNotFoundError(BaseDataValidationError):
    """Timeseries Widget Validate Series no data columns found."""

    def __init__(
        self,
        series_class_name: str,
        column_name: str,
        column_value: str,
    ) -> None:
        """Constructor for TimeseriesValidateSeriesDataColumnNotFoundError class.

        Args:
            series_class_name: Timeseries series class name.
            column_name: data column name.
            column_value: data column value.
        """
        super().__init__(
            f"Missing {column_name}='{column_value}' in "
            f"Data for the {series_class_name}."
        )


class TimeseriesDifferentAxisTypeError(EngineAIDashboardError):
    """Timeseries Widget Different Axis Type Error."""

    def __init__(self, *args: object) -> None:
        """Constructor for TimeseriesDifferentAxisTypeError class."""
        super().__init__(*args)
        self.error_strings.append(
            "Different Y Axis type are not allowed in the same Chart."
        )


class TimeseriesChartBothAxisNotDefinedError(EngineAIDashboardError):
    """Timeseries Chart Both Axis Not Defined Error."""

    def __init__(self, *args: object) -> None:
        """Constructor for TimeseriesChartBothAxisNotDefinedError class."""
        super().__init__(*args)
        self.error_strings.append(
            "Both 'left_y_axis' and 'right_y_axis' are not defined. "
            "Please define at least one."
        )


class TimeseriesDataNoDatetimeIndexError(EngineAIDashboardError):
    """Timeseries Widget Data No Datetime Index Error."""

    def __init__(self, *args: object) -> None:
        """Constructor for TimeseriesDataNoDatetimeIndexError class."""
        super().__init__(*args)
        self.error_strings.append("Dataframe index must be of type DatetimeIndex.")


class TimeseriesTooManyChartsError(TimeseriesError):
    """Timeseries Widget Too Many Charts Error."""

    def __init__(self, widget_id: str, *args: object) -> None:
        """Constructor for TimeseriesTooManyChartsError class.

        Args:
            widget_id: widget id.
        """
        super().__init__(widget_id, *args)
        self.error_strings.append(f"Cannot add more then 5 charts {widget_id=}.")


class TimeseriesChartHeightOverflowError(TimeseriesError):
    """Timeseries Widget Chart Height Overflow Error."""

    def __init__(
        self,
        widget_id: str,
        total_height: float,
        height_percentage: float,
        *args: object,
    ) -> None:
        """Constructor for TimeseriesChartHeightOverflowError class.

        Args:
            widget_id: widget id.
            total_height: current total height.
            height_percentage: new chart height_percentage argument.
        """
        super().__init__(widget_id, total_height, height_percentage, *args)
        self.error_strings.append(
            "Adding chart would result in height overflow: "
            f"{total_height + height_percentage} = "
            f"{total_height} + {height_percentage} (new chart)."
        )


class TimeseriesChartsHeightSetError(TimeseriesError):
    """Timeseries Charts Height Set Error."""

    def __init__(self, widget_id: str, *args: object) -> None:
        """Constructor for TimeseriesChartsHeightSetError class.

        Args:
            widget_id: widget id.
        """
        super().__init__(widget_id, *args)
        self.error_strings.append(
            "All TimeseriesChart must have 'height_percentage' argument set or "
            "none should have it set."
        )


class TimeseriesChartsHeightNotUniformError(TimeseriesError):
    """Timeseries Charts Height Not Uniform Error."""

    def __init__(
        self, widget_id: str, total_height: Union[int, float], *args: object
    ) -> None:
        """Constructor for TimeseriesChartsHeightNotUniformError class.

        Args:
            widget_id: widget id.
            total_height: charts total height.
        """
        super().__init__(widget_id, total_height, *args)
        self.error_strings.append(
            f"Total height percentage of timeseries widget {widget_id} "
            f"does not sum up to 1 (total height: {total_height})"
        )


class TimeseriesHeightWrongDefinitionError(TimeseriesError):
    """Timeseries Height Wrong Definition Error."""

    def __init__(self, *args: object) -> None:
        """Constructor for TimeseriesHeightWrongDefinitionError class."""
        super().__init__(None, *args)
        self.error_strings.append(
            "The `height` value must be between 2 and 10, for charts inside a "
            "Timeseries Widget."
        )


class TimeseriesHeightUnitWrongDefinitionError(TimeseriesError):
    """Timeseries Height Unit Wrong Definition Error."""

    def __init__(self, *args: object) -> None:
        """Constructor for TimeseriesHeightUnitWrongDefinitionError class."""
        super().__init__(None, *args)
        self.error_strings.append(
            "Height units for Timeseries Charts must have a 0.5 step increments "
            "(e.g. 1, 1.5, 2, 2.5, etc.)"
        )


class TimeseriesPeriodSelectorNoAvailableDefaultOptionError(TimeseriesError):
    """Timeseries Period Selector No Available Default Option Error."""

    def __init__(self, periods_len: int, option: int, *args: object) -> None:
        """Construct for TimeseriesPeriodSelectorNoAvailableDefaultOptionError class.

        Args:
            periods_len: number of periods added into TimeseriesPeriodSelector.
            option: selected option to be the default selection.
        """
        super().__init__(None, periods_len, option, *args)
        self.error_strings.append(
            f"The '{option=}' inserted for TimeseriesPeriodSelector default selection "
            f"is not available. TimeseriesPeriodSelector only has '{periods_len}' "
            "periods added."
        )


class TimeseriesPeriodSelectorDatesDefinitionError(TimeseriesError):
    """Timeseries Period Selector Dates Definition Error."""

    def __init__(self, start_date: int, end_date: int, *args: object) -> None:
        """Construct for TimeseriesPeriodSelectorDatesDefinitionError class.

        Args:
            start_date: start date of custom period in a format supported by
                pandas.to_datetime.
            end_date: end date of custom period in a format supported by
                pandas.to_datetime.
        """
        super().__init__(None, start_date, end_date, *args)
        self.error_strings.append(
            f"End date {end_date} needs to be greater than start date {start_date}"
        )


class TimeseriesPeriodSelectorHiddenPeriodsError(TimeseriesError):
    """Timeseries Period Selector Hidden Periods Error."""

    def __init__(self, *args: object) -> None:
        """Construct for TimeseriesPeriodSelectorHiddenPeriodsError class."""
        super().__init__(None, *args)
        self.error_strings.append(
            "Period selector has periods but it is defined as not visible. Please "
            "make sure that if periods were added they are visible or vice-versa."
        )


class TimeseriesDataWithoutColumnsError(TimeseriesError):
    """Timeseries Data Without Columns Error."""

    def __init__(self, *args: object) -> None:
        """Constructor for TimeseriesDataWithoutColumnsError class."""
        super().__init__(None, *args)
        self.error_strings.append(
            "The data passed to the Timeseries widget does not have columns."
        )


class TimeseriesChartsEmptyDefinitionError(TimeseriesError):
    """Timeseries Charts Empty Definition Error."""

    def __init__(self, *args: object) -> None:
        """Constructor for TimeseriesChartsEmptyDefinitionError class."""
        super().__init__(None, *args)
        self.error_strings.append(
            "`set_charts` methods was called without any instances. "
            "Please define at least one."
        )


class TimeseriesSeriesEmptyDefinitionError(TimeseriesError):
    """Timeseries Series Empty Definition Error."""

    def __init__(self, *args: object) -> None:
        """Constructor for TimeseriesSeriesEmptyDefinitionError class."""
        super().__init__(None, *args)
        self.error_strings.append(
            "`set_series` methods was called without any instances. "
            "Please define at least one."
        )


class TimeseriesAxisEmptyDefinitionError(TimeseriesError):
    """Timeseries Axis Empty Definition Error."""

    def __init__(self, *args: object) -> None:
        """Construct for TimeseriesAxisEmptyDefinitionError class.

        Args:
            duplicated_labels (List[str]): found duplicated labels.
        """
        super().__init__(None, *args)
        self.error_strings.append(
            "`add_series` method was called without any series instances. "
            "Please define at least one series."
        )


class TimeseriesNavigatorEmptyDefinitionError(TimeseriesError):
    """Timeseries Navigator Empty Definition Error."""

    def __init__(self, *args: object) -> None:
        """Constructor for TimeseriesNavigatorEmptyDefinitionError class."""
        super().__init__(None, *args)
        self.error_strings.append(
            "Navigator instance was called without any series. "
            "Please define at least one series."
        )


class TimeseriesTransformScalarRequiredError(TimeseriesError):
    """Timeseries Transform Scalar Required Error."""

    def __init__(self, transformation: str, *args: object) -> None:
        """Constructor for TimeseriesTransformScalarRequiredError class."""
        super().__init__(None, transformation, *args)
        self.error_strings.append(f"Transformation {transformation} requires a scalar.")


class TimeseriesEmptyDateColumnError(TimeseriesError):
    """Timeseries Empty Date Column Error."""

    def __init__(self, *args: object) -> None:
        """Constructor for TimeseriesEmptyDateColumnError class."""
        super().__init__(None, *args)
        self.error_strings.append(
            "Date column is empty. Please make sure that the date column is not empty."
        )


class TimeseriesDateColumnNotFoundError(BaseDataValidationError):
    """Timeseries Date Column Not Found Error."""

    def __init__(self) -> None:
        """Constructor for TimeseriesDateColumnNotFoundError class."""
        super().__init__("No date column found on the Widget data.")


class TimeseriesDateColumnTypeError(BaseDataValidationError):
    """Timeseries Date Column Value Error."""

    def __init__(self, current_type: str) -> None:
        """Constructor for TimeseriesDateColumnValueError class."""
        super().__init__(
            "Date column type is not supported (current type: "
            f"{current_type}). Please make sure that the date column is of type "
            "'datetime64'."
        )


class TimeseriesNoChartsDefinedError(TimeseriesError):
    """Timeseries No Charts Defined Error."""

    def __init__(self, widget_id: str, *args: object) -> None:
        """Constructor for TimeseriesNoChartsDefinedError class."""
        super().__init__(widget_id, *args)
        self.error_strings.append("No charts defined for the Timeseries Widget.")


class TimeseriesWrongSeriesAxisError(EngineAIDashboardError):
    """Timeseries Wrong Series Axis Error."""

    def __init__(self, *args: object) -> None:
        """Constructor for TimeseriesWrongSeriesAxisError class."""
        super().__init__(*args)
        self.error_strings.append(
            "Using a Series with `right_axis` set as True when "
            "defining the left Y Axis in a Chart."
        )

"""Common charts Exceptions."""

from typing import Any

from engineai.sdk.dashboard.exceptions import BaseDataValidationError
from engineai.sdk.dashboard.exceptions import EngineAIDashboardError


class CommonChartsError(EngineAIDashboardError):
    """Common Charts Base Exception."""

    def __init__(self, class_name: str, *args: object) -> None:
        """Constructor for Common Charts Error.

        Args:
            class_name (str): class type.
        """
        super().__init__(class_name, *args)
        self.error_strings.append(f"{class_name} class error.")


class ChartScaleSymmetricValueError(CommonChartsError):
    """Common Charts Base Exception."""

    def __init__(self, class_name: str, *args: object) -> None:
        """Constructor for Chart Scale Symmetric Value Error.

        Args:
            class_name (str): class type.
        """
        super().__init__(class_name, *args)
        self.error_strings.append(
            "Cannot set `min_value`, `max_value` and `strict` arguments."
        )


class ChartStylingMissingDataColumnError(CommonChartsError):
    """Chart Missing Data Column if Color Selected Error."""

    def __init__(self, class_name: str, *args: object) -> None:
        """Constructor for Chart Styling Missing Data ColumnError.

        Args:
            class_name (str): class type.
        """
        super().__init__(class_name, *args)
        self.error_strings.append(
            "Argument data_column cannot be None if color_spec is a "
            "ColorDiscreteMap or a ColorGradient class."
        )


class ChartStylingNoDataColumnError(BaseDataValidationError):
    """Chart Missing Data Column if Color Selected Error."""

    def __init__(
        self,
        class_name: str,
        data_column: str,
    ) -> None:
        """Constructor for ChartStylingNoDataColumnError class.

        Args:
            class_name (str): styling class type.
            data_column (str): data columns.
        """
        super().__init__(
            f"Missing data column {data_column=} used for {class_name} in Data."
        )


class ChartSeriesEntityInvalidCountryCodeError(CommonChartsError):
    """Chart Series Entity Invalid Country Code Error."""

    def __init__(self, class_name: str, country_code: str, *args: object) -> None:
        """Constructor for Chart Styling Missing Data ColumnError.

        Args:
            class_name: class type.
            country_code: country code.
        """
        super().__init__(class_name, country_code, *args)
        self.error_strings.append(f"{country_code=} is not a valid country code.")


class ChartSeriesEntityNoDataColumnError(BaseDataValidationError):
    """Chart Series Entity Data Column Error."""

    def __init__(
        self,
        class_name: str,
        data_column: str,
    ) -> None:
        """Constructor for ChartSeriesEntityNoDataColumnError class.

        Args:
            class_name (str): styling class type.
            data_column (str): data columns.
        """
        super().__init__(f"Missing {data_column=} used for {class_name} in Data.")


class ChartNoDataColumnError(BaseDataValidationError):
    """Chart Missing Data Column Error."""

    def __init__(
        self,
        data_column: str,
    ) -> None:
        """Constructor for ChartNoDataColumnError class.

        Args:
            data_column (str): class type.
        """
        super().__init__(f"Column {data_column=} not found in chart data.")


class ChartBandsConfigError(CommonChartsError):
    """Chart Bands Config Error."""

    def __init__(
        self,
        class_name: str,
        axis: str,
        *args: object,
    ) -> None:
        """Constructor for ChartBandsConfigError class.

        Args:
            class_name (str): class type.
            widget_id (str): id that belongs to the widget that failed.
            axis (str): axis where the error was caused.
        """
        super().__init__(class_name, axis, *args)
        self.error_strings.append(
            f"All Bands for the {class_name} {axis} Axis must have the "
            "`styling` attribute defined or set as None, which sets the "
            "color automatically."
        )


class ChartDependencyNotFoundError(CommonChartsError):
    """Chart Dependency Not Found Error."""

    def __init__(
        self,
        class_name: str,
        widget_id: str,
        band: bool,
        dependency_id: str,
        *args: object,
    ) -> None:
        """Constructor for ChartDependencyNotFoundError class.

        Args:
            class_name (str): class type.
            widget_id (str): id that belongs to the widget that failed.
            band (bool): flag that defines if the error comes from a band or a line.
            dependency_id (str): id of the dependency where the error was ocurred.
        """
        component = "Band" if band else "Line"
        super().__init__(class_name, widget_id, band, dependency_id, *args)
        self.error_strings.append(
            f"Missing dependency {dependency_id} in "
            f"one Axis {component} used in the {class_name} Chart in "
            f"{widget_id=}."
        )


class ChartSeriesNameAlreadyExistsError(CommonChartsError):
    """Chart Series Name Already Exists Error."""

    def __init__(
        self,
        class_name: str,
        series_name: Any,
        *args: object,
    ) -> None:
        """Constructor for ChartSeriesNameAlreadyExistsError class.

        Args:
            class_name (str): class type.
            series_name (Any): the name of the series that is causing the error.
                It can be a str, WidgetLink or DashboardRouteLink.
        """
        super().__init__(class_name, series_name, *args)
        self.error_strings.append(f"A {class_name} with {series_name=} already exists.")


class ChartAxisBandStylingNotDefinedError(CommonChartsError):
    """Chart Axis Styling Not Defined Error."""

    def __init__(self, class_name: str, *args: object) -> None:
        """Constructor for ChartAxisBandStylingNotDefinedError class."""
        super().__init__(class_name, *args)
        self.error_strings.append(
            "Band `styling` is None, make sure all bands have the `styling` defined."
        )


class SeriesMissingLabelError(EngineAIDashboardError):
    """Common Chart missing Label Error."""

    def __init__(self, class_name: str, *args: object) -> None:
        """Construct for SeriesMissingLabelError class."""
        super().__init__(class_name, *args)
        self.error_strings.append(
            f"Series ({class_name}) needs to have the label argument set. "
            "Both name and data_column are None."
        )


class SeriesUnsupportedDataColumnError(EngineAIDashboardError):
    """Common Chart missing Label Error."""

    def __init__(self, class_name: str, *args: object) -> None:
        """Construct for SeriesUnsupportedDataColumnError class."""
        super().__init__(class_name, *args)
        self.error_strings.append(
            f"Series ({class_name}) needs to have the label argument set, when "
            f"using WidgetLinks as data_column."
        )

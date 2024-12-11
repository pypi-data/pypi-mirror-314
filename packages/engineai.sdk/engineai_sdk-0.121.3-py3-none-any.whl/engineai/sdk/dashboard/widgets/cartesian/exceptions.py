"""Continuous Cartesian Exceptions."""

from engineai.sdk.dashboard.exceptions import BaseDataValidationError
from engineai.sdk.dashboard.widgets.exceptions import DashboardWidgetError


class CartesianError(DashboardWidgetError):
    """Continuous Cartesian Base Exception."""

    CLASS_NAME = "Cartesian"


class CartesianValidateDataColumnNotFoundError(BaseDataValidationError):
    """Cartesian Widget Validate No Data Error."""

    def __init__(
        self,
        class_name: str,
        column_name: str,
        column_value: str,
    ) -> None:
        """Constructor for CartesianValidateSeriesDataColumnNotFoundError class.

        Args:
            class_name: Cartesian series class name.
            column_name: data column name.
            column_value: data column value.
        """
        super().__init__(
            f"Missing {column_name}='{column_value}' in Data for the {class_name}."
        )


class CartesianMissingChartAxisError(CartesianError):
    """Cartesian Widget Validate Missing Chart and Axis Error."""

    def __init__(self, *args: object) -> None:
        """Constructor for CartesianMissingChartAxisError class."""
        super().__init__(None, *args)
        self.error_strings.append(
            "Chart information not found. Please ensure that either "
            "the x_axis and left_y_axis or right_y_axis arguments are not empty. "
            "You can also provide data as a DataFrame with Y axis values."
        )

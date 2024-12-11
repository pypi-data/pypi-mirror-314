"""Categorical Exceptions."""

from typing import Optional

from engineai.sdk.dashboard.exceptions import BaseDataValidationError
from engineai.sdk.dashboard.widgets.exceptions import DashboardWidgetError


class CategoricalError(DashboardWidgetError):
    """Categorical Base Exception."""

    CLASS_NAME = "Categorical"


class CategoricalValueAxisAndSecondaryAxisNotFoundError(CategoricalError):
    """Categorical Value Axis and Secondary Axis Not Found Error."""

    def __init__(
        self,
        *args: object,
    ) -> None:
        """Constructor for CategoricalValueAxisAndSecondaryAxisNotFoundError class."""
        super().__init__(None, *args)
        self.error_strings.append(
            "value_axis and secondary_value_axis not found. "
            "You need to set at least one."
        )


class CategoricalNoSeriesDefinedError(CategoricalError):
    """Categorical No Series Defined Error."""

    def __init__(
        self,
        *args: object,
    ) -> None:
        """Constructor for CategoricalNoSeriesDefinedError class.

        Args:
            widget_id: Unique widget ID in the dashboard.
        """
        super().__init__(None, *args)
        self.error_strings.append(
            "No series defined for the Categorical Widget. "
            "There has to be at least one."
        )


class CategoricalSeriesDataColumnNotNumericError(BaseDataValidationError):
    """Categorical Widget Series Data Column Not Numeric Error."""

    def __init__(
        self,
        series_class_name: str,
        column_name: Optional[str] = None,
    ) -> None:
        """Constructor for CategoricalSeriesDataColumnNotNumericError class.

        Args:
            series_class_name: Categorical series class name.
            column_name: data column name.
        """
        super().__init__(
            f"Data column `{column_name}` for the `{series_class_name}` "
            "is not numeric."
            if column_name
            else f"Value series data for the `{series_class_name}` has no numeric data."
        )


class CategoricalValidateDataColumnNotFoundError(BaseDataValidationError):
    """Categorical Widget Validate no data columns found."""

    def __init__(
        self,
        series_class_name: str,
        column_value: str,
        column_name: str,
    ) -> None:
        """Constructor for CategoricalValidateSeriesDataColumnNotFound class.

        Args:
            series_class_name: Categorical series class name.
            column_name: data column name.
            column_value: data column value.
        """
        super().__init__(
            f"Missing {column_name}='{column_value}' in Data "
            f"for the {series_class_name}."
        )

"""Table Columns Styling Exceptions."""

from engineai.sdk.dashboard.exceptions import BaseDataValidationError
from engineai.sdk.dashboard.widgets.table.exceptions import TableWidgetError


class TableColumnStylingValidationError(BaseDataValidationError):
    """TableColumn Styling Validation Error."""

    def __init__(self, class_name: str, data_column: str) -> None:
        """Constructor for TableColumnStylingValidationError class."""
        super().__init__(
            f"{class_name} data_column with {data_column=} not found in Data."
        )


class TableColumnStylingValueError(TableWidgetError):
    """TableColumn Styling Value Error."""

    def __init__(self, _class: str) -> None:
        """Constructor for TableColumnStylingValueError class."""
        super().__init__(
            widget_id=None,
        )
        self.error_strings.append(
            f"{_class} `data_column` argument cannot be None if `color_spec` is "
            f"ColorDiscreteMap or ColorGradient."
        )


class TableColumnStylingMinMaxValueError(TableWidgetError):
    """TableColumn Styling Color Bar Value Error."""

    def __init__(
        self, _class: str, min_value: float, max_value: float, *args: object
    ) -> None:
        """Constructor for TableColumnStylingMinMaxValueError class."""
        super().__init__(None, _class, min_value, max_value, *args)

        self.error_strings.append(
            f"{_class} Argument min_value {min_value} "
            f"needs be smaller than max_value {max_value}."
        )

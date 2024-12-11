"""Table Widget Exceptions."""

from typing import Any
from typing import Set

from engineai.sdk.dashboard.exceptions import BaseDataValidationError
from engineai.sdk.dashboard.widgets.table.exceptions import TableWidgetError


class TableColumnMissingLabelError(TableWidgetError):
    """Common TableColumn missing Label Error."""

    def __init__(self, class_name: str, *args: object) -> None:
        """Construct for TableColumnError class."""
        super().__init__(None, class_name, *args)
        self.error_strings.append(
            f"TableColumn ({class_name}) needs to have the label argument set, when "
            f"using WidgetLinks as data_column."
        )


class TableColumnDataTypeError(BaseDataValidationError):
    """TableColumn Data Type Error."""

    def __init__(self, data_column: Any, row_type: Any, types: str) -> None:
        """Constructor for TableColumnDataTypeError class."""
        super().__init__(
            f"Values inside {data_column=} in Data "
            f"does not have the right type ({row_type}). "
            f"The following types {types} needs to be provided."
        )


class TableColumnDataColumnNotFoundError(BaseDataValidationError):
    """TableColumn Data Type Error."""

    def __init__(
        self,
        column_name: str,
        column_value: str,
    ) -> None:
        """Constructor for TableColumnDataColumnNotFoundError class."""
        super().__init__(f"Missing {column_name}=`{column_value}` in Data.")


class TableDataColumnValueTypeError(BaseDataValidationError):
    """TableColumn Data Column Value Type Error."""

    def __init__(self, data_column: Any, value: Any) -> None:
        """Constructor for TableDataColumnValueTypeError class."""
        super().__init__(
            f"Values inside {data_column=} need to be a "
            f"dictionary. {type(value)} provided."
        )


class TableDataColumnValueKeyError(BaseDataValidationError):
    """TableColumn Data Column Value Key Error."""

    def __init__(self, data_column: Any, data_key: Any) -> None:
        """Constructor for TableDataColumnValueTypeError class."""
        super().__init__(
            f"Value inside {data_column=} does not contain "
            f"entries with {data_key=}."
        )


class TableCategoryColumnMappingError(BaseDataValidationError):
    """Table Category Column Mapping Error."""

    def __init__(
        self,
        data_column: Any,
        missing_formatting: Set[int],
    ) -> None:
        """Constructor for TableCategoryColumnMappingError class."""
        super().__init__(
            f"Values inside {data_column=} in Data has the following "
            f"values={missing_formatting} not included in the mapper formatting."
        )


class TableDatetimeColumnMappingError(BaseDataValidationError):
    """Table Datetime Column Mapping Error."""

    def __init__(self, data_column: Any) -> None:
        """Constructor for TableDatetimeColumnMappingError class."""
        super().__init__(
            f"Not all values from {data_column=} in Data have epoch datetimes."
        )


class TableRangeColumnValueError(BaseDataValidationError):
    """Table Range Column Value Error."""

    def __init__(self, data_column: Any, key: str) -> None:
        """Constructor for TableRangeColumnValueError class."""
        super().__init__(
            f"Values in {data_column=} do not "
            f"contain entries with {key=}. Each row must be "
            f"a dictionary with keys min, value and max."
        )


class TableColumnChartIncorrectLengthError(BaseDataValidationError):
    """Table Group Column Key Not Found Error."""

    def __init__(self, data_column: Any) -> None:
        """Constructor for TableColumnChartIncorrectLengthError class.

        Args:
            data_column: Table Group data column.
        """
        super().__init__(
            f"Length between styling and values must be same. "
            f"There are inconsistencies in data inside {data_column=}."
        )

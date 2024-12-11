"""Table Widget Exceptions."""

from typing import Any

from engineai.sdk.dashboard.exceptions import BaseDataValidationError
from engineai.sdk.dashboard.widgets.exceptions import DashboardWidgetError


class TableWidgetError(DashboardWidgetError):
    """Table Widget Base Exception."""

    CLASS_NAME = "Table"


class TableValidateDataTypeError(BaseDataValidationError):
    """Table Widget Validate Data Type Error."""

    def __init__(self, _type: Any) -> None:
        """Constructor for TableValidateDataTypeError class.

        Args:
            _type: provided data type.
        """
        super().__init__(f"Data is not a pandas DataFrame {_type} provided.")


class TableGroupColumnKeyNotFoundError(BaseDataValidationError):
    """Table Group Column Key Not Found Error."""

    def __init__(self, data_column: str) -> None:
        """Constructor for TableGroupColumnKeyNotFoundError class.

        Args:
            data_column: Table Group data column.
        """
        super().__init__(
            f"Table Group Column with {data_column=} does not exists on Data."
        )


class TableInitialStateIncompatiblePreSelectedRowsError(TableWidgetError):
    """Table Initial State Incompatible Pre Selected Rows Error."""

    def __init__(
        self, pre_selected_rows: int, row_selection: int, *args: object
    ) -> None:
        """Constructor for TableInitialStateIncompatiblePreSelectedRowsError class.

        Args:
            pre_selected_rows: initial state pre selected rows.
            row_selection: total of Table rows that can be selected.
        """
        super().__init__(None, pre_selected_rows, row_selection, *args)
        self.error_strings.append(
            f"The number of pre selected rows {pre_selected_rows} "
            f"is higher than the number of rows that can "
            f"be selected {row_selection}"
        )


class TableInitialStateIncompatiblePreSelectedIndexError(TableWidgetError):
    """Table Initial State Incompatible Pre Selected Index Error."""

    def __init__(
        self, pre_selected_max_index: int, dataframe_rows: int, *_: object
    ) -> None:
        """Constructor for TableInitialStateIncompatiblePreSelectedIndexError class.

        Args:
            pre_selected_max_index: initial state pre selected max index.
            dataframe_rows: total of Table rows.
        """
        super().__init__(None, pre_selected_max_index, dataframe_rows)
        self.error_strings.append(
            f"The index inserted: {pre_selected_max_index}, exceeds the total "
            f"number of available rows: {dataframe_rows}"
        )


class TableHeaderLevelsError(TableWidgetError):
    """TableHeader Levels Error."""

    def __init__(self, *args: object) -> None:
        """Constructor for TableHeaderLevelsError class."""
        super().__init__(None, *args)
        self.error_strings.append(
            "Adding too many TableHeaders layers. Maximum "
            "Header depth (max: 2 Headers depth)."
        )


class TableHeaderChildTypeError(TableWidgetError):
    """TableHeader Child Header Error."""

    def __init__(self, _type: Any, *args: object) -> None:
        """Constructor for TableHeaderChildTypeError class."""
        super().__init__(None, _type, *args)
        self.error_strings.append(
            f"Trying to build a child item with an invalid type inside a TableHeader. "
            f"Expecting TableHeader or TableColumn. {_type} provided."
        )


class TableDuplicatedItemIdError(TableWidgetError):
    """Table Widget Duplicated Item Ids Error."""

    def __init__(self, widget_id: str, item_ids: str) -> None:
        """Constructor for TableDuplicatedItemIdsError class.

        Args:
            widget_id: Table widget id.
            item_ids: List of duplicated Item Ids.
        """
        super().__init__(widget_id, item_ids)
        self.error_strings.append(
            f"The following {item_ids=} are duplicated. Please make sure that "
            "every 'item_id' is unique."
        )


class TableNoColumnError(TableWidgetError):
    """TableHeader Levels Error."""

    def __init__(self, *args: object) -> None:
        """Constructor for TableHeaderLevelsError class."""
        super().__init__(None, *args)
        self.error_strings.append(
            "Please specify the 'columns' argument for the 'Table' when "
            "using 'DataSource' or 'Http' as the data source. This argument is "
            "essential to determine which columns should be used. "
            "Alternatively, you can provide the data as a Pandas "
            "DataFrame for automatic column inference."
        )


class TableDataWithoutColumnsError(TableWidgetError):
    """Table Data Without Columns Error."""

    def __init__(self, *args: object) -> None:
        """Constructor for TableDataWithoutColumnsError class."""
        super().__init__(None, *args)
        self.error_strings.append(
            "The data passed to the Table widget does not have columns."
        )


class TableColumnsEmptyError(TableWidgetError):
    """Table With Columns Argument Empty Error."""

    def __init__(self, *args: object) -> None:
        """Constructor for TableDataWithoutColumnsError class."""
        super().__init__(None, *args)
        self.error_strings.append(
            "The columns argument is empty list. Please provide "
            "the necessary columns information."
        )

"""Content Widget Exceptions."""

from typing import Iterable
from typing import Optional
from typing import Union

from engineai.sdk.dashboard.exceptions import BaseDataValidationError
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.widgets.exceptions import DashboardWidgetError


class SearchWidgetError(DashboardWidgetError):
    """Search Widget Base Exception."""

    CLASS_NAME = "Search"


class SearchValidateNoDataColumnError(BaseDataValidationError):
    """Search Widget Validate No Data Column Error."""

    def __init__(self, data_column: TemplatedStringItem) -> None:
        """Constructor for SearchValidateNoDataColumnError class.

        Args:
            data_column: Name of column in pandas dataframe(s)
            used for search data.
        """
        super().__init__(f"Missing {data_column=} in Data.")


class SearchValidateNoValidDataTypeError(BaseDataValidationError):
    """Search Widget Validate No Valid Data Type Error."""

    def __init__(
        self,
        data_column: TemplatedStringItem,
        class_name: Optional[str] = None,
        required_types: Optional[Union[Iterable, str]] = None,
    ) -> None:
        """Constructor for SearchValidateNoValidDataTypeError class.

        Args:
            data_column: Name of column in pandas dataframe(s)
            used for search data.
            class_name: Name of class that requires all elements to be
            of type `required_types`.
            required_types: Required data types.
        """
        data_column = str(data_column)
        super().__init__(
            f"{data_column=} has ambiguous data types. Ensure all values are of the "
            "same type."
            if class_name is None and required_types is None
            else f"{data_column=} has ambiguous data types. `{class_name}` requires "
            f"all elements to be of type `{required_types}`."
        )


class SearchStylingMissingDataColumnError(SearchWidgetError):
    """Search Styling Missing Data Column Error."""

    def __init__(self, *args: object) -> None:
        """Constructor for SearchStylingMissingDataColumnError class."""
        super().__init__(None, *args)
        self.error_strings.append(
            "Argument 'data_column' cannot be None if color_spec is a "
            "ColorDiscreteMap or a ColorGradient class."
        )


class SearchNoSearchableColumnError(SearchWidgetError):
    """Search No Searchable Column Error."""

    def __init__(
        self, widget_id: str, selected_text_column: str, has_items: bool, *args: object
    ) -> None:
        """Constructor for SearchNoSearchableColumnError class.

        Args:
            widget_id: Search widget id.
            selected_text_column: Name of column in pandas dataframe(s)
                used for search data.
            has_items: if has items set by user.
        """
        super().__init__(widget_id, selected_text_column, has_items, *args)
        msg = (
            (
                "None of the added 'items' are searchable. "
                "Add at least one ResultTextItem that is searchable."
            )
            if has_items
            else (
                f"Column `{selected_text_column}` is not searchable. "
                "Please add a column containing only strings."
            )
        )
        self.error_strings.append(msg)

"""Spec for Table widget state."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import cast

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.decorator import type_check

from .exceptions import TableInitialStateIncompatiblePreSelectedIndexError
from .exceptions import TableInitialStateIncompatiblePreSelectedRowsError


class InitialState(AbstractFactory):
    """Define initial state for table widget.

    Define the initial state for the table widget,
    including the default page, search text, and pre-selected rows.
    """

    @type_check
    def __init__(
        self,
        *,
        page: int = 0,
        search_text: str = "",
        selected: Optional[List[str]] = None,
    ) -> None:
        """Constructor for InitialState.

        Args:
            page: the default initial page.
            search_text: Initial string in the search box.
            selected: List of rows pre-selected by default.
        """
        super().__init__()
        self.__page = page
        self.__search_text = search_text
        self.__selected = selected if selected is not None else []
        self.__rows_per_page = 1

    @property
    def rows_per_page(self) -> int:
        """Get rows_per_page argument."""
        return self.__rows_per_page

    @rows_per_page.setter
    def rows_per_page(self, rows_per_page: int) -> None:
        """Set rows_per_page argument."""
        self.__rows_per_page = rows_per_page

    def validate(
        self,
        *,
        row_selection: int,
        dataframe_rows: int,
    ) -> None:
        """Validates if the arguments inserted are valid."""
        pre_selected_rows: int = len(self.__selected)

        if pre_selected_rows != 0:
            if pre_selected_rows > row_selection:
                raise TableInitialStateIncompatiblePreSelectedRowsError(
                    pre_selected_rows, row_selection
                )

            pre_selected_max_index: int = cast(int, max(self.__selected))

            if int(pre_selected_max_index) > dataframe_rows:
                raise TableInitialStateIncompatiblePreSelectedIndexError(
                    pre_selected_max_index, dataframe_rows
                )

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            "page": self.__page,
            "rowsPerPage": self.__rows_per_page,
            "searchText": self.__search_text,
            "selected": self.__selected,
            "expanded": [],
        }

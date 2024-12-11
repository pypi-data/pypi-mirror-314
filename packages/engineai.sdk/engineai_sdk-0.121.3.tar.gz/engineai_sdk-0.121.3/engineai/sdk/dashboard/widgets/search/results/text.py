"""Specs for Search Result Column Text."""

from typing import Any
from typing import Mapping
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.styling.color import Palette
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.widgets.chart_utils import column_is_of_type
from engineai.sdk.dashboard.widgets.search.exceptions import (
    SearchValidateNoValidDataTypeError,
)
from engineai.sdk.dashboard.widgets.search.results.base import BaseResultItem
from engineai.sdk.dashboard.widgets.search.results.styling.text import ResultTextStyling


class ResultTextItem(BaseResultItem):
    """Define text item for search results.

    Define a text item for search results, specifying the data column
    to display, whether it's searchable, and styling options.
    """

    def __init__(
        self,
        data_column: TemplatedStringItem,
        searchable: bool = True,
        styling: Optional[Union[Palette, ResultTextStyling]] = None,
    ) -> None:
        """Constructor for ResultTextItem.

        Args:
            data_column: Column name in pandas DataFrame used for
                search result.
            searchable: Flag that makes the result searchable.
            styling: Specs for Search Result styling.
        """
        super().__init__(
            data_column=data_column,
            styling=styling,
        )
        self.__searchable = searchable

    @property
    def searchable(self) -> bool:
        """Get search result searchable flag."""
        return self.__searchable

    def validate(self, *, data: pd.DataFrame) -> None:
        """Validate if data has the right columns.

        Args:
            data: pandas DataFrame where the data is present.

        Raises:
            SearchValidateNoDataColumnError: If data_column is not present in data.
            SearchValidateNoValidDataTypeError: If data_column is not a string.
        """
        super().validate(data=data)
        if not column_is_of_type(data[self._data_column], str):
            raise SearchValidateNoValidDataTypeError(
                self._data_column, self.__class__.__name__, "str"
            )

    def _build_extra_inputs(self) -> Mapping[str, Any]:
        """Method used to build extra fields."""
        return {"searchable": self.searchable}

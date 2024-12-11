"""Specs for Search Result Column Number."""

from typing import Any
from typing import Mapping
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.formatting import NumberFormatting
from engineai.sdk.dashboard.styling.color import Palette
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.widgets.chart_utils import column_is_of_type
from engineai.sdk.dashboard.widgets.search.exceptions import (
    SearchValidateNoValidDataTypeError,
)
from engineai.sdk.dashboard.widgets.search.results.base import BaseResultItem
from engineai.sdk.dashboard.widgets.search.results.styling.number import (
    ResultNumberStyling,
)


class ResultNumberItem(BaseResultItem):
    """Define number item for search results.

    Define a number item for search results, specifying the data column
    to display, formatting options, and styling options.
    """

    def __init__(
        self,
        data_column: TemplatedStringItem,
        formatting: Optional[NumberFormatting] = None,
        styling: Optional[Union[Palette, ResultNumberStyling]] = None,
    ) -> None:
        """Constructor for ResultNumberItem.

        Args:
            data_column: Column name in pandas DataFrame used for
                search result.
            formatting: formatting spec.
            styling: Specs for Search Result styling.

        Examples:
            ??? example "Create a minimal search widget with a result number item"
                ```py linenums="1"
                import pandas as pd
                from engineai.sdk.dashboard.dashboard import Dashboard
                from engineai.sdk.dashboard.widgets import search

                data = pd.DataFrame(
                    data=[
                        {"key": "AAPL", "name": "Apple", "score": 10},
                        {"key": "MSFT", "name": "Microsoft", "score": 5},
                    ]
                )

                search_widget = search.Search(
                    data=data,
                    items=[
                        search.ResultTextItem(data_column="key"),
                        search.ResultNumberItem(data_column="score"),
                    ],
                    selected_text_column="name",
                )

                Dashboard(content=search_widget)
                ```
        """
        super().__init__(
            data_column=data_column,
            styling=styling,
        )
        self.__formatting = formatting if formatting is not None else NumberFormatting()

    def validate(self, *, data: pd.DataFrame) -> None:
        """Validate if data has the right columns.

        Args:
            data: pandas DataFrame where the data is present.

        Raises:
            SearchValidateNoDataColumnError: If data_column is not present in data.
            SearchValidateNoValidDataTypeError: If data_column is not a number.
        """
        super().validate(data=data)
        if not column_is_of_type(data[self._data_column], (int, float)):
            raise SearchValidateNoValidDataTypeError(
                self._data_column, self.__class__.__name__, ("int", "float")
            )
        self.__formatting.validate(data)

    def _build_extra_inputs(self) -> Mapping[str, Any]:
        """Method used to build extra fields."""
        return {"formatting": self.__formatting.build()}

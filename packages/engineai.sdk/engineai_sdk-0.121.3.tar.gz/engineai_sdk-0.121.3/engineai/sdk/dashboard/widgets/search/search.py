"""Specs for Search Widget."""

import warnings
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Union
from typing import get_args

import pandas as pd

from engineai.sdk.dashboard.data.decorator import DataSource
from engineai.sdk.dashboard.data.http import Http
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.base import SelectableWidget
from engineai.sdk.dashboard.widgets.chart_utils import column_is_of_type
from engineai.sdk.dashboard.widgets.search.results.number import ResultNumberItem
from engineai.sdk.dashboard.widgets.search.results.text import ResultTextItem
from engineai.sdk.dashboard.widgets.search.results.typing import ResultItemType
from engineai.sdk.dashboard.widgets.utils import build_data

from .exceptions import SearchNoSearchableColumnError
from .exceptions import SearchValidateNoDataColumnError
from .exceptions import SearchValidateNoValidDataTypeError
from .results.build_result import build_search_result


class Search(SelectableWidget):
    """Construct search widget.

    Construct a search widget for searching through data, allowing
    customization of selected text column, widget ID, search items,
    and placeholder text.
    """

    _WIDGET_API_TYPE = "search"
    _DEPENDENCY_ID = "__SEARCH_DATA_DEPENDENCY__"
    _DEFAULT_HEIGHT = 0.6
    _FORCE_HEIGHT = True
    _FLUID_ROW_COMPATIBLE = True

    @type_check
    def __init__(
        self,
        *,
        data: Union[DataSource, pd.DataFrame, Http],
        selected_text_column: TemplatedStringItem,
        widget_id: Optional[str] = None,
        items: Optional[Union[TemplatedStringItem, List[ResultItemType]]] = None,
        placeholder: Optional[TemplatedStringItem] = None,
    ) -> None:
        """Constructor for Search widget.

        Args:
            data: data source for the widget.
            selected_text_column: Column with information to show
                when the option is selected.
            widget_id: widget ID.
            items: List of ResultItemTypes to be displayed in the search results.
            placeholder: Default text to show before searching.

        Examples:
            ??? example "Minimal Search Widget"
                ```py linenums="1"
                import pandas as pd
                from engineai.sdk.dashboard.dashboard import Dashboard
                from engineai.sdk.dashboard.widgets import search

                data = pd.DataFrame(
                    data=[
                        {"key": "AAPL", "name": "Apple"},
                        {"key": "MSFT", "name": "Microsoft"},
                    ]
                )

                # add_result_items allows info to be displayed in the drop-down list
                # when searching for an item
                search_widget = search.Search(
                    data=data,
                    selected_text_column="name",
                )
                Dashboard(content=search_widget)
                ```
        """
        super().__init__(widget_id=widget_id, data=data)
        self.__placeholder = placeholder
        self.__items = items
        self.__search_columns: List[ResultItemType] = []
        self.__has_searchable = False
        self.__selected_text_column = selected_text_column
        self._set_result_items(data=data)

    def add_result_items(self, *items: ResultItemType) -> "Search":
        """Add new search column(s), to be displayed in widget.

        Args:
            items: item(s) that will be added to the search
                columns list.
        """
        warnings.warn(
            "add_result_items is deprecated. Use `items` argument instead.",
            DeprecationWarning,
        )
        self.__search_columns = []
        self._set_searchable_items(items)
        self.__search_columns.extend(items)
        return self

    def validate(self, data: pd.DataFrame, **_: Any) -> None:
        """Validates Content Widget specs and its inner components.

        Args:
            data: reference to panda's DataFrame where data is present.
        """
        if not self.__has_searchable:
            raise SearchNoSearchableColumnError(
                self.widget_id,
                selected_text_column=str(self.__selected_text_column),
                has_items=bool(self.__items),
            )

        if (
            isinstance(self.__selected_text_column, str)
            and self.__selected_text_column not in data.columns
        ):
            raise SearchValidateNoDataColumnError(
                data_column=self.__selected_text_column
            )

        for result in self.__search_columns:
            result.validate(data=data)

    def _set_result_items(
        self,
        data: Union[DataSource, pd.DataFrame],
    ) -> None:
        if self.__items is None:
            self.__set_empty_items(data)
        elif isinstance(self.__items, Iterable) and isinstance(
            self.__items[0], get_args(ResultItemType)
        ):
            self._set_searchable_items(self.__items)
            self.__search_columns.extend(self.__items)
        else:
            result_item = self._extract_result_item(item=self.__items, data=data)
            self._set_searchable_items([result_item])
            self.__search_columns.append(result_item)

    def __set_empty_items(self, data: pd.DataFrame) -> None:
        result_item = self._extract_result_item(
            item=self.__selected_text_column, data=data
        )
        self._set_searchable_items([result_item])
        self.__search_columns.append(result_item)

    def _extract_result_item(
        self, item: TemplatedStringItem, data: Union[DataSource, pd.DataFrame]
    ) -> ResultItemType:
        self._validate_if_string_item_in_dataframe(item=item, data=data)

        result_item = None
        if isinstance(data, pd.DataFrame) and isinstance(item, str):
            if column_is_of_type(data[item], str):
                result_item = ResultTextItem(data_column=item)
            elif column_is_of_type(data[item], int):
                result_item = ResultNumberItem(data_column=item)
            else:
                raise SearchValidateNoValidDataTypeError(data_column=item)
        return result_item or ResultTextItem(data_column=item)

    @staticmethod
    def _validate_if_string_item_in_dataframe(
        item: TemplatedStringItem, data: Union[DataSource, pd.DataFrame]
    ) -> None:
        if (
            isinstance(data, pd.DataFrame)
            and isinstance(item, str)
            and item not in data.columns
        ):
            raise SearchValidateNoDataColumnError(data_column=item)

    def _set_searchable_items(self, items: Iterable[ResultItemType]) -> None:
        for item in items:
            if item in self.__search_columns:
                continue
            if (
                not self.__has_searchable
                and isinstance(item, ResultTextItem)
                and item.searchable
            ):
                self.__has_searchable = item.searchable

    def _build_widget_input(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "placeholder": build_templated_strings(items=self.__placeholder),
            "data": build_data(path=self.dependency_id),
            "selectedValueLabel": build_templated_strings(
                items=f"{{{{{self.__selected_text_column}}}}}"
            ),
            "results": {
                "columns": [
                    build_search_result(result) for result in self.__search_columns
                ],
            },
        }

"""Spec for Sankey connections."""

from typing import Any
from typing import Dict
from typing import Generic
from typing import Optional
from typing import TypeVar
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.data import DataSource
from engineai.sdk.dashboard.data.http import Http
from engineai.sdk.dashboard.data.manager.manager import DependencyManager
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.styling.color import Palette
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.charts.tooltip.item import (
    build_tooltip_item,
)
from engineai.sdk.dashboard.widgets.components.charts.typing import TooltipItems
from engineai.sdk.dashboard.widgets.sankey.exceptions import (
    SankeyItemsValidateNoDataColumnError,
)
from engineai.sdk.dashboard.widgets.utils import build_data
from engineai.sdk.dashboard.widgets.utils import get_tooltips

from .styling.connections import ConnectionsStyling

T = TypeVar("T", pd.DataFrame, Dict[str, pd.DataFrame])


class BaseConnections(Generic[T], DependencyManager):
    """Spec for Sankey connections."""

    _DEPENDENCY_ID = "__SANKEY_CONNECTIONS_DEPENDENCY__"
    _ID_COUNTER = 0

    @type_check
    def __init__(
        self,
        data: Union[DataSource, T, Http],
        *,
        from_column: TemplatedStringItem = "from",
        to_column: TemplatedStringItem = "to",
        data_column: TemplatedStringItem = "value",
        styling: Optional[Union[Palette, ConnectionsStyling]] = None,
        tooltips: Optional[TooltipItems] = None,
    ) -> None:
        """Construct spec for connections in Sankey widget.

        Args:
            from_column: name of column in pandas dataframe with
                id for source node. Id needs to match one of the ids provided in
                the node dataframe.
            to_column: name of column in pandas dataframe with
                id for destination node. Id needs to match one of the ids provided in
                the node dataframe.
            data_column: name of column in pandas dataframe
                with value for connection.
            data: data for
                the widget. Can be a pandas dataframe, a dictionary or Storage object
                if the data is to be retrieved from a storage.
            styling: styling spec.
            tooltips: list of tooltip items.
        """
        self.__data_id = self.__generate_id()
        super().__init__(data=data, base_path=self.__data_id)
        self._tooltip_items = get_tooltips(tooltips)
        self.__from_column = from_column
        self.__to_column = to_column
        self.__data_column = data_column
        self.__styling = (
            ConnectionsStyling(color_spec=styling)
            if isinstance(styling, Palette)
            else styling
            if styling
            else ConnectionsStyling()
        )

    @property
    def data_id(self) -> str:
        """Get data id."""
        return self.__data_id

    def __generate_id(self) -> str:
        self._increment_id_counter()
        return f"connections_data_{self._ID_COUNTER}"

    @classmethod
    def _increment_id_counter(cls) -> None:
        cls._ID_COUNTER = cls._ID_COUNTER + 1

    @property
    def tooltip_items(self) -> Any:
        """List[TooltipItem]: List of tooltip items."""
        return self._tooltip_items

    def validate(self, data: T, **_: object) -> None:  # type: ignore
        """Validates Sankey Series Connections widget spec.

        Args:
            data (pd.DataFrame, Dict[str, pd.DataFrame]): Data related to Connections

        Raises:
            SankeyItemsValidateNoDataColumnError: If from_column is not found
                in Data Columns
            SankeyItemsValidateNoDataColumnError: If to_column is not found
                in Data Columns
            SankeyItemsValidateNoDataColumnError: If data_column is not found
                in Data Columns
        """
        iterable = iter([data]) if isinstance(data, pd.DataFrame) else data.values()
        for value in iterable:
            if (
                isinstance(self.__from_column, str)
                and isinstance(value, pd.DataFrame)
                and self.__from_column not in value.columns
            ):
                raise SankeyItemsValidateNoDataColumnError(
                    missing_column_name="From column",
                    missing_column=self.__from_column,
                    item_name="Connection",
                )

            if (
                isinstance(self.__to_column, str)
                and isinstance(value, pd.DataFrame)
                and self.__to_column not in value.columns
            ):
                raise SankeyItemsValidateNoDataColumnError(
                    missing_column_name="To column",
                    missing_column=self.__to_column,
                    item_name="Connection",
                )

            if (
                isinstance(self.__data_column, str)
                and isinstance(value, pd.DataFrame)
                and self.__data_column not in value.columns
            ):
                raise SankeyItemsValidateNoDataColumnError(
                    missing_column_name="Value column",
                    missing_column=self.__data_column,
                    item_name="Connection",
                )

            self.__styling.validate(data=value)

    def build_tooltips(
        self,
    ) -> Optional[Dict[str, Any]]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return (
            {
                "fromIdKey": self.__from_column,
                "toIdKey": self.__to_column,
                "items": [
                    build_tooltip_item(item=item) for item in self._tooltip_items
                ],
                "data": build_data(path=self.dependency_id),
            }
            if len(self._tooltip_items) > 0
            else None
        )

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "fromNodeIdKey": build_templated_strings(items=self.__from_column),
            "toNodeIdKey": build_templated_strings(items=self.__to_column),
            "valueKey": build_templated_strings(items=self.__data_column),
            "styling": self.__styling.build(),
            "data": build_data(path=self.dependency_id),
        }

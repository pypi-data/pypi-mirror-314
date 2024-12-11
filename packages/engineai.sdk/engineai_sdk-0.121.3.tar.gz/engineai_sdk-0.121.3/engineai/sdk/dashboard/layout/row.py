"""Spec for a row in a dashboard vertical grid layout."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from typing_extensions import Unpack

from engineai.sdk.dashboard.abstract.layout import AbstractLayoutItem
from engineai.sdk.dashboard.abstract.typing import PrepareParams
from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.decorator import type_check

from .column import Column
from .exceptions import ElementHeightNotDefinedError
from .exceptions import RowColumnsAutoWidthError
from .exceptions import RowColumnsCustomWidthError
from .exceptions import RowColumnsMaximumWidthError
from .exceptions import RowMaximumAutoWidthItemsError
from .exceptions import RowMaximumItemsError
from .exceptions import RowMinimumItemsError
from .exceptions import RowsDifferentCustomHeightError
from .exceptions import RowsHeightsSetMultipleLevelsError
from .typings import LayoutItem


class Row(AbstractFactory):
    """Organize and group content horizontally within a vertical grid layout.

    The Row class represents a row within a vertical grid layout, allowing
    users to organize and group content horizontally.
    """

    @type_check
    def __init__(
        self,
        *items: Union[LayoutItem, Column],
        height: Optional[Union[int, float]] = None,
    ) -> None:
        """Constructor for Row.

        Args:
            *items: Content that is going to be added inside the Row,
                if the item is a Column, it will be added to the row, if the item
                is a Widget or a Grid, it will be added to a Column.
            height: Custom height for the row.

        Examples:
            ??? example "Create Row with widget"
                ```py linenums="1"
                import pandas as pd

                from engineai.sdk.dashboard import dashboard
                from engineai.sdk.dashboard import layout
                from engineai.sdk.dashboard.widgets import select

                data = pd.DataFrame({"id": [1, 2, 3]})

                dashboard.Dashboard(
                    content=layout.Grid(
                        layout.Row(select.Select(data))
                    )
                )
                ```

            ??? example "Create Row with multiple widgets"
                ```py linenums="1"
                import pandas as pd

                from engineai.sdk.dashboard import dashboard
                from engineai.sdk.dashboard import layout
                from engineai.sdk.dashboard.widgets import select
                from engineai.sdk.dashboard.widgets import toggle

                data = pd.DataFrame({"id": [1, 2, 3]})

                dashboard.Dashboard(
                    content=layout.Grid(
                        layout.Row(
                            select.Select(data),
                            toggle.Toggle(data),
                        )
                    )
                )
                ```

            ??? example "Create Row with Tab Section and Card"
                ```py linenums="1"
                import pandas as pd

                from engineai.sdk.dashboard import dashboard
                from engineai.sdk.dashboard import layout
                from engineai.sdk.dashboard.widgets import select
                from engineai.sdk.dashboard.widgets import toggle

                data = pd.DataFrame({"id": [1, 2, 3]})

                dashboard.Dashboard(
                    content=layout.Grid(
                        layout.Row(
                            layout.TabSection(
                                layout.Tab(
                                    label="tab",
                                    content=select.Select(data),
                                )
                            ),
                            layout.Card(
                                header=layout.Header(title="Card"),
                                content=toggle.Toggle(data),
                            ),
                        )
                    )
                )
                ```
        """
        super().__init__()
        self.__total_width: int = 0
        self.__auto_width: bool = True
        self.__columns: List[Column] = []
        self.__set_items(*items)
        self.__custom_height: Optional[Union[int, float]] = height
        self.__height: Optional[Union[int, float]] = None

    @property
    def custom_height(self) -> Optional[Union[int, float]]:
        """Get custom height."""
        return self.__custom_height

    def __set_items(self, *items: Union[LayoutItem, Column]) -> None:
        """Set columns for row."""
        if len(items) > 6:
            raise RowMaximumItemsError

        if len(items) == 0:
            raise RowMinimumItemsError

        for item in items:
            if isinstance(item, Column):
                self.__add_column(item)
            else:
                self.__add_column(Column(content=item))

    def __add_column(self, new_column: Column) -> None:
        """Add column to row."""
        self.__validate_new_column(new_column)
        self.__columns.append(new_column)

    def __validate_new_column(self, new_column: Column) -> None:
        self.__validate_auto_width(new_column)
        self.__validate_custom_width(new_column)

    def __validate_auto_width(self, new_column: Column) -> None:
        if new_column.width is None:
            if any(column.width is not None for column in self.__columns):
                raise RowColumnsAutoWidthError
            self.__total_width = 12

    def __validate_custom_width(self, new_column: Column) -> None:
        if new_column.width is not None:
            if any(column.width is None for column in self.__columns):
                raise RowColumnsCustomWidthError

            if self.__total_width + new_column.width > 12:
                raise RowColumnsMaximumWidthError(
                    overflow_width=self.__total_width + new_column.width,
                    total_width=self.__total_width,
                    new_width=new_column.width,
                )

            self.__total_width += new_column.width
            self.__auto_width = False

    def prepare_heights(
        self, column_height: Optional[Union[int, float]] = None
    ) -> None:
        """Prepare row heights."""
        self.__prepare_columns_heights(column_height)
        self.__resize_columns_height()
        self.__set_height(column_height)

    def __prepare_columns_heights(
        self, column_height: Optional[Union[int, float]] = None
    ) -> None:
        for column in self.__columns:
            row_height = column_height or self.__custom_height
            self.__validate_parent_and_inner_height(column, row_height)
            column.prepare_heights(row_height=row_height)

    @staticmethod
    def __validate_parent_and_inner_height(
        column: Column, row_height: Optional[Union[int, float]] = None
    ) -> None:
        if column.has_custom_heights and row_height:
            raise RowsHeightsSetMultipleLevelsError

    def __resize_columns_height(self) -> None:
        column_custom_height = self.__get_columns_custom_height()
        if column_custom_height:
            self.__resize_column_without_custom_heights(column_custom_height)
        else:
            self.__resize_columns_with_lower_height()

    def __get_columns_custom_height(self) -> Optional[float]:
        self.__validate_uniform_custom_heights()
        columns = [column for column in self.__columns if column.has_custom_heights]
        return columns[0].height if len(columns) > 0 else None

    def __validate_uniform_custom_heights(self) -> None:
        heights = [
            column.height for column in self.__columns if column.has_custom_heights
        ]
        if len(heights) > 0 and len(set(heights)) > 1:
            raise RowsDifferentCustomHeightError

    def __resize_column_without_custom_heights(self, row_height: float) -> None:
        for column in [
            column for column in self.__columns if not column.has_custom_heights
        ]:
            column.prepare_heights(row_height=row_height)

    def __resize_columns_with_lower_height(self) -> None:
        columns_heights = [column.height for column in self.__columns]
        if len(set(columns_heights)) > 1:
            for column in self.__columns:
                if column.height != max(columns_heights):
                    column.prepare_heights(row_height=max(columns_heights))

    def __set_height(self, column_height: Optional[Union[int, float]] = None) -> None:
        if self.__height is None:
            self.__height = self.__custom_height or max(
                column.height for column in self.__columns
            )
        elif column_height is not None:
            self.__height = column_height

    @property
    def height(self) -> float:
        """Get row height."""
        if self.__height is None:
            raise ElementHeightNotDefinedError
        return self.__height

    @property
    def has_custom_heights(self) -> bool:
        """Get if the Row has a custom height."""
        return self.__custom_height is not None

    def prepare(self, **kwargs: Unpack[PrepareParams]) -> None:
        """Prepare row."""
        if self.__auto_width and len(self.__columns) == 5:
            raise RowMaximumAutoWidthItemsError

        auto_width = int(12 / len(self.__columns)) if self.__auto_width else None

        for column in self.__columns:
            column.prepare(auto_width=auto_width, **kwargs)

    @property
    def force_height(self) -> bool:
        """Get if the Row has a forced height from the ."""
        return self.__columns[0].force_height if len(self.__columns) == 1 else False

    def items(self) -> List[AbstractLayoutItem]:
        """Returns list of grid items that need to be inserted individually."""
        items: List[AbstractLayoutItem] = []
        for column in self.__columns:
            items += column.items()
        return items

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "height": self.__height,
            "columns": [column.build() for column in self.__columns],
        }

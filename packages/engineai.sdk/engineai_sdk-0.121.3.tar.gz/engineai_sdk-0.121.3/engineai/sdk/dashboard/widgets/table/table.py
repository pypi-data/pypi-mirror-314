"""Spec for Table widget."""

import math
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Union

import pandas as pd
from pandas.api.types import is_datetime64_dtype
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_period_dtype

from engineai.sdk.dashboard.base import HEIGHT_ROUND_VALUE
from engineai.sdk.dashboard.data.decorator import DataSource
from engineai.sdk.dashboard.data.http import Http
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting.number import NumberFormatting
from engineai.sdk.dashboard.formatting.number import NumberScale
from engineai.sdk.dashboard.styling.color.default_specs import (
    PercentageAllNegativeSequentialColorGradient as AllNegative,
)
from engineai.sdk.dashboard.styling.color.default_specs import (
    PercentageAllPositiveSequentialColorGradient as AllPositive,
)
from engineai.sdk.dashboard.styling.color.default_specs import (
    PositiveNegativeDiscreteMap,
)
from engineai.sdk.dashboard.styling.color.default_specs import ScoreColorDiscreteMap
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.base import SelectableWidget
from engineai.sdk.dashboard.widgets.base import WidgetTitleType
from engineai.sdk.dashboard.widgets.pandas_utils import are_values_relative
from engineai.sdk.dashboard.widgets.pandas_utils import only_integers
from engineai.sdk.dashboard.widgets.pandas_utils import only_negative_or_positive_values
from engineai.sdk.dashboard.widgets.pandas_utils import only_negative_values
from engineai.sdk.dashboard.widgets.pandas_utils import only_positive_values
from engineai.sdk.dashboard.widgets.table.columns.items.datetime import DatetimeColumn
from engineai.sdk.dashboard.widgets.table.columns.items.number import NumberColumn
from engineai.sdk.dashboard.widgets.table.columns.items.text import TextColumn
from engineai.sdk.dashboard.widgets.table.columns.styling.arrow import ArrowStyling
from engineai.sdk.dashboard.widgets.table.columns.styling.cell import CellStyling
from engineai.sdk.dashboard.widgets.table.columns.styling.color_bar import (
    ColorBarStyling,
)
from engineai.sdk.dashboard.widgets.table.columns.styling.font import FontStyling
from engineai.sdk.dashboard.widgets.table.columns.styling.split_bar import (
    SplitBarStyling,
)
from engineai.sdk.dashboard.widgets.utils import build_data

from .columns.items.base import Column
from .exceptions import TableColumnsEmptyError
from .exceptions import TableDataWithoutColumnsError
from .exceptions import TableDuplicatedItemIdError
from .exceptions import TableNoColumnError
from .exceptions import TableValidateDataTypeError
from .group import Group
from .header import Header
from .header import TableColumns
from .initial_state import InitialState
from .styling import TableStyling


class Table(SelectableWidget):
    """Construct table widget.

    Construct a table widget with customizable parameters such as data source,
    columns, title, styling, row selection, pagination, search box, and more.
    """

    _DEPENDENCY_ID = "__TABLE_DATA_DEPENDENCY__"
    _WIDGET_API_TYPE = "tableGrid"

    _HEIGHT_TABLE_BODY_BORDER = 0.01
    _HEIGHT_TABLE_ROW = 0.30
    _HEIGHT_TABLE_HEADER_ROW = 0.31
    _HEIGHT_TABLE_FILTER_ROW = 0.325
    _HEIGHT_TABLE_SELECTOR = 0.46
    _HEIGHT_TABLE_TITLE = 0.38
    _HEIGHT_TABLE_TOP_MARGIN = 0.24
    _HEIGHT_TABLE_BOTTOM_MARGIN = 0.32

    _SCORE_MIN = -10
    _SCORE_MAX = 10
    _POSITIVE_SCORE_MIN = 0
    _POSITIVE_SCORE_MAX = 10
    _SCORE_CHANGE_MIN = -5
    _SCORE_CHANGE_MAX = 5

    _WINSORIZATION_LIMIT_LOWER = 0.05
    _WINSORIZATION_LIMIT_UPPER = 0.95
    _PERCENTAGE_LIMIT = 2

    @type_check
    def __init__(
        self,
        data: Union[DataSource, pd.DataFrame, Http],
        *,
        columns: Optional[TableColumns] = None,
        widget_id: Optional[str] = None,
        title: WidgetTitleType = None,
        styling: Optional[TableStyling] = None,
        row_selection: int = 1,
        rows_per_page: int = 10,
        initial_state: Optional[InitialState] = None,
        has_search_box: bool = False,
        has_filter_row: bool = False,
        has_header_filter: bool = False,
        group_columns: Optional[List[Group]] = None,
    ) -> None:
        """Constructor for Table widget.

        Args:
            data: data to be used by widget. Accepts DataSource as well as raw data.
            columns: header(s)/column(s) into the Table Widget. When this is of type
                string, it is assumed to be a text column.
            widget_id: unique widget id in a dashboard.
            title: title of widget can be either a string (fixed value) or determined
                by a value from another widget using a WidgetField.
            styling: styling of table widget.
            row_selection: number of rows that can be selected.
            rows_per_page: number of rows shown in each page.
            initial_state: initial state of table widget.
            has_search_box: show search box.
            has_filter_row: show filter row.
            has_header_filter: show header filter.
            group_columns: list of columns that should be grouped.

        Examples:
            ??? example "Create minimal Table widget"
                ```py linenums="1"
                import pandas as pd
                from engineai.sdk.dashboard.dashboard import Dashboard
                from engineai.sdk.dashboard.widgets import table
                data = pd.DataFrame(
                   {
                       "name": ["A", "B", "C"],
                       "value": [1, 2, 3],
                       "country": ["ES", "PT", "UK"],
                   },
                )
                Dashboard(content=table.Table(data))
                ```

            ??? example "Create Table widget with columns"
                ```py linenums="11"
                Dashboard(content=table.Table(data=data, columns="name"))
                ```
        """
        super().__init__(widget_id=widget_id, data=data)
        self.__items: List[Union[Header, Column]] = self.__generate_columns(
            data, columns
        )
        self.__styling = styling if styling else TableStyling()
        self.__row_selection = row_selection
        self.__initial_state = initial_state if initial_state else InitialState()
        self.__initial_state.rows_per_page = rows_per_page
        self.__has_search_box = has_search_box
        self.__has_filter_row = has_filter_row
        self.__has_header_filter = has_header_filter
        self.__group_columns = group_columns
        self.__title = title
        self._json_data = None

    @property
    def columns(self) -> List[Union[Header, Column]]:
        """Get columns of table widget."""
        return self.__items

    def validate(self, data: pd.DataFrame, **_: Any) -> None:
        """Validates widget spec."""
        self._validate_dataframe(data=data)
        self._validate_group_columns(data=data)

    def _validate_group_columns(
        self,
        *,
        data: pd.DataFrame,
    ) -> None:
        if self.__group_columns is not None:
            for group_column in self.__group_columns:
                group_column.validate(data=data)

    def _validate_dataframe(self, *, data: pd.DataFrame) -> None:
        if not isinstance(data, pd.DataFrame):
            raise TableValidateDataTypeError(_type=type(data))
        self.__initial_state.validate(
            row_selection=self.__row_selection, dataframe_rows=len(data)
        )
        for item in self.__items:
            item.validate(data=data)

    def _prepare(self, **kwargs: object) -> None:
        """Prepare widget for rendering."""
        validated_item_ids: Set[str] = set()
        if len(self.__items) > 0:
            for item in self.__items:
                if item.item_id in validated_item_ids:
                    raise TableDuplicatedItemIdError(
                        self.widget_id, item_ids=item.item_id
                    )
                validated_item_ids.add(item.item_id)
                if isinstance(item, Header):
                    validated_item_ids.update(
                        item.validate_item_ids(
                            widget_id=self.widget_id,
                            previous_level_item_id=validated_item_ids,
                        )
                    )
                item.prepare()

        self._json_data = kwargs.get("json_data")

    def __generate_columns(
        self,
        data: Union[DataSource, pd.DataFrame, Http],
        columns: Optional[TableColumns],
    ) -> List[Union[Header, Column]]:
        if isinstance(data, Http) and columns is None:
            raise TableNoColumnError
        self.__validate_columns(data=data, columns=columns)
        if self.__can_set_columns_from_data(data, columns):
            return self.__get_columns_from_data(data=data)
        return self.__generate_columns_from_argument(columns=columns)

    @staticmethod
    def __validate_columns(
        data: Union[DataSource, pd.DataFrame],
        columns: Optional[TableColumns],
    ) -> None:
        if isinstance(data, DataSource) and (columns is None or len(columns) == 0):
            raise TableNoColumnError

    @staticmethod
    def __can_set_columns_from_data(
        data: Union[DataSource, pd.DataFrame], columns: Optional[TableColumns]
    ) -> bool:
        return columns is None and isinstance(data, pd.DataFrame)

    def __get_columns_from_data(
        self, data: Union[DataSource, pd.DataFrame]
    ) -> List[Union[Header, Column]]:
        if len(data.columns) == 0:
            raise TableDataWithoutColumnsError
        return self.__get_columns(data=data)

    def __get_columns(
        self,
        data: pd.DataFrame,
    ) -> List[Union[Header, Column]]:
        items: List[Union[Header, Column]] = []
        for column in data.columns:
            if self._is_numeric_and_relative(data, column):
                items.append(
                    NumberColumn(
                        data_column=column,
                        formatting=NumberFormatting(scale=NumberScale.DYNAMIC_RELATIVE),
                        styling=(
                            ArrowStyling()
                            if not only_negative_or_positive_values(data[column])
                            else (
                                ColorBarStyling(
                                    min_value=0,
                                    max_value=1,
                                    color_spec=AllPositive(),
                                )
                                if only_positive_values(data[column])
                                else (
                                    ColorBarStyling(
                                        min_value=0,
                                        max_value=-1,
                                        color_spec=AllNegative(),
                                    )
                                    if only_negative_values(data[column])
                                    else None
                                )
                            )
                        ),
                    )
                )
            elif is_numeric_dtype(data[column]):
                items.append(
                    NumberColumn(
                        data_column=column,
                        formatting=(
                            NumberFormatting(decimals=0)
                            if only_integers(data[column])
                            else None
                        ),
                        styling=(
                            CellStyling(color_spec=ScoreColorDiscreteMap())
                            if self._has_positive_score_values(data[column])
                            else (
                                SplitBarStyling()
                                if self._has_score_change_values(data[column])
                                else (
                                    CellStyling(
                                        color_spec=PositiveNegativeDiscreteMap()
                                    )
                                    if self._has_score_values(data[column])
                                    else (
                                        FontStyling(
                                            color_spec=PositiveNegativeDiscreteMap()
                                        )
                                        if self.__has_positive_and_negative_value(
                                            data[column]
                                        )
                                        else None
                                    )
                                )
                            )
                        ),
                    )
                )
            elif is_datetime64_dtype(data[column]) or is_period_dtype(data[column]):
                items.append(DatetimeColumn(data_column=column))
            else:
                items.append(TextColumn(data_column=column))
        return items

    def _is_numeric_and_relative(
        self, data: pd.DataFrame, column: pd.DataFrame
    ) -> bool:
        # TODO: this method should be removed when removing default styling
        try:
            non_na_column = data[column].dropna()
            return is_numeric_dtype(non_na_column) and are_values_relative(
                non_na_column,
                self._WINSORIZATION_LIMIT_UPPER,
                self._WINSORIZATION_LIMIT_LOWER,
                self._PERCENTAGE_LIMIT,
            )
        except Exception:  # noqa: BLE001
            return False

    def _has_positive_score_values(self, column: pd.DataFrame) -> bool:
        non_na_column = column.dropna()
        return bool(
            (
                non_na_column.ge(self._POSITIVE_SCORE_MIN)
                & non_na_column.le(self._POSITIVE_SCORE_MAX)
            ).all()
        )

    def _has_score_change_values(self, column: pd.DataFrame) -> bool:
        scores = column.ge(self._SCORE_MIN) & column.le(self._SCORE_MAX)
        score_changes = column.ge(self._SCORE_CHANGE_MIN) & column.le(
            self._SCORE_CHANGE_MAX
        )
        if (
            scores.all() and score_changes.all()
        ):  # ambiguous result, check now if all within score change range
            return score_changes.all()
        return False

    def __has_positive_and_negative_value(self, data: pd.Series) -> bool:
        return (data > 0).any() and (data < 0).any()

    def _has_score_values(self, column: pd.DataFrame) -> bool:
        return (column.ge(self._SCORE_MIN) & column.le(self._SCORE_MAX)).all()

    @staticmethod
    def __generate_columns_from_argument(
        columns: Optional[TableColumns],
    ) -> List[Union[Header, Column]]:
        items: List[Union[Header, Column]] = []

        if isinstance(columns, str):
            items.append(TextColumn(data_column=columns))
        elif isinstance(columns, List):
            if len(columns) == 0:
                raise TableColumnsEmptyError
            for item in columns:
                if isinstance(item, str):
                    items.append(TextColumn(data_column=item))
                else:
                    items.append(item)
        else:
            items.append(columns)
        return items

    @property
    def height(self) -> float:
        """Calculates the automatic height for Table widget."""
        height = (
            self._generate_rows_height()
            + self._generate_headers_height()
            + self._generate_extra_height()
        )

        return round(
            int(math.ceil(height / self._WIDGET_HEIGHT_STEP))
            * self._WIDGET_HEIGHT_STEP,
            HEIGHT_ROUND_VALUE,
        )

    def _generate_rows_height(self) -> float:
        if self.__initial_state.rows_per_page > 2:
            height: float = (
                self._HEIGHT_TABLE_ROW * (self.__initial_state.rows_per_page - 2)
                + 2 * 0.295
            )
        else:
            height = self.__initial_state.rows_per_page * self._HEIGHT_TABLE_ROW

        height += self._HEIGHT_TABLE_BODY_BORDER * 2

        return height

    def _generate_headers_height(self) -> float:
        headers_len = max(
            (item.depth for item in self.__items),
            default=1,
        )
        height = (
            headers_len * self._HEIGHT_TABLE_HEADER_ROW + self._HEIGHT_TABLE_BODY_BORDER
        )
        height += self._HEIGHT_TABLE_FILTER_ROW if self.__has_filter_row is True else 0

        return height

    def _generate_extra_height(self) -> float:
        height = self._HEIGHT_TABLE_TITLE if self.__title is not None else 0

        height += (
            self._HEIGHT_TABLE_SELECTOR
            + self._HEIGHT_TABLE_TOP_MARGIN
            + self._HEIGHT_TABLE_BOTTOM_MARGIN
        )

        return height

    def _get_items_specs(self) -> List[Any]:
        items_spec = []
        for item in self.__items:
            if isinstance(item, Header):
                items_spec.append({"header": item.build()})
            else:
                items_spec.append({"column": item.build()})
        return items_spec

    def _build_widget_input(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            "title": build_templated_strings(items=self.__title),
            "hasSearchBox": self.__has_search_box,
            "hasFilterRow": self.__has_filter_row,
            "hasHeaderFilter": self.__has_header_filter,
            "rowSelection": self.__row_selection,
            "columns": self._get_items_specs(),
            "defaultState": self.__initial_state.build(),
            "data": build_data(path=self.dependency_id, json_data=self._json_data),
            "styling": self.__styling.build(),
            "groupColumns": (
                [group_column.build() for group_column in self.__group_columns]
                if self.__group_columns is not None
                else None
            ),
        }

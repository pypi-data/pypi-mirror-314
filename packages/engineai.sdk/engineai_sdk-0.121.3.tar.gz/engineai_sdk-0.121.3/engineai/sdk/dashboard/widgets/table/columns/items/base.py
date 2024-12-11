"""Base spec shared by all column types."""

from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.links.abstract import AbstractFactoryLinkItemsHandler
from engineai.sdk.dashboard.links.typing import GenericLink
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.table.columns.items.exceptions import (
    TableColumnDataColumnNotFoundError,
)
from engineai.sdk.dashboard.widgets.table.columns.items.exceptions import (
    TableColumnMissingLabelError,
)


class Column(AbstractFactoryLinkItemsHandler):
    """Base spec for columns in a Table widget."""

    _ITEM_ID_TYPE: Optional[str] = None

    @type_check
    def __init__(
        self,
        *,
        data_column: Union[str, WidgetField],
        label: Optional[Union[str, GenericLink]] = None,
        hiding_priority: int = 0,
        tooltip_text: Optional[List[TemplatedStringItem]] = None,
        min_width: Optional[int] = None,
        optional: bool = False,
    ) -> None:
        """Base spec for columns in a Table widget.

        Args:
            data_column: name of column in pandas dataframe(s) used to fill this
                column.
            label: label to be displayed for this column.
            hiding_priority: columns with lower hiding_priority are hidden first
                if not all data can be shown.
            tooltip_text: info text to explain column. Each element of list is
                displayed as a separate paragraph.
            min_width: min width of the column in pixels.
            optional: flag to make the column optional if there is no Data for that
                columns.
        """
        super().__init__()
        self._data_column = data_column
        self.__label = self._set_label(label=label, data_column=data_column)
        self.__hiding_priority = hiding_priority
        self.__tooltip_text = tooltip_text or []
        self.__min_width = min_width
        self.depth: int = 1
        self.__item_id: str = f"{self._item_id_type}_" + (
            data_column.item_id
            if isinstance(data_column, WidgetField)
            else str(data_column)
        )
        self._optional = optional

    @property
    def _item_id_type(self) -> str:
        if self._ITEM_ID_TYPE is None:
            msg = f"Class {self.__class__.__name__}.ITEM_API_TYPE not defined."
            raise NotImplementedError(msg)
        return self._ITEM_ID_TYPE

    @property
    def item_id(self) -> str:
        """Return Item ID."""
        return self.__item_id

    def set_item_id(self, item_id: str) -> None:
        """Set item_id.

        Args:
            item_id: parent item_id.
        """
        self.__item_id = f"{item_id}__{self.__item_id}"

    @property
    def tooltip_text(self) -> List[TemplatedStringItem]:
        """Return Tooltip Text."""
        return self.__tooltip_text

    @tooltip_text.setter
    def tooltip_text(self, tooltip_text: List[TemplatedStringItem]) -> None:
        """Set Tooltip Text."""
        self.__tooltip_text = tooltip_text

    def _set_label(
        self,
        label: Optional[Union[str, GenericLink]],
        data_column: TemplatedStringItem,
    ) -> Union[str, GenericLink]:
        if label is not None:
            return label
        if isinstance(data_column, str):
            return data_column.replace("_", " ").title()
        raise TableColumnMissingLabelError(class_name=self.__class__.__name__)

    def prepare(self) -> None:
        """Prepare class."""

    def validate(self, *, data: pd.DataFrame) -> None:
        """Validate if dataframe that will be used for column contains required columns.

        Args:
            data: pandas dataframe which will be used for table
        """
        if not self._optional:
            self._validate_data_column(
                data=data, column=str(self._data_column), column_name="data_column"
            )
        self._custom_validation(data=data)

    def _validate_data_column(
        self, *, data: pd.DataFrame, column: Union[str, WidgetField], column_name: str
    ) -> None:
        if isinstance(column, str) and column not in data.columns:
            raise TableColumnDataColumnNotFoundError(
                column_name=column_name,
                column_value=column,
            )

    @abstractmethod
    def _custom_validation(self, *, data: pd.DataFrame) -> None:
        """Custom validation for each columns to implement.

        Args:
            data: pandas dataframe which will be used for table.
        """

    @property
    def data_column(self) -> TemplatedStringItem:
        """Name of column used in pandas dataframe.

        Returns:
            str: data column
        """
        return self._data_column

    @property
    def label(self) -> Union[str, GenericLink]:
        """Label used for column.

        Returns:
            str: column label
        """
        return self.__label

    @abstractmethod
    def _build_column(self) -> Dict[str, Any]:
        """Build Column input."""

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            "dataKey": build_templated_strings(items=self._data_column),
            "columnId": self.item_id,
            "label": build_templated_strings(items=self.__label),
            "fixed": False,
            "tooltipText": [
                build_templated_strings(items=tooltip)
                for tooltip in self.__tooltip_text
            ],
            "hidingPriority": self.__hiding_priority,
            "minWidth": self.__min_width,
            "columnType": self._build_column(),
        }

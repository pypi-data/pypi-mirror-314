"""Spec for Table group column."""

from typing import Any
from typing import Dict
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.links.abstract import AbstractFactoryLinkItemsHandler
from engineai.sdk.dashboard.templated_string import build_templated_strings

from .exceptions import TableGroupColumnKeyNotFoundError


class Group(AbstractFactoryLinkItemsHandler):
    """Define group column for table widget.

    Define a group column for the table widget,
    which allows grouping rows based on specified columns.
    """

    @type_check
    def __init__(
        self,
        data_column: Union[str, WidgetField],
        label: Union[str, WidgetField],
    ) -> None:
        """Constructor for Group.

        Args:
            data_column: column that will be used to group the table rows.
            label: table group label.
        """
        super().__init__()
        self.__data_column = data_column
        self.__label = label

    def validate(self, data: pd.DataFrame) -> None:
        """Validates column key.

        Args:
            data: pandas DataFrame or dict where the data is present.
        """
        if (
            isinstance(self.__data_column, str)
            and self.__data_column not in data.columns
        ):
            raise TableGroupColumnKeyNotFoundError(data_column=self.__data_column)

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            "columnKey": build_templated_strings(items=self.__data_column),
            "label": build_templated_strings(items=self.__label),
        }

"""Specs for NumericCondition."""

import enum
from typing import Any
from typing import Dict
from typing import Union

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings

from .base import BaseOperation


class NumericConditionOperator(enum.Enum):
    """Alignment keys."""

    GREATER = "GREATER"
    GREATER_OR_EQUAL = "GREATER_OR_EQUAL"
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS = "LESS"
    LESS_OR_EQUAL = "LESS_OR_EQUAL"


class NumericCondition(BaseOperation):
    """Specs for NumericCondition."""

    _ITEM_ID = "numericCondition"

    @type_check
    def __init__(
        self,
        *,
        data_column: TemplatedStringItem,
        operator: NumericConditionOperator,
        scalar: Union[int, float],
    ) -> None:
        """Construct for NumericCondition class.

        Args:
            data_column: column in dataframe to use in comparison.
            operator: comparison operator.
            scalar: number to compare against values in value_column.
        """
        super().__init__()
        self.__operator = operator.value
        self.__data_column = data_column
        self.__scalar = scalar

    def build_filter(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "operator": self.__operator,
            "valueKey": build_templated_strings(items=self.__data_column),
            "scalar": self.__scalar,
        }

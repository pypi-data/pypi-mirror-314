"""Specs for Select Widget Group."""

from typing import Any
from typing import Dict

import pandas as pd

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings

from .exceptions import SelectValidateValueError


class Group(AbstractFactory):
    """Constructor for Select Widget Group spec."""

    def __init__(
        self,
        group_column: TemplatedStringItem,
        show_group_when_selected: bool = False,
    ) -> None:
        """Spec for Select Group.

        Args:
            group_column: name of column in pandas dataframe(s) used to define the
                entries groups.
            show_group_when_selected: flag will append the group name into entry
                label.
        """
        self.__group_column = group_column
        self.__show_group_when_selected = show_group_when_selected

    def validate(self, data: pd.DataFrame) -> None:
        """Validates Group spec.

        Args:
            data (DataFrame): data that will be used in the validation.
        """
        if self.__group_column not in data.columns:
            raise SelectValidateValueError(
                argument="group_column",
                value=str(self.__group_column),
            )

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "groupKey": build_templated_strings(items=self.__group_column),
            "showGroupOnSelection": self.__show_group_when_selected,
        }

"""Select Widget Exceptions."""

from typing import List

from engineai.sdk.dashboard.exceptions import BaseDataValidationError
from engineai.sdk.dashboard.widgets.exceptions import DashboardWidgetError


class SelectWidgetError(DashboardWidgetError):
    """Select Widget Base Exception."""

    CLASS_NAME = "Select"


class SelectValidateValueError(BaseDataValidationError):
    """Select Validate Value not found Error."""

    def __init__(self, argument: str, value: str) -> None:
        """Constructor for SelectValidateValueError class.

        Args:
            argument: Select widget column name argument.
            value: Select widget argument value.
        """
        super().__init__(f"Missing {argument}='{value}' on provided data.")


class SelectValidateUniqueIDError(BaseDataValidationError):
    """Select Validate Unique ID Error."""

    def __init__(self, unique_ids: int, nr_rows: int) -> None:
        """Constructor for SelectValidateUniqueIDError class.

        Args:
            unique_ids: Select widget unique ids length.
            nr_rows: Number of rows present in Select widget data.
        """
        super().__init__(
            f"IDs must be unique. The number of Unique IDs: {unique_ids} != number of "
            f"rows in data: {nr_rows}, on provided data."
        )


class SelectValidateDifferentGroupsError(BaseDataValidationError):
    """Select Validate Different Groups Error."""

    def __init__(
        self,
        select_widget_groups: List[str],
        groups: List[str],
    ) -> None:
        """Constructor for SelectValidateDifferentGroupsError class."""
        super().__init__(
            f"Inserted groups are different: {select_widget_groups=} , {groups=}. "
            "Make sure that both match."
        )


class CategoryGroupColumnNotFoundError(BaseDataValidationError):
    """Category Group Column Not Found."""

    def __init__(
        self,
        column_name: str,
        column_value: str,
    ) -> None:
        """Constructor for CategoryGroupColumnNotFoundError class."""
        super().__init__(f"Groups missing {column_name}='{column_value}'.")

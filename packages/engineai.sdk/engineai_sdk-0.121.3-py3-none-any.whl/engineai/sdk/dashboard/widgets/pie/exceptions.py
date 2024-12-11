"""Pie Widget Exceptions."""

from engineai.sdk.dashboard.exceptions import BaseDataValidationError
from engineai.sdk.dashboard.widgets.exceptions import DashboardWidgetError


class PieError(DashboardWidgetError):
    """Pie Widget Base Exception."""

    CLASS_NAME = "Pie"


class PieValidateValueError(BaseDataValidationError):
    """Pie Widget Validate Value Error."""

    def __init__(
        self,
        subclass: str,
        argument: str,
        value: str,
    ) -> None:
        """Constructor for PieValidateValueError class.

        Args:
            subclass: Pie widget secondary class.
            argument: Pie widget argument.
            value: Pie widget value.
        """
        super().__init__(
            f"Missing {subclass} {argument}='{value}' on provided data, for item with "
            f"{value=}."
        )

"""Chart Tooltips Exceptions."""

from engineai.sdk.dashboard.exceptions import BaseDataValidationError
from engineai.sdk.dashboard.templated_string import TemplatedStringItem


class TooltipItemColumnNotFoundError(BaseDataValidationError):
    """Tooltip Item Column Not Found Error."""

    def __init__(
        self,
        class_name: str,
        column_name: str,
        column_value: TemplatedStringItem,
    ) -> None:
        """Construct for TooltipItemColumnNotFoundError class."""
        super().__init__(
            f"{class_name}: Column {column_name}='{column_value}' not found in Data."
        )

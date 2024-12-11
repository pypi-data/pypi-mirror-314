"""Items Styling Exceptions."""

from engineai.sdk.dashboard.exceptions import BaseDataValidationError


class ItemStylingValidationError(BaseDataValidationError):
    """Items Styling Validation Error."""

    def __init__(
        self,
        class_name: str,
        column_name: str,
        column_value: str,
    ) -> None:
        """Constructor for ItemStylingValidationError class."""
        super().__init__(
            f"No data found for {column_name}='{column_value}' used in {class_name}."
        )


class StylingInvalidDashValuesError(BaseDataValidationError):
    """Items Styling Invalid Dash Values Error."""

    def __init__(self, class_name: str, column_name: str, column_value: str) -> None:
        """Constructor for StylingInvalidDashValuesError class."""
        super().__init__(
            f"{class_name} dash values in {column_name}='{column_value}' are "
            f"not correctly defined, please use DashStyle enum values."
        )

"""Content Widget Exceptions."""

from engineai.sdk.dashboard.exceptions import BaseDataValidationError
from engineai.sdk.dashboard.widgets.exceptions import DashboardWidgetError


class ContentNoItemsError(DashboardWidgetError):
    """Content Widget No Items Error."""

    CLASS_NAME = "Content"

    def __init__(self, widget_id: str, *args: object) -> None:
        """Constructor for ContentNoItemsError class.

        Args:
            widget_id (str): Content widget id.
        """
        super().__init__(widget_id, *args)
        self.error_strings.append(
            "No items associated. "
            "Use `add_items` method to add items (content.MarkdownItem, for example)."
        )


class ContentItemNoValueError(BaseDataValidationError):
    """Content Widget No Items Error."""

    def __init__(
        self,
        data_key: str,
        data_key_value: str,
        class_name: str,
    ) -> None:
        """Constructor for ContentNoItemsError class.

        Args:
            data_key (str): Content Item data key.
            data_key_value (str): Content Item data key value.
            class_name (str): Content Item class name.
        """
        super().__init__(f"Missing {class_name} {data_key}='{data_key_value}' in Data.")

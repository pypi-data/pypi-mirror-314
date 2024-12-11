"""Actions Exceptions."""

from typing import Optional

from engineai.sdk.dashboard.widgets.exceptions import DashboardWidgetError


class ActionsError(DashboardWidgetError):
    """Actions Base Exception."""

    def __init__(self, class_name: str, *args: object) -> None:
        """Constructor for TreeMap Widget Base Exception.

        Args:
            class_name (str): Class that calls the Actions.
        """
        self.CLASS_NAME = class_name
        super().__init__(
            class_name,
            *args,
        )


class ActionLinkMissingColumnError(ActionsError):
    """Cartesian Widget Validate No Data Error."""

    def __init__(
        self,
        column_name: str,
        column_value: str,
        class_name: str,
        key: Optional[str],
    ) -> None:
        """Constructor for CartesianValidateSeriesDataColumnNotFound class.

        Args:
            column_name (str): data column name.
            column_value (str): data column value.
            class_name (str): Cartesian series class name.
            key (Optional[str]): Key associated to data in case the data is a dictionary
                node (used in Tree widgets).
        """
        super().__init__(class_name=class_name)
        node_key_error = f" on node with {key=}," if key is not None else ""
        self.error_strings.append(
            f"Action Link {column_name}='{column_value}' "
            f"not found{node_key_error} on provided data."
        )

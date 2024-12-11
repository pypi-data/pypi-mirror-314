"""Specs for Errors DatastoreDependency."""

from engineai.sdk.dashboard.exceptions import EngineAIDashboardError


class OrderByDuplicatedColumnsError(EngineAIDashboardError):
    """Order By Duplicated Columns Error."""

    def __init__(self, *args: object) -> None:
        """Constructor for OrderByDuplicatedColumnsError class."""
        super().__init__(*args)
        self.error_strings.append(
            "OrderByItem's `order_column` must be unique. Make sure that "
            "all `order_column` are unique."
        )

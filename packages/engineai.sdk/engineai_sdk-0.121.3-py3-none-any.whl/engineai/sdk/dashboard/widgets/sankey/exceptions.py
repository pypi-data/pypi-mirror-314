"""Sankey Exceptions."""

from typing import List
from typing import Optional

from engineai.sdk.dashboard.exceptions import BaseDataValidationError
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.widgets.exceptions import DashboardWidgetError


class SankeyError(DashboardWidgetError):
    """Sankey Base Exception."""

    CLASS_NAME = "Sankey"


class SankeyItemsValidateNoDataColumnError(BaseDataValidationError):
    """Sankey Widgets Validate No DataColumn Error."""

    def __init__(
        self,
        missing_column_name: str,
        missing_column: TemplatedStringItem,
        item_name: str,
        style: bool = False,
    ) -> None:
        """Constructor for SankeyItemsValidateNoDataColumnError class.

        Args:
            missing_column_name: Missing column name
            missing_column: Missing column value
            item_name: Sankey object name (Node, Connection, Frame, etc.).
            style: connection or node styling.
        """
        message = (
            f"{missing_column_name} {missing_column} not found in Data."
            if not style
            else f"{missing_column_name} {missing_column} not found in Data"
            f", for the Sankey {item_name} Style."
        )
        super().__init__(message)


class SankeyDataColumnMissingError(SankeyError):
    """Sankey Widgets Validate No Data Column Error."""

    def __init__(
        self,
        widget_id: Optional[str],
        color_specs: List[str],
        *args: object,
    ) -> None:
        """Constructor for SankeyDataColumnMissingError class.

        Args:
            widget_id: Sankey widget id.
            color_specs: Missing Sankey object name
                (Nodes, Connections, Frames, etc.).
        """
        super().__init__(widget_id, color_specs, *args)
        self.error_strings.append(
            "data_column argument cannot be None if color_spec is "
            f"{' or '.join(color_specs)}"
        )


class SankeyNodesAndConnectionsWrongArgumentsError(SankeyError):
    """Sankey Widgets Validate No Data Column Error."""

    def __init__(
        self,
        nodes_args: List[str],
        connections_args: List[str],
        *args: object,
    ) -> None:
        """Constructor for SankeyNodesAndConnectionsWrongArgumentsError class.

        Args:
            nodes_args: Sankey's Nodes arguments.
            connections_args: Sankey's Connections arguments.
        """
        super().__init__(None, nodes_args, connections_args, *args)
        self.error_strings.append(
            f"Sankey's Nodes and Connections data are mismatched (Nodes: {nodes_args}, "
            f"Connections: {connections_args}). Please make sure that both use the "
            "same arguments."
        )

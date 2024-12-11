"""Spec for Base Sankey widget."""

from typing import Any
from typing import Dict
from typing import Mapping
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting import NumberFormatting
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.base import Widget
from engineai.sdk.dashboard.widgets.base import WidgetTitleType

from .exceptions import SankeyNodesAndConnectionsWrongArgumentsError
from .series.connections import BaseConnections
from .series.nodes import BaseNodes
from .series.series import Series


class BaseSankey(Widget):
    """Spec for Base Sankey widget."""

    _WIDGET_API_TYPE = "sankey"
    _DEPENDENCY_ID = "__SANKEY_DEPENDENCY__"

    @type_check
    def __init__(
        self,
        *,
        series_name: str,
        nodes: BaseNodes[Any],
        connections: BaseConnections[Any],
        widget_id: Optional[str] = None,
        formatting: Optional[NumberFormatting] = None,
        title: WidgetTitleType = "",
    ) -> None:
        """Construct spec for base Sankey widget.

        Args:
            series_name: name shown next to values in nodes
                and connections.
            nodes: spec for nodes.
            connections: spec for connections.
            widget_id: unique widget id in a dashboard.
            formatting: formatting spec for value
                associated with nodes and connections.
            title: title of widget can be either a
                string (fixed value) or determined by a value from another widget
                using a WidgetLink.
        """
        super().__init__(widget_id=widget_id, data=None)
        self._series = Series(
            name=series_name,
            nodes=nodes,
            connections=connections,
            formatting=formatting,
        )
        self._title = title

    def validate(self, _: Union[pd.DataFrame, Dict[str, Any]], **__: object) -> None:
        """Validate data for Sankey widget."""
        return

    def _prepare(self, **_: object) -> None:
        """Method for each Widget prepare before building."""
        for nodes, connections in zip(
            self._series.nodes.data_sources, self._series.connections.data_sources
        ):
            if (
                len(nodes.func_args) != len(connections.func_args)
                or nodes.args != connections.args
            ):
                raise SankeyNodesAndConnectionsWrongArgumentsError(
                    nodes.func_args,
                    connections.func_args,
                )

    def _build_playback(self) -> Mapping[str, Any]:
        return {}

    def _build_widget_input(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            "chart": {
                "series": self._series.build(),
                "nodeTooltip": self._series.nodes.build_tooltips(),
                "connectionTooltip": self._series.connections.build_tooltips(),
            },
            **self._build_playback(),
            "title": build_templated_strings(
                items=self._title,
            ),
        }

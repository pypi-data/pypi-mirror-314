"""Spec for Sankey widget."""

from typing import Optional

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting import NumberFormatting
from engineai.sdk.dashboard.widgets.base import WidgetTitleType

from .base import BaseSankey
from .series.connections import BaseConnections
from .series.nodes import BaseNodes

Nodes = BaseNodes[pd.DataFrame]
Connections = BaseConnections[pd.DataFrame]


class Sankey(BaseSankey):
    """Spec for Sankey widget."""

    @type_check
    def __init__(
        self,
        *,
        series_name: str = "series",
        nodes: Nodes,
        connections: Connections,
        widget_id: Optional[str] = None,
        formatting: Optional[NumberFormatting] = None,
        title: WidgetTitleType = "",
    ) -> None:
        """Construct spec for Sankey widget.

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

        Examples:
            ??? example "Create a minimal Sankey widget"
                ```py linenums="1"
                    import pandas as pd
                    from engineai.sdk.dashboard.dashboard import Dashboard
                    from engineai.sdk.dashboard.widgets import sankey

                    nodes = pd.DataFrame({"id": ["company", "imports", "exports"]})
                    connections = pd.DataFrame(
                        {
                            "from": ["company", "company"],
                            "to": ["imports", "exports"],
                            "value": [0.76, 0.24],
                        }
                    )
                    sankey_widget = sankey.Sankey(
                        nodes=sankey.Nodes(
                            data=nodes,
                        ),
                        connections=sankey.Connections(
                            data=connections,
                        ),
                    )
                    Dashboard(content=sankey_widget)
                ```
        """
        super().__init__(
            series_name=series_name,
            nodes=nodes,
            connections=connections,
            widget_id=widget_id,
            formatting=formatting,
            title=title,
        )

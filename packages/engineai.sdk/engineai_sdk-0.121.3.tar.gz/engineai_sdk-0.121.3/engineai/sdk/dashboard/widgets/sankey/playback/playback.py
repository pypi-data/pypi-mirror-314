"""Spec for Sankey Playback widget."""

from typing import Any
from typing import Dict
from typing import Mapping
from typing import Optional

import pandas as pd

from engineai.sdk.dashboard.formatting import NumberFormatting
from engineai.sdk.dashboard.widgets.base import WidgetTitleType
from engineai.sdk.dashboard.widgets.components.playback import Playback
from engineai.sdk.dashboard.widgets.sankey.series.connections import BaseConnections
from engineai.sdk.dashboard.widgets.sankey.series.nodes import BaseNodes

from ..base import BaseSankey

Nodes = BaseNodes[Dict[str, pd.DataFrame]]
Connections = BaseConnections[Dict[str, pd.DataFrame]]


class SankeyPlayback(BaseSankey):
    """Spec for Base Sankey Playback widget."""

    def __init__(
        self,
        *,
        series_name: str = "series",
        nodes: Nodes,
        connections: Connections,
        playback: Playback,
        widget_id: Optional[str] = None,
        formatting: Optional[NumberFormatting] = None,
        title: WidgetTitleType = "",
    ) -> None:
        """Construct spec for base Sankey Playback widget.

        Args:
            series_name: name shown next to values in nodes
                and connections.
            nodes: spec for nodes.
            connections: spec for connections.
            playback: specs for Playback component.
            widget_id: unique widget id in a dashboard.
            formatting: formatting spec for value
                associated with nodes and connections.
            title: title of widget can be either a
                string (fixed value) or determined by a value from another widget
                using a WidgetLink.

        Examples:
            ??? example "Create a minimal sankey playback widget"
                ```py linenums="1"

                    import pandas as pd

                    from engineai.sdk.dashboard.dashboard import Dashboard
                    from engineai.sdk.dashboard.widgets.sankey import playback

                    nodes = {}
                    connections = {}
                    frames = []

                    # We now create a sankey playback with 3 frames, bases on the first
                    # three months

                    data = [[0.76, 0.24], [0.23, 0.53], [0.13, 0.11]]

                    for month, values in zip(["Jan", "Feb", "Mar"], data):
                        nodes[month] = pd.DataFrame(
                            {
                                "id": ["company", "imports", "exports"]
                            }
                        )
                        connections[month] = pd.DataFrame(
                            {
                                "from": ["company", "company"],
                                "to": ["imports", "exports"],
                                "value": values,
                            }
                        )
                        frames.append({"id": month})

                    sankey_widget = playback.SankeyPlayback(
                        nodes=playback.Nodes(
                            data=nodes,
                        ),
                        connections=playback.Connections(
                            data=connections,
                        ),
                        playback=playback.Playback(
                            data=pd.DataFrame(data=frames),
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
        self._playback = playback

    def _prepare(self, **_: object) -> None:
        """Method for each Widget prepare before building."""
        self._playback.prepare()

    def _build_playback(self) -> Mapping[str, Any]:
        return {"playback": self._playback.build()}

"""Spec for Sankey series."""

from typing import Any
from typing import Dict
from typing import Optional

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting import NumberFormatting
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings

from .connections import BaseConnections
from .nodes import BaseNodes


class Series(AbstractFactory):
    """Spec for Sankey series."""

    @type_check
    def __init__(
        self,
        *,
        name: TemplatedStringItem,
        nodes: BaseNodes[Any],
        connections: BaseConnections[Any],
        formatting: Optional[NumberFormatting] = None,
    ) -> None:
        """Constructs spec for a series of Sankey Widget.

        Args:
            name: name shown next to values in nodes and
                connections.
            nodes: spec for nodes.
            connections: spec for connections.
            formatting: formatting spec for value associated with nodes and connections.
        """
        super().__init__()
        self.__nodes = nodes
        self.__connections = connections
        self.__name = name
        self.__formatting = formatting if formatting else NumberFormatting()

    @property
    def nodes(self) -> BaseNodes[Any]:
        """Returns node spec."""
        return self.__nodes

    @property
    def connections(self) -> BaseConnections[Any]:
        """Returns node spec."""
        return self.__connections

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "name": build_templated_strings(items=self.__name),
            "formatting": self.__formatting.build(),
            "nodes": {"standard": self.__nodes.build()},
            "connections": self.__connections.build(),
        }

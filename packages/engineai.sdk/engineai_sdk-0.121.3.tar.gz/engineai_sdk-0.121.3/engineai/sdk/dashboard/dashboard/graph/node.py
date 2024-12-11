"""Specs for graph's node."""

from engineai.sdk.dashboard.data import DataSource


class Node:
    """Specs for dependency node."""

    def __init__(self, name: str, data_source: DataSource) -> None:
        """Node constructor."""
        self.name = name
        self.data_source = data_source
        self.args = {repr(dep) for dep in self.data_source.args}
        self.links = set(self.data_source.args)
        self.kwargs = {repr(self.data_source.kwargs)}

    def __str__(self) -> str:
        return (
            f"{self.name}{tuple(self.args) if self.args else ''}"
            f"{tuple(self.kwargs) if self.kwargs else ''}"
        )

    def __repr__(self) -> str:
        return (
            f"{self.name}{tuple(self.args) if self.args else ''}"
            f"{tuple(self.kwargs) if self.kwargs else ''}"
        )

    def __hash__(self) -> int:
        return hash(f"{self.name}_{''.join(self.args)}_{''.join(self.kwargs)}")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Node):
            return (
                self.name == other.name
                and self.args == other.args
                and self.kwargs == other.kwargs
            )
        return False

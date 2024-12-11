"""Spec for a root grid in a dashboard."""

from typing import Any
from typing import Dict
from typing import Final
from typing import List
from typing import Union

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.interface import CollapsibleInterface as CollapsibleSection
from engineai.sdk.dashboard.interface import SelectableInterface as SelectableSection
from engineai.sdk.dashboard.layout import FluidRow
from engineai.sdk.dashboard.layout import Grid
from engineai.sdk.dashboard.layout import Row
from engineai.sdk.dashboard.layout.typings import LayoutItem

ROW_HEIGHT_PIXELS: Final[int] = 100


class RootGrid(Grid):
    """Spec for a root grid in a dashboard."""

    @type_check
    def __init__(
        self, *items: Union[LayoutItem, Row, FluidRow, CollapsibleSection]
    ) -> None:
        """Construct dashboard grid.

        Args:
            items: items to add to grid. Can be widgets, rows or
                selectable sections (e.g tabs).
        """
        super().__init__()
        self._rows: List[
            Union[Row, FluidRow, CollapsibleSection, SelectableSection]
        ] = [
            (
                item
                if isinstance(
                    item, (Row, FluidRow, CollapsibleSection, SelectableSection)
                )
                else Row(item)
            )
            for item in items
        ]

    def __build_items(self) -> List[Dict[str, Any]]:
        return [
            {
                "fluid": row.build() if isinstance(row, FluidRow) else None,
                "responsive": row.build() if isinstance(row, Row) else None,
                "card": (row.build() if isinstance(row, CollapsibleSection) else None),
                "tabs": (row.build() if isinstance(row, SelectableSection) else None),
            }
            for row in self._rows
        ]

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "items": self.__build_items(),
            "rowHeightPixels": ROW_HEIGHT_PIXELS,
        }

"""Spec for the layout Collapsible Section Header."""

from typing import Optional

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.layout.components.header import BaseHeader
from engineai.sdk.dashboard.templated_string import TemplatedStringItem

from .chip import CollapsibleSectionChip


class CollapsibleSectionHeader(BaseHeader):
    """Provides title and chips for collapsible section headers.

    The CollapsibleSectionHeader class represents the header of a
    collapsible section, providing additional information such as
    title and chips.
    """

    @type_check
    def __init__(
        self,
        *chips: CollapsibleSectionChip,
        title: Optional[TemplatedStringItem] = None,
    ) -> None:
        """Constructor for CollapsibleSectionHeader.

        Args:
            chips: chips to be added to the collapsible section header.
            title: Collapsible Section title.

        Examples:
            ??? example "Create a Collapsible Section layout with a title"
                ```py linenums="1"
                # Add Header to a Collapsible Section
                import pandas as pd
                from engineai.sdk.dashboard.dashboard import Dashboard
                from engineai.sdk.dashboard.widgets import pie
                from engineai.sdk.dashboard import layout

                data = pd.DataFrame(
                   {
                       "category": ["A", "B"],
                       "value": [1, 2],
                   },
                )

                Dashboard(
                    content=layout.CollapsibleSection(
                        content=pie.Pie(data=data),
                        header=layout.CollapsibleSectionHeader(title="Header Title")
                    )
                )
                ```
        """
        super().__init__(*chips, title=title)

    def has_title(self) -> bool:
        """Method to validate if header has title."""
        return self.__title is not None

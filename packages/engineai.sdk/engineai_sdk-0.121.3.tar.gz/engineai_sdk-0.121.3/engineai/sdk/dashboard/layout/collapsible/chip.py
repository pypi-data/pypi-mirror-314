"""Spec for the layout Collapsible Section Header context."""

from typing import List
from typing import Optional
from typing import Union

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.layout.components.chip import BaseChip
from engineai.sdk.dashboard.links.typing import GenericLink
from engineai.sdk.dashboard.templated_string import TemplatedStringItem


class CollapsibleSectionChip(BaseChip):
    """Labels or links within collapsible section headers for extra context.

    The CollapsibleSectionChip class represents individual chips within a
    collapsible section header, providing additional labels or links.
    """

    @type_check
    def __init__(
        self,
        *,
        label: Union[str, GenericLink],
        tooltip_text: Optional[List[TemplatedStringItem]] = None,
        prefix: str = "",
        suffix: str = "",
    ) -> None:
        """Constructor for CollapsibleSectionChip.

        Args:
            label: Collapsible Section Header label value. Can assume a static label.
            tooltip_text: informational pop up text. Each element of list is displayed
                as a separate paragraph. Can only use this option if the `label` is
                set.
            prefix: prefix value to use in before each label.
            suffix: suffix value to use in after each label.

        Examples:
            ??? example "Create a Collapsible Section with multiple chips."
                ```py linenums="1"
                # Using a CollapsibleSectionChip with a static label and a
                # CollapsibleSectionChip with a Toggle widget.
                import pandas as pd
                from engineai.sdk.dashboard.dashboard import Dashboard
                from engineai.sdk.dashboard import layout
                from engineai.sdk.dashboard.widgets import toggle
                from engineai.sdk.dashboard.widgets import maps

                data = pd.DataFrame(
                    data=[
                        {"id": 1, "label": "Option 1"},
                        {"id": 2, "label": "Option 2"}
                    ]
                )
                toggle_widget = toggle.Toggle(data=data)

                chip = layout.CollapsibleSectionChip(label="Chip 1")
                linked_chip = layout.CollapsibleSectionChip(
                        label=toggle_widget.selected.label
                    )

                map_data = pd.DataFrame(
                   data=[{"region": "PT", "value": 10}, {"region": "GB", "value": 100}]
                )
                Dashboard(
                    content=[
                       toggle_widget,
                       layout.CollapsibleSection(
                            content=maps.Geo(data=map_data),
                            header=layout.CollapsibleSectionHeader(chip, linked_chip)
                        )
                    ]
                )
                ```

        """
        super().__init__(
            label=label,
            tooltip_text=tooltip_text,
            prefix=prefix,
            suffix=suffix,
        )

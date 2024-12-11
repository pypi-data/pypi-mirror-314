"""Spec for Url Link."""

from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Union

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.templated_string import DataField
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.actions.links.base import BaseLink


class UrlLink(BaseLink):
    """Spec for Url Link."""

    _INPUT_KEY: str = "actionHyperLink"

    @type_check
    def __init__(
        self,
        data_column: TemplatedStringItem,
        tooltip: Optional[Union[List[str], TemplatedStringItem, DataField]] = None,
    ) -> None:
        """Construct for ActionUrlLink class.

        Args:
            data_column (TemplatedStringItem): column that
                contains the url.
            tooltip (Optional[Union[List[str], TemplatedStringItem, DataField]]): static
                tooltip spec.
        """
        super().__init__(
            data_column=data_column,
            tooltip=tooltip,
        )

    def _build_tooltip(self) -> Dict[str, Any]:
        build_tooltip = self._tooltip.build() if self._tooltip else None
        if self._tooltip and isinstance(build_tooltip, Iterable):
            tooltip = build_tooltip
        elif self._tooltip:
            tooltip = [build_tooltip]
        else:
            tooltip = []
        return tooltip

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "urlKey": build_templated_strings(items=self._data_column),
            "tooltip": self._build_tooltip(),
            "params": [],
        }

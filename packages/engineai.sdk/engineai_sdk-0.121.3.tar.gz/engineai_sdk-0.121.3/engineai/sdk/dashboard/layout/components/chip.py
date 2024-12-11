"""Spec for the layout chip component."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.base import DependencyInterface
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.layout.components.label import build_context_label
from engineai.sdk.dashboard.links.typing import GenericLink
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings


class BaseChip(AbstractFactory):
    """Spec for the layout chip component.

    This component is used in Card and CollapsibleSection components.
    """

    @type_check
    def __init__(
        self,
        *,
        label: Union[str, GenericLink],
        tooltip_text: Optional[List[TemplatedStringItem]] = None,
        separator: str = "-",
        prefix: str = "",
        suffix: str = "",
    ) -> None:
        """Constructor for BaseChip.

        Args:
            label: Header label value. Can assume a static label or a single
                GenericLink.
            tooltip_text: informational pop up text. Each element of list is displayed
                as a separate paragraph. Can only use this option if the `label` is
                set.
            separator: label separator in case of a List of WidgetLinks
            prefix: prefix value to use in before each label.
            suffix: suffix value to use in after each label.
        """
        super().__init__()
        self.__tooltip_text = tooltip_text or []
        self.__label = label
        self.__separator = separator
        self.__prefix = prefix
        self.__suffix = suffix

    @property
    def dependencies(self) -> List[DependencyInterface]:
        """Method to generate the dependencies list from the elements of this class."""
        return [self.__label.dependency] if not isinstance(self.__label, str) else []

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            "label": build_context_label(
                label=self.__label,
                separator=self.__separator,
                prefix=self.__prefix,
                suffix=self.__suffix,
            ),
            "tooltipText": [
                build_templated_strings(items=tooltip)
                for tooltip in self.__tooltip_text
            ],
        }

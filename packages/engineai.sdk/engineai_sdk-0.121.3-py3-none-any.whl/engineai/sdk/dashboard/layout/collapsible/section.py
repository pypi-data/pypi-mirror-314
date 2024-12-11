"""Spec for a Collapsible Section in a dashboard grid layout."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from typing_extensions import Unpack

from engineai.sdk.dashboard.abstract.layout import AbstractLayoutItem
from engineai.sdk.dashboard.abstract.typing import PrepareParams
from engineai.sdk.dashboard.base import DependencyInterface
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.interface import CollapsibleInterface
from engineai.sdk.dashboard.interface import WidgetInterface as Widget
from engineai.sdk.dashboard.layout.build_item import build_item
from engineai.sdk.dashboard.layout.exceptions import ElementHeightNotDefinedError
from engineai.sdk.dashboard.layout.grid import Grid
from engineai.sdk.dashboard.layout.typings import LayoutItem
from engineai.sdk.dashboard.templated_string import TemplatedStringItem

from .header import CollapsibleSectionHeader


class CollapsibleSection(CollapsibleInterface):
    """Organize and group content with expandable/collapsible sections.

    The CollapsibleSection class is used to create collapsible sections
    within a dashboard layout, providing a way to organize and group
    content that can be expanded or collapsed.
    """

    _INPUT_KEY = "collapsible"

    @type_check
    def __init__(
        self,
        *,
        content: Union[LayoutItem, List[LayoutItem]],
        header: Optional[Union[TemplatedStringItem, CollapsibleSectionHeader]] = None,
        expanded: bool = True,
    ) -> None:
        """Constructor for CollapsibleSection.

        Args:
            content: content within the Section. One of Widget, Card, Grid,
                SelectableSection.
            header: Header specifications. By default the CollapsibleSection does
                not have title
            expanded: Whether the section is expanded or not.

        Examples:
            ??? example "Create a Collapsible Section layout and add a widget"
                ```py linenums="1"
                import pandas as pd
                from engineai.sdk.dashboard.dashboard import Dashboard
                from engineai.sdk.dashboard.widgets import maps
                from engineai.sdk.dashboard import layout

                data = pd.DataFrame(
                   data=[{"region": "PT", "value": 10}, {"region": "GB", "value": 100}]
                )

                Dashboard(content=layout.CollapsibleSection(
                    content=maps.Geo(data=data))
                )
                ```

            ??? example "Create a Collapsible Section layout with multiple Widgets"
                ```py linenums="1"
                import pandas as pd
                from engineai.sdk.dashboard.dashboard import Dashboard
                from engineai.sdk.dashboard.widgets import maps
                from engineai.sdk.dashboard import layout

                data = pd.DataFrame(
                   data=[{"region": "PT", "value": 10}, {"region": "GB", "value": 100}]
                )

                Dashboard(
                    content=layout.CollapsibleSection(content=[
                        maps.Geo(data=data),
                        maps.Geo(data=data)
                    ])
                )
                ```

        """
        super().__init__()
        self.__header = self._set_header(header)
        self.__content = self.__set_content(content)
        self.__height: Optional[Union[int, float]] = None
        self.__expanded = expanded

    @property
    def force_height(self) -> bool:
        """Get if the Section has a forced height."""
        return False

    @staticmethod
    def __set_content(
        content: Union[LayoutItem, List[LayoutItem]],
    ) -> LayoutItem:
        # pylint: disable=C0415
        """Sets content for Section."""
        return Grid(*content) if isinstance(content, list) else content

    @property
    def height(self) -> float:
        """Returns height required by Section based on underlying item height.

        Returns:
            float: height required by Section
        """
        if self.__height is None:
            raise ElementHeightNotDefinedError
        return self.__height

    @property
    def has_custom_heights(self) -> bool:
        """Returns if the Item has custom heights in its inner components."""
        return (
            False
            if isinstance(self.__content, Widget)
            else self.__content.has_custom_heights
        )

    def _set_header(
        self, header: Optional[Union[TemplatedStringItem, CollapsibleSectionHeader]]
    ) -> CollapsibleSectionHeader:
        if header is None:
            return CollapsibleSectionHeader()
        if isinstance(header, CollapsibleSectionHeader):
            return header
        return CollapsibleSectionHeader(title=header)

    def items(self) -> List[AbstractLayoutItem]:
        """Returns list of grid items that need to be inserted individually."""
        return self.__content.items()

    def prepare(self, **kwargs: Unpack[PrepareParams]) -> None:
        """Prepare Section.

        Args:
            **kwargs (Unpack[PrepareParams]): keyword arguments
        """
        self.__content.prepare(**kwargs)

    def prepare_heights(self, row_height: Optional[Union[int, float]] = None) -> None:
        """Prepare Selectable Layout heights."""
        if not isinstance(self.__content, Widget):
            self.__content.prepare_heights(row_height=row_height)

        self.__height = row_height or self.__content.height

    def __build_dependencies(self) -> List[Any]:
        """Build dependencies for Card."""
        return [
            self.__build_dependency(dependency)
            for dependency in self.__header.dependencies
        ]

    @staticmethod
    def __build_dependency(dependency: DependencyInterface) -> Dict[str, Any]:
        return {
            dependency.input_key: dependency.build(),
        }

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "item": build_item(self.__content),
            "height": self.height,
            "header": self.__header.build(),
            "expanded": self.__expanded,
            "dependencies": self.__build_dependencies(),
        }

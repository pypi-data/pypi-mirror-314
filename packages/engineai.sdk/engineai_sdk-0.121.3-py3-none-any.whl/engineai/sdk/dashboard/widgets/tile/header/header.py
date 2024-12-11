"""Spec for Tile Header."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links.abstract import AbstractFactoryLinkItemsHandler
from engineai.sdk.dashboard.templated_string import DataField
from engineai.sdk.dashboard.templated_string import InternalDataField
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.widgets.components.actions.links import UrlLink
from engineai.sdk.dashboard.widgets.tile.header.number_item import HeaderNumberItem

from ...components.actions.links.external import ExternalEvent
from ..content.exceptions import TileValidateValueError
from ..failure_handler import validation_failure_handler
from .exceptions import TileHeaderNoConfigurationError

Actions = Union[UrlLink, ExternalEvent]


class Header(AbstractFactoryLinkItemsHandler):
    """Spec for Tile Header."""

    @type_check
    def __init__(
        self,
        *,
        icon: Optional[Union[TemplatedStringItem, DataField]] = None,
        title: Optional[Union[TemplatedStringItem, DataField]] = None,
        item: Optional[HeaderNumberItem] = None,
        link: Optional[Actions] = None,
    ) -> None:
        """Construct spec for the Tile Widget Header.

        Args:
            icon: str that will be icon of header.
            title: str that will be title of header.
            item: tile header number item.
            link: action widget link spec.
        """
        super().__init__()

        self.__item = item
        self.__link = link

        self.__set_icon(icon=icon)
        self.__set_title(title=title)

        self.__verify_all_variables_none()

    def __set_icon(self, icon: Optional[Union[TemplatedStringItem, DataField]]) -> None:
        if icon is None:
            self.__icon = None
        elif isinstance(icon, (DataField)):
            self.__icon = InternalDataField(icon)
        else:
            self.__icon = InternalDataField(str(icon))

    def __set_title(
        self, title: Optional[Union[TemplatedStringItem, DataField]]
    ) -> None:
        if title is None:
            self.__title = None
        elif isinstance(title, (DataField)):
            self.__title = InternalDataField(title)
        else:
            self.__title = InternalDataField(str(title))

    def __verify_all_variables_none(self) -> None:
        """Method validate if all class variables are None error."""
        class_var = [
            self.__icon,
            self.__title,
            self.__item,
            self.__link,
        ]
        for var in class_var:
            if var is not None:
                return
        raise TileHeaderNoConfigurationError

    def validate(self, *, data: Dict[str, Any], required: bool) -> None:
        """Validates Tile Header."""
        if self.__icon is not None and str(self.__icon) not in data:
            validation_failure_handler(
                required=required,
                error=TileValidateValueError(
                    subclass="TileHeader",
                    argument="icon_key",
                    value=str(self.__icon),
                ),
            )
        if self.__title is not None and str(self.__title) not in data:
            validation_failure_handler(
                required=required,
                error=TileValidateValueError(
                    subclass="TileHeader",
                    argument="title_key",
                    value=str(self.__title),
                ),
            )

    def _build_item(self) -> Dict[str, Any]:
        """Method implemented by all header items."""
        return {
            "number": self.__item.build() if self.__item is not None else self.__item,
        }

    def _build_link(self) -> Dict[str, Any]:
        if isinstance(self.__link, ExternalEvent):
            return self.__link.build_action()

        if isinstance(self.__link, UrlLink):
            return {"actionHyperLink": self.__link.build()}

        msg = "TileHeader `link` requires one of ExternalEvent, UrlLink."
        raise TypeError(msg)

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec."""
        return {
            "icon": self.__icon.build() if self.__icon else None,
            "title": self.__title.build() if self.__title else "",
            "item": self._build_item() if self.__item is not None else None,
            "link": self._build_link() if self.__link is not None else None,
        }

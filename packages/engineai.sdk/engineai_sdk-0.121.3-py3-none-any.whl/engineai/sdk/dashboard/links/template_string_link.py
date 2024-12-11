"""Class that represents one of the possible Links after being stringify."""

from typing import Any
from typing import List
from typing import Optional
from typing import Union

from engineai.sdk.dashboard.abstract.selectable_widgets import AbstractSelectWidget
from engineai.sdk.dashboard.interface import RouteInterface

from .route_link import RouteLink
from .web_component import WebComponentLink


class TemplateStringLink:
    """Class that represents one of the possible Links after being stringify."""

    def __init__(self, template: str) -> None:
        """Construct for TemplateStringLink class.

        Args:
            template (str): String representing the link associated.
        """
        self.__route_field: Optional[str] = self._extract_field(
            template, "__ROUTE__.0."
        )
        self.__web_component_path: Optional[str] = self._extract_path(template)
        self.__widget_id: Optional[str] = self._extract_widget_id(template)
        self.__component: Optional[Union[AbstractSelectWidget, RouteInterface]] = None

    @staticmethod
    def _extract_field(template: str, prefix: str) -> Optional[str]:
        return template.replace(prefix, "") if prefix in template else None

    @staticmethod
    def _extract_path(template: str) -> Optional[List[str]]:
        if "web_component_" not in template:
            return None
        result = template.replace("web_component_", "")
        return result.replace(".", "_").split("_")

    @staticmethod
    def _extract_widget_id(template: str) -> Optional[str]:
        return (
            template.split(".")[0]
            if "__QUERY__" not in template
            and "__ROUTE__" not in template
            and "web_component_" not in template
            else None
        )

    @property
    def widget_id(self) -> str:
        """Returns Widget Id."""
        if self.__widget_id is None:
            msg = "No Widget ID set."
            raise ValueError(msg)
        return self.__widget_id

    @widget_id.setter
    def widget_id(self, widget_id: str) -> None:
        """Sets new Widget Id."""
        self.__widget_id = widget_id

    @property
    def component(self) -> Any:
        """Returns Widget."""
        if self.__component is None:
            msg = "No SelectWidget nor Route set."
            raise ValueError(msg)
        return self.__component

    @component.setter
    def component(self, component: Union[AbstractSelectWidget, RouteInterface]) -> None:
        """Sets Widget."""
        self.__component = component

    @property
    def route_link(self) -> RouteLink:
        """Returns Dashboard Route Link."""
        if self.__route_field is None:
            msg = "No Dashboard Route Link set."
            raise ValueError(msg)
        return RouteLink(field=self.__route_field, route=self.component)

    @property
    def web_component_link(self) -> WebComponentLink:
        """Returns WebComponent Link."""
        if self.__web_component_path is None:
            msg = "No WebComponent Link set."
            raise ValueError(msg)
        return WebComponentLink(path=self.__web_component_path)

    def is_widget_field(self) -> bool:
        """Returns if the TemplateStringLink is a WidgetField."""
        return self.__widget_id is not None

    def is_route_link(self) -> bool:
        """Returns if the TemplateStringLink is a DashboardRouteLink."""
        return self.__route_field is not None

    def is_web_component_link(self) -> bool:
        """Returns if the TemplateStringLink is a WebComponent."""
        return self.__web_component_path is not None

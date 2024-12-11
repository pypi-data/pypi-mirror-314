"""Top-level package for Dashboard Items with Link arguments."""

import re
from typing import Any
from typing import List
from typing import Set

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.data import DataSource
from engineai.sdk.dashboard.interface import HttpInterface as Http
from engineai.sdk.dashboard.templated_string import InternalDataField

from .route_link import RouteLink
from .template_string_link import TemplateStringLink
from .web_component import WebComponentLink
from .widget_field import WidgetField


class AbstractFactoryLinkItemsHandler(AbstractFactory):
    """Top-level package for Dashboard Items with Link arguments."""

    def __init__(self) -> None:
        """Construct for AbstractFactory class.

        This Abstract Item has the logic to get all WidgetLinks,
        associated to the class and its Children.

        Examples:
            class Child(AbstractFactoryItem):

                def __init__(label: Union[str, WidgetField]):
                    self.__label = label

            class Parent(AbstractFactoryItem):

                def __init__(title: Union[str, WidgetField], child: Child):
                    self.__title = title
                    self.__child = child

            parent = Parent(
                child=Child(label=WidgetField(widget=select_widget, field="b"))
            )

            parent.get_widget_fields() = [WidgetField(widget=select_widget, field="b")]

            In the build and publish process all the links are handle and publish.
        """
        super().__init__()
        self.__widget_fields: Set[WidgetField] = set()
        self.__route_links: Set[RouteLink] = set()
        self.__web_component_links: Set[WebComponentLink] = set()
        self.__template_link: Set[TemplateStringLink] = set()
        self.__internal_data_fields: Set[InternalDataField] = set()
        self.__data_sources: Set[DataSource] = set()
        self.__http_dependencies: Set[Http] = set()
        self.__checked_items: List[Any] = []

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        if isinstance(value, WidgetField):
            self.__widget_fields.add(value)
        elif isinstance(value, WebComponentLink):
            self.__web_component_links.add(value)
        elif isinstance(value, str):
            for template_link in self._get_template_links(value):
                self.__template_link.add(template_link)
        elif isinstance(value, RouteLink):
            self.__route_links.add(value)
        elif isinstance(value, InternalDataField):
            self.__internal_data_fields.add(value)
        elif isinstance(value, DataSource):
            self.__data_sources.add(value)
        elif isinstance(value, Http):
            self.__http_dependencies.add(value)

    @staticmethod
    def _get_template_links(value: str) -> List[TemplateStringLink]:
        return [TemplateStringLink(result) for result in re.findall("{{(.*?)}}", value)]

    @property
    def widget_fields(self) -> Set[WidgetField]:
        """Get Widget Links."""
        return self.__widget_fields

    @property
    def route_links(self) -> Set[RouteLink]:
        """Get Dashboard Route Links."""
        return self.__route_links

    @property
    def web_component_links(self) -> Set[WebComponentLink]:
        """Get Dashboard Web Component Links."""
        return self.__web_component_links

    @property
    def template_links(self) -> Set[TemplateStringLink]:
        """Get Dashboard Template Links."""
        return self.__template_link

    @property
    def internal_data_fields(self) -> Set[InternalDataField]:
        """Get Dashboard Internal Data Fields."""
        return self.__internal_data_fields

    @property
    def data_sources(self) -> Set[DataSource]:
        """Get Widget Data Sources."""
        return self.__data_sources

    @property
    def http_dependencies(self) -> Set[DataSource]:
        """Get Widget Data Sources."""
        return self.__http_dependencies

    def _get_abstract_items(
        self, variable: Any
    ) -> List["AbstractFactoryLinkItemsHandler"]:
        items = (
            [variable] if isinstance(variable, AbstractFactoryLinkItemsHandler) else []
        )

        for value in vars(variable).values():
            if isinstance(value, AbstractFactory) and value not in self.__checked_items:
                self.__checked_items.append(value)
                items += self._get_abstract_items(variable=value)
            elif isinstance(value, (set, list)):
                for item in value:
                    if (
                        isinstance(item, AbstractFactory)
                        and item not in self.__checked_items
                    ):
                        self.__checked_items.append(item)
                        items += self._get_abstract_items(variable=item)

        return items

    def get_widget_fields(self) -> Set[WidgetField]:
        """Get Widget Links inside the Item and its subcomponents."""
        widget_fields = self.widget_fields
        self.__checked_items = []

        items = self._get_abstract_items(variable=self)
        for item in items:
            widget_fields.update(item.widget_fields)

        return widget_fields

    def get_template_links(self) -> Set[TemplateStringLink]:
        """Get URL Links inside the Item and its subcomponents."""
        template_links = self.__template_link
        self.__checked_items = []

        for item in self._get_abstract_items(variable=self):
            template_links.update(item.template_links)

        return template_links

    def get_route_links(self) -> Set[RouteLink]:
        """Get URL Links inside the Item and its subcomponents."""
        route_links = self.__route_links
        self.__checked_items = []

        for item in self._get_abstract_items(variable=self):
            route_links.update(item.route_links)

        return route_links

    def get_web_component_links(self) -> Set[WebComponentLink]:
        """Get Web Components Links inside the Item and its subcomponents."""
        web_component_links = self.__web_component_links
        self.__checked_items = []

        for item in self._get_abstract_items(variable=self):
            web_component_links.update(item.web_component_links)

        return web_component_links

    def get_internal_data_fields(self) -> Set[InternalDataField]:
        """Get Internal Data Fields the Item and its subcomponents."""
        internal_data_fields = self.__internal_data_fields
        self.__checked_items = []

        for item in self._get_abstract_items(variable=self):
            internal_data_fields.update(item.internal_data_fields)

        return internal_data_fields

    def get_data_sources(self) -> Set[DataSource]:
        """Get Data Sources inside the Item and its subcomponents."""
        data_sources = self.__data_sources
        self.__checked_items = []

        for item in self._get_abstract_items(variable=self):
            data_sources.update(item.data_sources)

        return data_sources

    def get_http_dependencies(self) -> Set[Http]:
        """Get Data Sources inside the Item and its subcomponents."""
        http_dependencies = self.__http_dependencies
        self.__checked_items = []

        for item in self._get_abstract_items(variable=self):
            http_dependencies.update(item.http_dependencies)

        return http_dependencies

"""Class to manage component's data and dependencies."""

import re
from copy import copy
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Type
from typing import Union
from typing import cast

import pandas as pd
from typing_extensions import Unpack

from engineai.sdk.dashboard.abstract.selectable_widgets import AbstractSelectWidget
from engineai.sdk.dashboard.abstract.typing import PrepareParams
from engineai.sdk.dashboard.dependencies import WidgetSelectDependency
from engineai.sdk.dashboard.links import RouteLink
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.links.abstract import AbstractFactoryLinkItemsHandler
from engineai.sdk.dashboard.widgets.exceptions import (
    WidgetTemplateStringWidgetNotFoundError,
)

from ...base import DependencyInterface
from ...dependencies.datastore import DashboardStorage
from ..decorator import DataSource
from ..decorator import OperationItem
from ..enums import StorageType
from ..http import Http
from .interface import DependencyManagerInterface
from .interface import StaticDataType

WidgetDataType = Union[DataSource, StaticDataType, Http]

RouteDataType = Union[DataSource, pd.DataFrame, Http]


class DependencyManager(AbstractFactoryLinkItemsHandler, DependencyManagerInterface):
    """Class to manage component's data and dependencies."""

    def __init__(
        self,
        data: Optional[Union[WidgetDataType, RouteDataType]] = None,
        base_path: Optional[str] = None,
    ) -> None:
        """Constructor to manage components data.

        Args:
            data: data for the widget.
                Can be a pandas dataframe or a dictionary depending on the widget type,
                or Storage object if the data is to be retrieved from a storage.
            base_path: data storage base path.
        """
        super().__init__()
        self.__dependencies: Set[DependencyInterface] = set()
        self._data = self.__set_data(data=data, base_path=base_path)

    @property
    def dependencies(self) -> Set[DependencyInterface]:
        """Returns dependencies of widget.

        Returns:
            Set[DependencyInterface]: dependencies of widget
        """
        return self.__dependencies

    def __set_data(
        self,
        data: Optional[Union[WidgetDataType, RouteDataType, Http]],
        base_path: Optional[str] = None,
    ) -> Optional[Union[DataSource, Http]]:
        if data is None:
            return None
        if isinstance(data, Http):
            data.dependency.dependency_id = self.dependency_id
            return data
        data = (
            data
            if isinstance(data, DataSource)
            else DataSource(data, base_path=base_path)
        )
        data.component = self
        return data

    @property
    def data(self) -> Union[Set[DataSource], Set[Http]]:
        """Returns data of widget.

        Returns:
            WidgetDataType: data of widget
        """
        return (
            self.get_data_sources()
            if not self.has_http_data
            else self.get_http_dependencies()
        )

    @property
    def has_http_data(self) -> bool:
        """Returns True if widget has http data.

        Returns:
            bool: True if widget has http data
        """
        return isinstance(self._data, Http)

    def _prepare_dependencies(self, **kwargs: Unpack[PrepareParams]) -> None:
        """Prepares dependencies for widget."""
        page_id = re.sub(r"\W+", "", kwargs["page"].path)
        self.__set_internal_data_field()
        self.__set_template_links_widgets(**kwargs)
        self.__set_storage(**kwargs)
        self.__prepare_web_component_links()
        self.__prepare_template_dependencies()
        self.__prepare_route_dependencies()
        self.__prepare_widget_fields()
        self.__prepare_widget_dependencies(page_id)
        self.__prepare_http_dependencies()

    def store_data(
        self, write: bool, metadata: Set[str], **kwargs: Unpack[PrepareParams]
    ) -> None:
        """Stores data in widget."""
        for data_source in self.get_data_sources():
            data_source.storage_type = kwargs.get("storage_type")
            data_source(
                storage_config=kwargs["storage"],
                write_keys=write,
                metadata=metadata,
            )

    def build_datastore_dependencies(self) -> List[Any]:
        """Build datastore dependencies."""
        return [
            self.__build_dependency(dependency) for dependency in self.__dependencies
        ]

    @staticmethod
    def __build_dependency(dependency: DependencyInterface) -> Dict[str, Any]:
        return {
            dependency.input_key: dependency.build(),
        }

    def __prepare_widget_dependencies(self, page_id: str) -> None:
        for dependency in self.__dependencies:
            if (
                isinstance(dependency, WidgetSelectDependency)
                and page_id
                and not dependency.widget_id.endswith(page_id)
            ):
                dependency.widget_id = f"{dependency.widget_id}_{page_id}"

    def __prepare_http_dependencies(self) -> None:
        for http in self.get_http_dependencies():
            http_dependency = http.dependency
            self.__dependencies.add(http_dependency)
            if http_dependency.operations is not None:
                self.__add_operations_dependencies(
                    operations=http_dependency.operations,
                )

    def __prepare_web_component_links(self) -> None:
        for web_component in self.get_web_component_links():
            self.__dependencies.add(web_component.dependency)

    def __prepare_widget_fields(self) -> None:
        for widget_field in self.get_widget_fields():
            dependency = widget_field.link_component.select_dependency()
            self.__dependencies.add(cast(WidgetSelectDependency, dependency))

    def __prepare_template_dependencies(self) -> None:
        for template_link in self.get_template_links():
            if template_link.is_widget_field():
                dependency = template_link.component.select_dependency(
                    dependency_id=template_link.widget_id
                )

                self.__dependencies.add(
                    cast(
                        WidgetSelectDependency,
                        dependency,
                    )
                )
            elif template_link.is_route_link():
                route_link = template_link.route_link
                self.__dependencies.add(route_link.dependency)
            elif template_link.is_web_component_link():
                self.__dependencies.add(template_link.web_component_link.dependency)

    def __prepare_route_dependencies(self) -> None:
        for route_link in self.get_route_links():
            self.__dependencies.add(route_link.dependency)

    def __set_internal_data_field(self) -> None:
        for internal_data_field in self.get_internal_data_fields():
            if internal_data_field.dependency_id == "":
                internal_data_field.set_dependency_id(dependency_id=self.dependency_id)

    def __set_template_links_widgets(
        self,
        **kwargs: Unpack[PrepareParams],
    ) -> None:
        dashboard_slug = kwargs["dashboard_slug"]
        selectable_widgets: Dict[str, AbstractSelectWidget] = kwargs[
            "selectable_widgets"
        ]
        for template_link in self.get_template_links():
            if template_link.is_web_component_link():
                continue
            if template_link.is_widget_field():
                if template_link.widget_id not in selectable_widgets:
                    raise WidgetTemplateStringWidgetNotFoundError(
                        slug=dashboard_slug,
                        widget_id=self.data_id,
                        template_widget_id=template_link.widget_id,
                    )
                template_link.component = cast(
                    AbstractSelectWidget,
                    selectable_widgets.get(template_link.widget_id),
                )
            elif template_link.is_route_link():
                template_link.component = kwargs["page"].route

    def __set_storage(self, **kwargs: PrepareParams) -> None:
        """Sets the data storage based on widget dependency id(s)."""
        for data_source in self.get_data_sources():
            data_source.storage_type = kwargs.get("storage_type")
            self.__add_link_dependencies(data_source=data_source)
            dependency: DashboardStorage = self.__set_dependency(data_source)

            self.__dependencies.add(dependency)

            if data_source.operations is not None:
                self.__add_operations_dependencies(
                    operations=data_source.operations,
                )

    def __set_dependency(self, data_source: DataSource) -> DashboardStorage:
        _storage_type: Type[DashboardStorage] = StorageType.get_storage_class(
            data_source.storage_type.value
        )
        return _storage_type(
            dependency_id=data_source.component.dependency_id,
            series_id=self.__generate_series_id(data_source),
            operations=data_source.operations,
        )

    @staticmethod
    def __generate_series_id(data_source: DataSource) -> str:
        if len(data_source.args) > 0:
            store_id_templates: List[str] = [str(link) for link in data_source.args]

            series_id = (
                store_id_templates[0]
                if len(store_id_templates) == 1
                else data_source.separator.join(store_id_templates)
            )
            return f"{data_source.base_path}/{series_id}"
        return data_source.base_path

    def __add_link_dependencies(self, data_source: DataSource) -> None:
        for link in data_source.args:
            if isinstance(link, WidgetField):
                dependency = cast(
                    WidgetSelectDependency, link.link_component.select_dependency()
                )
                self.__dependencies.add(dependency)

            elif isinstance(link, RouteLink):
                new_link = copy(link)
                new_link.dependency.path = data_source.base_path
                self.__dependencies.add(new_link.dependency)

    def __add_operations_dependencies(
        self,
        operations: List[OperationItem],
    ) -> None:
        for operation in operations:
            for dependency in operation.dependencies:
                self.__dependencies.add(dependency)

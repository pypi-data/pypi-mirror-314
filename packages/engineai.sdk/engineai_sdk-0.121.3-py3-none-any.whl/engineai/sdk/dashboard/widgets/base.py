"""Base spec shared by all widgets."""

import re
from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas as pd
from typing_extensions import Unpack

from engineai.sdk.dashboard.abstract.layout import AbstractLayoutItem
from engineai.sdk.dashboard.abstract.selectable_widgets import AbstractSelectWidget
from engineai.sdk.dashboard.abstract.typing import PrepareParams
from engineai.sdk.dashboard.data.manager.manager import DependencyManager
from engineai.sdk.dashboard.data.manager.manager import WidgetDataType
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.dependencies import WidgetSelectDependency
from engineai.sdk.dashboard.exceptions import WidgetDataNotFoundError
from engineai.sdk.dashboard.exceptions import WidgetFieldNotFoundError
from engineai.sdk.dashboard.interface import WidgetInterface
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.links.typing import GenericLink
from engineai.sdk.dashboard.selected import Selected
from engineai.sdk.dashboard.widgets.exceptions import WidgetIdValueError

WidgetTitleType = Optional[Union[str, GenericLink]]


class Widget(DependencyManager, AbstractLayoutItem, WidgetInterface):
    """Building blocks of visualizations within the Platform SDK."""

    _WIDGET_API_TYPE: Optional[str] = None
    _DEFAULT_HEIGHT: Union[int, float] = 4
    _FORCE_HEIGHT: bool = False
    _FLUID_ROW_COMPATIBLE: bool = False
    _WIDGET_HEIGHT_STEP = 0.1
    _WIDGET_ID_COUNTER = 0
    _INPUT_KEY = "widget"

    @type_check
    def __init__(
        self,
        *,
        widget_id: Optional[str] = None,
        data: Optional[WidgetDataType] = None,
    ) -> None:
        """Shared fields by all widgets.

        Args:
            widget_id: unique id amongst other widgets in a dashboard
            data: data for the widget. Can be a
                pandas dataframe or a dictionary depending on the widget type, or
                Storage object if the data is to be retrieved from a storage.
        """
        super().__init__(
            base_path=(__widget_id := self.__set_widget_id(widget_id)),
            data=data,
        )
        self.__widget_id = __widget_id

    @property
    def fluid_row_compatible(self) -> bool:
        """Returns True if widget is compatible with fluid row."""
        return self._FLUID_ROW_COMPATIBLE

    @property
    def data_id(self) -> str:
        """Returns data id."""
        return self.__widget_id

    def __set_widget_id(self, widget_id: Optional[str]) -> str:
        if widget_id is None:
            self._increment_widget_id_counter()
            return f"{self._WIDGET_API_TYPE}_{self._WIDGET_ID_COUNTER}"

        pattern = re.compile("^[a-zA-Z0-9-_]+$")

        if pattern.search(widget_id) is None:
            raise WidgetIdValueError(
                class_name=self.__class__.__name__,
                widget_id=widget_id,
            )

        return widget_id

    @classmethod
    def _increment_widget_id_counter(cls) -> None:
        cls._WIDGET_ID_COUNTER = cls._WIDGET_ID_COUNTER + 1

    def prepare_heights(self, row_height: Optional[Union[int, float]] = None) -> None:  # noqa
        """Prepare heights."""
        return

    @property
    def has_custom_heights(self) -> bool:
        """Returns widget has custom heights."""
        return False

    def items(self) -> List[AbstractLayoutItem]:
        """Returns list of items in layout."""
        return [self]

    @property
    def _widget_api_type(self) -> str:
        """Returns widget API type value.

        All widgets must now have the WIDGET_API_TYPE defined, and must match the API
        Input that has to be implemented, if not implement the  widget will raise
        NotImplementedError.

        Examples:
        class Cartesian(Widget):
            WIDGET_API_TYPE = "continuousCartesian"
        """
        if self._WIDGET_API_TYPE is None:
            msg = f"Class {self.__class__.__name__}._WIDGET_API_TYPE not defined."
            raise NotImplementedError(msg)
        return self._WIDGET_API_TYPE

    @property
    def height(self) -> float:
        """Returns True if widget height is auto."""
        return self._DEFAULT_HEIGHT

    @property
    def force_height(self) -> bool:
        """Returns True if widget height is forced."""
        return self._FORCE_HEIGHT

    @property
    def item_id(self) -> str:
        """Returns widget's id.

        Returns:
            str: widget id
        """
        return self.__widget_id

    @property
    def widget_id(self) -> str:
        """Unique id amongst other widgets in a dashboard."""
        return self.__widget_id

    @property
    def input_key(self) -> str:
        """Return input type argument value.

        All Select Layout Items must now have the _INPUT_KEY defined.
        """
        if self._INPUT_KEY is None:
            msg = f"Class {self.__class__.__name__}._INPUT_KEY not defined."
            raise NotImplementedError(msg)
        return self._INPUT_KEY

    @abstractmethod
    def _build_widget_input(self) -> Dict[str, Any]:
        """Builds widget Input specs for dashboard API.

        Returns:
            Dictionary with widget name and spec.
        """

    def prepare(self, **kwargs: Unpack[PrepareParams]) -> None:
        """Prepare widget for rendering."""
        self.__set_page_id(kwargs["page"].path)
        self._prepare_dependencies(**kwargs)
        self._prepare()

    def __set_page_id(self, path: str) -> None:
        page_id = re.sub(r"\W+", "", path)
        if page_id:
            self.__widget_id = f"{self.__widget_id}_{page_id}"

    def _prepare(self, **kwargs: object) -> None:
        """Method for each Widget prepare before building."""

    def _build_widget_type(self) -> Dict[str, Any]:
        return {self._widget_api_type: self._build_widget_input()}

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            "widgetId": self.__widget_id,
            "dependencies": self.build_datastore_dependencies(),
            "widgetType": self._build_widget_type(),
        }


class _Selected(Selected[AbstractSelectWidget, WidgetField, Widget]):
    """Widget Selected property configuration."""


class SelectableWidget(Widget, AbstractSelectWidget):
    """Base spec shared by all widgets that can be selected."""

    @type_check
    def __init__(
        self,
        *,
        widget_id: Optional[str] = None,
        data: WidgetDataType,
    ) -> None:
        """Shared fields by all widgets.

        Args:
            widget_id: unique id amongst other widgets in a dashboard
            data: data to be used by widget. Accepts DataSource
                method as well as raw data.
        """
        super().__init__(widget_id=widget_id, data=data)
        self.selected = _Selected(component=self)

    @type_check
    def select_dependency(self, *, dependency_id: str = "") -> WidgetSelectDependency:
        """Return dependency for selectable widget.

        Args:
            dependency_id (str): id of dependency to selectable widget.
                Defaults to "" (i.e. uses widgetId as dependency id).

        Returns:
            WidgetDependency: spec for dependency to select_widget
        """
        return WidgetSelectDependency(
            dependency_id=self.widget_id if dependency_id == "" else dependency_id,
            widget_id=self.widget_id,
        )

    def validate_field(self, field: str, data: pd.DataFrame) -> None:
        """Validates if field is exposed by widget.

        For instance if field is an id of one of the columns in a table

        Args:
            field (str): id of field exposed by widget.
            data (DataFrame): pandas DataFrame or dict where
                the data is present.

        Raises:
            WidgetDataNotFoundError: if there is no data.
            WidgetFieldNotFoundError: if the field is not present in the data.
        """
        if data is None or data.empty:
            raise WidgetDataNotFoundError(widget_id=self.widget_id)

        if field not in data.columns:
            raise WidgetFieldNotFoundError(field=field, columns=list(data.columns))

    def build(self) -> Dict[str, Any]:
        """Select widget build."""
        return {
            "widgetId": self.widget_id,
            "dependencies": self.build_datastore_dependencies(),
            "widgetType": self._build_widget_type(),
        }

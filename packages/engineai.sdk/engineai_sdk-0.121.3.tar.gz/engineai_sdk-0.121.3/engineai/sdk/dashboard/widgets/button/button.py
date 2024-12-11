"""Spec for Cartesian widget."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Set
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.data.decorator import DataSource
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.base import Widget

from .external import ExternalAction


class Button(Widget):
    """Spec for Button widget."""

    _DEPENDENCY_ID = "__BUTTON_DATA_DEPENDENCY__"
    _WIDGET_API_TYPE = "button"
    _FLUID_ROW_COMPATIBLE = True

    _DEFAULT_HEIGHT = 0.5
    _FORCE_HEIGHT = True

    @type_check
    def __init__(
        self,
        *,
        action: ExternalAction,
        widget_id: Optional[str] = None,
        icon: Optional[TemplatedStringItem] = None,
        label: Optional[TemplatedStringItem] = None,
    ) -> None:
        """Construct spec for Button widget.

        Args:
            action: Type of action to be performed on the button.
            widget_id: unique widget id in a dashboard.
            icon: icon spec.
            label: label to be displayed in the button.
        """
        super().__init__(widget_id=widget_id)
        self.__icon = icon
        self.__label = label
        self.__action = action

    def _prepare(self, **_: object) -> None:
        if self.__label is None:
            self.__label = self.__action.event_type

    def validate(self, _: Union[pd.DataFrame, Dict[str, Any]], **__: object) -> None:
        """Widget validations. Button has no data to validate."""
        return

    @property
    def data(self) -> Set[DataSource]:
        """Button has empty data."""
        data_source = DataSource(dict, base_path=self.dependency_id)
        data_source.component = self
        return {data_source}

    def _build_widget_input(self) -> Dict[str, Any]:
        return {
            "icon": build_templated_strings(items=self.__icon) if self.__icon else None,
            "label": (
                build_templated_strings(items=self.__label) if self.__label else None
            ),
            "action": {"external": self.__action.build()},
        }

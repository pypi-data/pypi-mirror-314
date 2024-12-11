"""Spec for Select widget."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.data import DataSource
from engineai.sdk.dashboard.data.http import Http
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.base import SelectableWidget
from engineai.sdk.dashboard.widgets.utils import build_data

from .exceptions import SelectValidateUniqueIDError
from .exceptions import SelectValidateValueError
from .group import Group


class Select(SelectableWidget):
    """Construct select widget.

    Construct a select widget for choosing from a list of options,
    with options to customize the data source, ID column,
    default selection, label column, widget ID, label text,
    grouping, and label display options.
    """

    _DEPENDENCY_ID = "__SELECT_DATA_DEPENDENCY__"

    _WIDGET_API_TYPE = "select"
    _FLUID_ROW_COMPATIBLE = True

    _DEFAULT_HEIGHT = 0.5
    _FORCE_HEIGHT = True

    @type_check
    def __init__(
        self,
        data: Union[DataSource, pd.DataFrame, Http],
        *,
        id_column: TemplatedStringItem = "id",
        default_selection: Optional[str] = None,
        label_column: Optional[TemplatedStringItem] = None,
        widget_id: Optional[str] = None,
        label: TemplatedStringItem = "",
        label_outside: bool = True,
        group_column: Optional[TemplatedStringItem] = None,
        show_group_when_selected: bool = False,
    ) -> None:
        """Constructor for Select widget.

        Args:
            data: data to be used by widget. Accepts storages as well as raw data.
            widget_id: unique widget id in a dashboard.
            id_column: name of column in pandas dataframe(s) used for the id associated
                with each entry.
            label_column: name of column in pandas dataframe(s) used for the value
                displayed for each entry.
            default_selection: id of entry that is selected by default.
            label: label shown before select options.
            label_outside: flag that inserts the `label` parameter outside the
                select dropdown.
            group_column: name of column in pandas dataframe(s) used to define the
                entries groups.
            show_group_when_selected: flag will append the group name into entry label.

        Examples:
            ??? example "Create a minimal select widget"
                ```py linenums="1"
                import pandas as pd
                from engineai.sdk.dashboard import dashboard
                from engineai.sdk.dashboard.widgets import select
                data = pd.DataFrame(
                    {
                        "id": ["A", "B"],
                    },
                )
                dashboard.Dashboard(content=select.Select(data=data))
                ```

            ??? example "Create select widget with group"
                ```py linenums="1"
                import pandas as pd
                from engineai.sdk.dashboard import dashboard
                from engineai.sdk.dashboard.widgets import select
                data = pd.DataFrame(
                    {
                        "id": ["A", "B", "C", "D", "E"],
                        "group": ["group1", "group2", None, "group1", "group3"],
                    },
                )
                dashboard.Dashboard(
                    content=select.Select(
                        data=data, group_column="group"
                    )
                )
                ```
        """
        super().__init__(widget_id=widget_id, data=data)
        self.__label_outside = label_outside
        self.__id_column = id_column
        self.__label_column = label_column or id_column
        self.__default_selection = default_selection
        self.__label = label
        self.__group = (
            Group(
                group_column=group_column,
                show_group_when_selected=show_group_when_selected,
            )
            if group_column is not None
            else None
        )

    def validate(self, data: pd.DataFrame, **_: Any) -> None:
        """Validates widget spec.

        Args:
            data (DataFrame): pandas DataFrame where the data is present.
        """
        if isinstance(self.__id_column, str):
            if self.__id_column in data.columns:
                ids = data[self.__id_column].unique()
                if len(ids) != len(data.index):
                    raise SelectValidateUniqueIDError(
                        unique_ids=len(ids),
                        nr_rows=len(data.index),
                    )
            else:
                raise SelectValidateValueError(
                    argument="id_column",
                    value=self.__id_column,
                )

        if (
            isinstance(self.__label_column, str)
            and self.__label_column not in data.columns
        ):
            raise SelectValidateValueError(
                argument="label_column",
                value=self.__label_column,
            )

        if self.__group is not None:
            self.__group.validate(data)

    def _build_widget_input(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            "option": {
                "idKey": build_templated_strings(items=self.__id_column),
                "labelKey": build_templated_strings(items=self.__label_column),
                "grouping": self.__group.build() if self.__group is not None else None,
            },
            "label": {
                "text": build_templated_strings(items=self.__label),
                "isOutside": self.__label_outside,
            },
            "initialState": {
                "selected": (
                    [self.__default_selection]
                    if self.__default_selection is not None
                    else []
                ),
            },
            "data": build_data(self.dependency_id),
        }

"""Spec for a column in a dashboard vertical grid layout."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from typing_extensions import Unpack

from engineai.sdk.dashboard.abstract.layout import AbstractLayoutItem
from engineai.sdk.dashboard.abstract.typing import PrepareParams
from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.layout.build_item import build_item
from engineai.sdk.dashboard.layout.typings import LayoutItem
from engineai.sdk.dashboard.widgets.base import Widget

from .exceptions import ColumnLimitsWidthError
from .exceptions import ColumnWrongWidthSizeError
from .exceptions import ElementHeightNotDefinedError


class Column(AbstractFactory):
    """Organize and group content vertically within a vertical grid layout.

    The Column class represents a column within a vertical grid layout,
    providing a way to organize and group content vertically.
    """

    @type_check
    def __init__(self, *, content: LayoutItem, width: Optional[int] = None) -> None:
        """Constructor for Column.

        Args:
            content: Representing the base class for items in a dashboard layout.
                It's a common type that other layout-related classes inherit from.
            width: Sets the column width, value between 3 and 12. If value is None
                the width will be set automatically based on the number of columns
                in the row.

        Examples:
            ??? example "Create Column with widget"
                ```py linenums="1"
                import pandas as pd

                from engineai.sdk.dashboard import dashboard
                from engineai.sdk.dashboard import layout
                from engineai.sdk.dashboard.widgets import select

                data = pd.DataFrame({"id": [1, 2, 3]})

                dashboard.Dashboard(
                    content=layout.Grid(
                        layout.Row(
                            layout.Column(content=select.Select(data))
                        )
                    )
                )
                ```

            ??? example "Columns with default Width"
                ```py linenums="1"
                import pandas as pd

                from engineai.sdk.dashboard import dashboard
                from engineai.sdk.dashboard import layout
                from engineai.sdk.dashboard.widgets import select
                from engineai.sdk.dashboard.widgets import toggle

                data = pd.DataFrame({"id": [1, 2, 3]})

                dashboard.Dashboard(
                    content=layout.Grid(
                        layout.Row(
                            layout.Column(content=select.Select(data)),
                            layout.Column(content=toggle.Toggle(data)),
                        )
                    )
                )
                ```

            ??? example "Columns with custom Width"
                ```py linenums="1"
                import pandas as pd

                from engineai.sdk.dashboard import dashboard
                from engineai.sdk.dashboard import layout
                from engineai.sdk.dashboard.widgets import select
                from engineai.sdk.dashboard.widgets import toggle

                data = pd.DataFrame({"id": [1, 2, 3]})

                dashboard.Dashboard(
                    content=layout.Grid(
                        layout.Row(
                            layout.Column(content=select.Select(data), width=4),
                            layout.Column(content=toggle.Toggle(data), width=8),
                        )
                    )
                )
                ```
        """
        super().__init__()
        if width:
            if width < 2 or width > 12:
                raise ColumnLimitsWidthError
            if (width % 2) != 0 and width != 3:
                raise ColumnWrongWidthSizeError

        self.__width = width
        self.__item = content
        self.__height: Optional[Union[int, float]] = None

    @property
    def width(self) -> Optional[int]:
        """Returns height required by column based on height required by item in column.

        Returns:
            int: width required by column
        """
        return self.__width

    def prepare(
        self, auto_width: Optional[int], **kwargs: Unpack[PrepareParams]
    ) -> None:
        """Prepares column."""
        self.__width = auto_width or self.__width
        self.__item.prepare(**kwargs)

    def prepare_heights(self, row_height: Optional[Union[int, float]] = None) -> None:
        """Prepares column height."""
        if not isinstance(self.__item, Widget):
            self.__item.prepare_heights(row_height=row_height)

        self.__height = row_height or self.__item.height

    @property
    def height(self) -> float:
        """Returns columns heights."""
        if self.__height is None:
            raise ElementHeightNotDefinedError
        return self.__height

    @property
    def has_custom_heights(self) -> bool:
        """Returns if the Column has custom heights."""
        return (
            False if isinstance(self.__item, Widget) else self.__item.has_custom_heights
        )

    @property
    def force_height(self) -> bool:
        """Returns if the Column has a forced height form the of item."""
        return self.__item.force_height if isinstance(self.__item, Widget) else False

    def items(self) -> List[AbstractLayoutItem]:
        """Returns list of grid items that need to be inserted individually."""
        return self.__item.items()

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "width": self.__width,
            "item": build_item(self.__item),
        }

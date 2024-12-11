"""Spec for a fluid row in a dashboard vertical grid layout."""

from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Union

from typing_extensions import Unpack

from engineai.sdk.dashboard.abstract.typing import PrepareParams
from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.enum.align import (
    FluidHorizontalAlignment as HorizontalAlignment,
)
from engineai.sdk.dashboard.enum.align import VerticalAlignment
from engineai.sdk.dashboard.layout.exceptions import ElementHeightNotDefinedError
from engineai.sdk.dashboard.widgets.base import Widget


class FluidRow(AbstractFactory):
    """Enables flexible and responsive content alignment in a vertical grid layout.

    The FluidRow class represents a fluid row within a vertical grid layout,
    allowing for flexible and responsive content alignment.
    """

    def __init__(
        self,
        *items: Widget,
        vertical_alignment: VerticalAlignment = VerticalAlignment.TOP,
        horizontal_alignment: HorizontalAlignment = HorizontalAlignment.CENTER,
    ) -> None:
        """Constructor for FluidRow.

        Args:
            items: item within the FluidRow must be compatible.
            vertical_alignment: Fluid Row vertical alignment option.
                `TOP`, `MIDDLE` or `BOTTOM`, available.
            horizontal_alignment: Fluid Row horizontal alignment option.
                `LEFT`, `CENTER`, `RIGHT` or `STRETCH` available.

        Examples:
            ??? example "Create Fluid Row with widget"
                ```py linenums="1"
                import pandas as pd

                from engineai.sdk.dashboard import dashboard
                from engineai.sdk.dashboard import layout
                from engineai.sdk.dashboard.widgets import select

                data = pd.DataFrame({"id": [1, 2, 3]})

                dashboard.Dashboard(
                    content=layout.Grid(
                        layout.FluidRow(select.Select(data))
                    )
                )
                ```

            ??? example "Create FluidRow with multiple Widgets"
                ```py linenums="1"
                import pandas as pd

                from engineai.sdk.dashboard import dashboard
                from engineai.sdk.dashboard import layout
                from engineai.sdk.dashboard.widgets import select
                from engineai.sdk.dashboard.widgets import toggle

                data = pd.DataFrame({"id": [1, 2, 3]})

                dashboard.Dashboard(
                    content=layout.Grid(
                        layout.FluidRow(
                            select.Select(data),
                            toggle.Toggle(data),
                        )
                    )
                )
                ```

            ??? example "Create FluidRow with left alignment"
                ```py linenums="1"
                import pandas as pd

                from engineai.sdk.dashboard import dashboard
                from engineai.sdk.dashboard import layout
                from engineai.sdk.dashboard.enum import align
                from engineai.sdk.dashboard.widgets import select
                from engineai.sdk.dashboard.widgets import toggle

                data = pd.DataFrame({"id": [1, 2, 3]})

                dashboard.Dashboard(
                    content=layout.Grid(
                        layout.FluidRow(
                            select.Select(data),
                            toggle.Toggle(data),
                            horizontal_alignment=align.FluidHorizontalAlignment.LEFT,
                        )
                    )
                )
                ```
        """
        super().__init__()
        self.__items: List[Widget] = []
        self.__set_items(*items)
        self.__height: Optional[Union[int, float]] = None
        self.__vertical_alignment = vertical_alignment.value
        self.__horizontal_alignment = horizontal_alignment.value

    def __set_items(self, *items: Widget) -> None:
        """Set items for fluid row."""
        for item in items:
            if not item.fluid_row_compatible:
                msg = (
                    f"Item {item} is not compatible with FluidRow. "
                    "Please use a compatible item."
                )
                raise ValueError(msg)
            self.__items.append(item)

    def prepare_heights(self) -> None:
        """Prepare fluid row heights."""
        self.__height = float(max(item.height for item in self.__items))

    @property
    def force_height(self) -> bool:
        """Get if the Row has a forced height from the ."""
        return True

    @property
    def height(self) -> float:
        """Get row height."""
        if self.__height is None:
            raise ElementHeightNotDefinedError
        return self.__height

    def items(self) -> Iterable[Widget]:
        """Return items associated."""
        return self.__items

    @property
    def widgets(self) -> List[Widget]:
        """Returns list of widgets in dashboard grid row layout.

        Returns:
            List[Widget]: list of widget
        """
        return self.__items

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "height": self.__height,
            "items": [{"widget": item.build()} for item in self.__items],
            "verticalAlign": self.__vertical_alignment,
            "horizontalAlign": self.__horizontal_alignment,
        }

    def prepare(self, **kwargs: Unpack[PrepareParams]) -> None:
        """Prepare row."""
        for item in self.__items:
            item.prepare(**kwargs)

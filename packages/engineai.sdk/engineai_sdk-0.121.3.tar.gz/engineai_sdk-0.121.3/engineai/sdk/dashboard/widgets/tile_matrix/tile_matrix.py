"""Spec for TileMatrix Widget."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import pandas as pd
from pandas.api.types import is_array_like
from pandas.api.types import is_numeric_dtype

from engineai.sdk.dashboard.data.decorator import DataSource
from engineai.sdk.dashboard.data.http import Http
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.widgets.base import Widget
from engineai.sdk.dashboard.widgets.utils import build_data

from .items.chart.line import LineChartItem
from .items.number.item import NumberItem
from .items.text.item import TextItem
from .typing import TileMatrixItem


class TileMatrix(Widget):
    """Spec for Tile Matrix Widget."""

    _DEPENDENCY_ID = "__TILE_MATRIX_DATA_DEPENDENCY__"
    _WIDGET_API_TYPE = "tileMatrix"
    _DEFAULT_HEIGHT = 0.86
    _FLUID_ROW_COMPATIBLE = True

    @type_check
    def __init__(
        self,
        data: Union[DataSource, pd.DataFrame, Http],
        *,
        widget_id: Optional[str] = None,
        max_columns: Optional[int] = None,
        item: Optional[Union[TileMatrixItem, str]] = None,
    ) -> None:
        """Construct spec for the Tile Matrix Widget.

        Args:
            data: data to be used by
                widget. Accepts Storages as well as raw data.
            widget_id: unique widget id in a dashboard.
            max_columns: maximum number of columns to be displayed.
            item: Tile Matrix item. If not provided, it will look into
                the first column of the data and decide the item type.

        Examples:
            ??? example "Create a minimal Tile Matrix Widget"
                ```py linenums="1"
                    import pandas as pd
                    from engineai.sdk.dashboard.dashboard import Dashboard
                    from engineai.sdk.dashboard.widgets import tile_matrix

                    data = pd.DataFrame([{"number": i} for i in range(1, 5)])

                    tile_widget = tile_matrix.TileMatrix(data=data)

                    Dashboard(content=tile_widget)
                ```

            ??? example "Create a Tile Matrix Widget with item as string"
                ```py linenums="1"
                    import pandas as pd
                    from engineai.sdk.dashboard.dashboard import Dashboard
                    from engineai.sdk.dashboard.widgets import tile_matrix

                    data = pd.DataFrame([{"number": i} for i in range(1, 5)])

                    tile_widget = tile_matrix.TileMatrix(data=data, item="number")

                    Dashboard(content=tile_widget)
                ```
        """
        super().__init__(widget_id=widget_id, data=data)
        self.__item = self.__set_item(data=data, item=item)
        self.__max_columns = max_columns

    def _prepare(self, **_: object) -> None:
        self.__item.prepare()

    def __set_item(
        self,
        data: Union[DataSource, pd.DataFrame, Http],
        item: Optional[Union[TileMatrixItem, str]],
    ) -> TileMatrixItem:
        """Sets item for Tile Matrix Widget.

        Args:
            data: data to be used by widget.
            item: Tile Matrix item
        """
        if item is not None:
            if isinstance(item, str):
                return TextItem(data_column=item)
            return item

        if (
            isinstance(data, (DataSource, Http))
            and item is None
            or isinstance(item, str)
        ):
            msg = (
                "Item is required for Tile Matrix Widget when 'data' "
                "is a DataSource or Http."
            )
            raise ValueError(msg)

        if isinstance(item, str):
            return self.__define_item_type(data=data, column=item)
        if isinstance(item, TileMatrixItem):
            return self.__define_item_type(data=data, column=data.columns[0])

        return TextItem(data_column=data.columns[0])

    def __define_item_type(self, data: pd.DataFrame, column: str) -> TileMatrixItem:
        """Defines item type based on the data."""
        if is_numeric_dtype(data[column]):
            return NumberItem(data_column=column)
        if is_array_like(data[column]):
            return LineChartItem(data_column=column)
        return TextItem(data_column=column)

    def validate(self, data: pd.DataFrame, **_: Any) -> None:
        """Validates widget spec.

        Args:
            data (pd.DataFrame): pandas DataFrame where the data is present.
        """
        self.__item.validate(data=data)

    def _build_widget_input(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            "data": build_data(path=self.dependency_id),
            "item": {self.__item.input_key: self.__item.build()},
            "maxColumns": self.__max_columns,
        }

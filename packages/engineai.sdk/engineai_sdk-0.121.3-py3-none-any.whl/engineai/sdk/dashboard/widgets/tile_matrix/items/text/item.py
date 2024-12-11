"""Spec for Tile Matrix Text Item."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting.text import TextFormatting
from engineai.sdk.dashboard.templated_string import DataField
from engineai.sdk.dashboard.templated_string import TemplatedStringItem

from ..base import BaseTileMatrixItem
from ..typing import Actions
from .typing import TileMatrixTextItemStyling


class TextItem(BaseTileMatrixItem[TileMatrixTextItemStyling]):
    """Spec for Tile Matrix Text Item."""

    _INPUT_KEY = "text"

    @type_check
    def __init__(
        self,
        *,
        data_column: TemplatedStringItem,
        label: Optional[Union[TemplatedStringItem, DataField]] = None,
        icon: Optional[Union[TemplatedStringItem, DataField]] = None,
        link: Optional[Actions] = None,
        formatting: Optional[TextFormatting] = None,
        styling: Optional[TileMatrixTextItemStyling] = None,
    ) -> None:
        """Construct spec for the TileMatrixTextItem class.

        Args:
            data_column: column that has the value to be represented.
            label: Label text to be displayed.
            icon: icon to be displayed.
            link: link or action to be executed in the URL Icon.
            formatting: formatting spec.
            styling: styling spec.

        Examples:
            ??? example "Create a Tile Matrix Widget with a Text Item."
                ```py linenums="1"
                    import pandas as pd
                    from engineai.sdk.dashboard.dashboard import Dashboard
                    from engineai.sdk.dashboard.widgets import tile_matrix

                    data = pd.DataFrame([{"text": ["a", "b", "c", "d", "e"]}])

                    tile_widget = tile_matrix.TileMatrix(
                        data=data, item=tile_matrix.TextItem(data_column="text")
                    )

                    Dashboard(content=tile_widget)
                ```
        """
        super().__init__(
            data_column=data_column,
            label=label,
            icon=icon,
            link=link,
            formatting=formatting or TextFormatting(),
            styling=styling,
        )

    def _build_extra_inputs(self) -> Dict[str, Any]:
        if self._styling is not None:
            return {"styling": self._styling.build_styling()}
        return {}

    def validate(
        self,
        *,
        data: pd.DataFrame,
    ) -> None:
        """Validates Tile Matrix Text Item.

        Args:
            data (Dict): data inside `path`.
        """
        super().validate(
            data=data,
        )
        if self._styling is not None:
            self._styling.validate(
                data=data,
                column_name="value_column",
            )

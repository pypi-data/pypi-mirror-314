"""Spec fot Number Styling Font."""

from typing import Optional

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.styling.color.spec import ColorSpec
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.widgets.components.items.styling.base import BaseItemStyling


class NumberStylingFont(BaseItemStyling):
    """Spec for Number Font Styling class."""

    _INPUT_KEY: str = "font"

    @type_check
    def __init__(
        self,
        *,
        color_spec: ColorSpec,
        data_column: Optional[TemplatedStringItem] = None,
    ) -> None:
        """Construct spec for Number Font Styling.

        Args:
            color_spec (Optional[ColorSpec): specs for color.
            data_column (Optional[TemplatedStringItem]): styling value key.
                Defaults to None.
        """
        super().__init__(data_column=data_column, color_spec=color_spec)

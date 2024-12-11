"""Utils for Table Columns."""

from typing import Any
from typing import Dict
from typing import Union

from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings

from .arrow import ArrowStyling
from .cell import CellStyling
from .color_bar import ColorBarStyling
from .country_flag import CountryFlagStyling
from .dot import DotStyling
from .font import FontStyling
from .icon import IconStyling
from .split_bar import SplitBarStyling

_ColumnStyling = Union[
    ArrowStyling,
    CellStyling,
    ColorBarStyling,
    CountryFlagStyling,
    DotStyling,
    FontStyling,
    IconStyling,
    SplitBarStyling,
]


def build_styling_input(
    data_column: TemplatedStringItem,
    styling: _ColumnStyling,
) -> Dict[str, Any]:
    """Build the styling class."""
    styling_spec = styling.build()
    if not styling_spec["dataKey"]:
        styling_spec["dataKey"] = build_templated_strings(items=data_column)
    return {_get_key(styling): styling_spec}


def _get_key(
    styling: _ColumnStyling,
) -> str:
    if isinstance(styling, CountryFlagStyling):
        key = "flag"
    elif isinstance(styling, FontStyling):
        key = "font"
    elif isinstance(styling, DotStyling):
        key = "dot"
    elif isinstance(styling, CellStyling):
        key = "cell"
    elif isinstance(styling, IconStyling):
        key = "icon"
    elif isinstance(styling, ArrowStyling):
        key = "arrow"
    elif isinstance(styling, ColorBarStyling):
        key = "colorBar"
    elif isinstance(styling, SplitBarStyling):
        key = "splitBar"
    else:
        msg = f"Styling with class {styling.__class__.__name__} not implemented."
        raise NotImplementedError(msg)
    return key

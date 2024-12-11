"""Module that contains operations for widgets that use charts."""

import datetime
from decimal import Decimal
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import pandas as pd

from engineai.sdk.dashboard.widgets.components.charts.tooltip.datetime import (
    DatetimeTooltipItem,
)
from engineai.sdk.dashboard.widgets.components.charts.tooltip.number import (
    NumberTooltipItem,
)
from engineai.sdk.dashboard.widgets.components.charts.tooltip.text import (
    TextTooltipItem,
)
from engineai.sdk.dashboard.widgets.components.charts.typing import TooltipItem

SCALE_THRESHOLD = 0


def get_object_columns_tooltip(
    column_data: pd.Series, column_name: str
) -> Optional[TooltipItem]:
    """Get tooltips item.

    Args:
        column_data: the column that contains data.
        column_name: column name.

    Returns:
        TooltipItem: tooltip item.
    """
    if column_is_of_type(column_data, (int, float, Decimal)):
        return NumberTooltipItem(data_column=str(column_name))
    if column_is_of_type(column_data, (pd.Timestamp, datetime.date)):
        return DatetimeTooltipItem(data_column=str(column_name))
    if column_is_of_type(column_data, (str, int, float, Decimal)):
        return TextTooltipItem(data_column=str(column_name))
    return None


def column_is_of_type(column: pd.Series, _type: Any) -> bool:
    """Check column type.

    Args:
        column: the column that contains data.
        _type: the type to validate.

    Returns:
        bool: return true if it is the corresponding type.
    """
    return bool(column.apply(lambda x: isinstance(x, _type)).all())


def process_scales(data: pd.DataFrame) -> pd.DataFrame:
    """Process the scales of the data."""
    # get the numeric data
    numeric_data = data.select_dtypes(include="number")
    # get scales
    return _define_scale_and_round_values(data=numeric_data)


def calculate_axis_ratios(scales: pd.DataFrame) -> Dict[str, List[str]]:
    """Calculate the ratios between the different scales."""
    # access different scales
    if not scales.empty:
        diff_scales = (
            scales[scales.columns[~(scales.columns.str.endswith("_round"))]]
            .iloc[-1]
            .sort_values(ascending=False)
            .reset_index()
        )

        diff_scales.columns = ["zeros", "scale"]

        return __build_axis_groups(diff_scales=diff_scales)
    return {}


def __build_axis_groups(diff_scales: pd.DataFrame) -> Dict[str, List[str]]:
    groups: Dict[str, List[str]] = {}

    zeros = diff_scales["zeros"].unique().tolist()

    for zero in zeros:
        scale_instance = __get_scale_ratios(diff_scales=diff_scales, zero=zero)

        # Add itself to the group
        groups[zero] = [zero]
        if not scale_instance.empty:
            # Add those that are in the same scale/in the threshold range
            result = scale_instance["zeros"].tolist()
            groups[zero] += result
            # Remove those that are already in a group
            for r in result:
                zeros.remove(r)

    return groups


def __get_scale_ratios(diff_scales: pd.DataFrame, zero: str) -> pd.DataFrame:
    current_scale = diff_scales[diff_scales["zeros"] == zero].iloc[-1].scale
    scale_instance = diff_scales.copy()
    scale_instance["ratio"] = current_scale - diff_scales["scale"]
    return scale_instance[
        (scale_instance["ratio"] >= 0)  # Get all positive ratios
        & (
            scale_instance["ratio"] <= SCALE_THRESHOLD
        )  # Get those that are in the threshold range
        & (scale_instance["zeros"] != zero)  # Remove itself
    ]


compares_dict = {10**i: i for i in range(-10, 11)}


def _get_scale_factor(value: float) -> float:
    """Get divider to scale the number."""
    to_compare = abs(value) if not pd.isna(value) else 1

    tmp = set(compares_dict.keys())
    tmp.add(to_compare)
    tmp = sorted(tmp)

    index = tmp.index(to_compare)

    return compares_dict[tmp[index - 1]]


def _get_category_median_value(*, values: pd.Series) -> float:
    return float(values.dropna().abs().max() if len(values.dropna()) > 0 else 1)


def _define_category_scale(*, data: pd.DataFrame, column: str) -> pd.DataFrame:
    data[column] = _get_scale_factor(
        value=_get_category_median_value(values=data[column])
    )
    data[f"{column.lower().replace(' ', '_')}_round"] = data[column].apply(
        lambda x: 3 if x <= 0 else 1
    )
    return data


def _define_scale_and_round_values(*, data: pd.DataFrame) -> pd.DataFrame:
    result = pd.DataFrame()
    for column in data.columns:
        result = pd.concat(
            [
                result,
                _define_category_scale(
                    data=data[[column]].copy(),
                    column=column,
                ),
            ],
            axis=1,
        )

    return result

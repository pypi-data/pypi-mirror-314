"""Formatting spec for Number Axis."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.formatting import validator
from engineai.sdk.dashboard.formatting.base import BaseNumberFormatting
from engineai.sdk.dashboard.templated_string import DataField
from engineai.sdk.dashboard.templated_string import InternalDataField
from engineai.sdk.dashboard.templated_string import TemplatedStringItem

from .number import NumberScale


class AxisNumberFormatting(BaseNumberFormatting):
    """Numeric axis formatting.

    Description for formatting numeric axis, allowing
    customization of scale, decimal places, prefix, and suffix.
    """

    def __init__(
        self,
        *,
        scale: NumberScale = NumberScale.DYNAMIC_ABSOLUTE,
        decimals: Optional[int] = None,
        prefix: Optional[Union[TemplatedStringItem, DataField]] = None,
        suffix: Optional[Union[TemplatedStringItem, DataField]] = None,
    ) -> None:
        """Constructor for AxisNumberFormatting.

        Args:
            scale (NumberScale): scale used to format number.
                For example, if NumberScale.THOUSAND, number is divided by 1_000
                and a suffix "K" is added.
                Defaults to NumberScale.DYNAMIC_ABSOLUTE (formats K, M, Bn), but
                not percentage or basis point values.
            decimals (Optional[int]): number of decimal places to show after adjusting
                for scale.
                Defaults to 0 if scale is Dynamic Absolute, Millions or Thousands.
                Defaults to 2 for the remaining scales.
            prefix (Optional[Union[TemplatedStringItem, DataField]], optional): Fixed
                text (or key/column data) to be added before axis.
                Defaults to None.
            suffix (Optional[Union[TemplatedStringItem, DataField]], optional): Fixed
                text (or key/column data) to be added after axis.
                Defaults to None.
        """
        super().__init__()
        self.__prefix = InternalDataField(prefix) if prefix else None
        self.__suffix = InternalDataField(suffix) if suffix else None
        self.__scale = scale
        self.__decimals = decimals

    @property
    def decimals(self) -> Optional[int]:
        """Return the decimals value."""
        if self.__decimals is not None:
            return self.__decimals
        if self.__scale == NumberScale.DYNAMIC_ABSOLUTE:
            return None
        if self.__scale in [
            NumberScale.MILLION,
            NumberScale.THOUSAND,
        ]:
            return 0
        return 2

    @decimals.setter
    def decimals(self, decimals: Optional[int]) -> None:
        self.__decimals = decimals

    @property
    def scale(self) -> NumberScale:
        """Return the scale value."""
        return self.__scale

    def validate(self, data: Union[pd.DataFrame, Dict[str, Any]]) -> None:
        """Validate if key or column exists in data.

        Args:
            data (Union[pd.DataFrame, Dict[str, Any]]): pandas DataFrame or dict where
                the data is present.
        """
        validator.validate(data=data, prefix=self.__prefix, suffix=self.__suffix)

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            "scale": self.scale.value,
            "seriesDecimals": self.decimals,
            "prefix": self.__prefix.build() if self.__prefix else None,
            "suffix": self.__suffix.build() if self.__suffix else None,
        }

"""Formatting validator module."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.templated_string import InternalDataField


def validate(
    data: Union[pd.DataFrame, Dict[str, Any]],
    prefix: Optional[InternalDataField] = None,
    suffix: Optional[InternalDataField] = None,
) -> None:
    """Validate if key or column exists in data.

    Args:
        data (Union[pd.DataFrame, Dict[str, Any]]): pandas DataFrame or dict where
            the data is present.
        prefix (Optional[InternalDataField]): Fixed
            text (or key/column data) to be added before axis.
            Defaults to None.
        suffix (Optional[InternalDataField]): Fixed
            text (or key/column data) to be added after axis.
            Defaults to None.
    """
    if prefix is not None:
        prefix.validate(data)
    if suffix is not None:
        suffix.validate(data)

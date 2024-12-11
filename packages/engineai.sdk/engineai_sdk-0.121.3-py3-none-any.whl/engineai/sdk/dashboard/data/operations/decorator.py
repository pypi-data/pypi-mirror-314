"""Specs for operations decorator."""

import functools
from typing import Any
from typing import Callable
from typing import List
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.data.decorator import DataSource
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.interface import OperationInterface as OperationItem


@type_check
def operations(
    data: Optional[Union[pd.DataFrame, DataSource]] = None,
    items: Optional[List[OperationItem]] = None,
) -> Any:
    """Decorator to apply operations to widget data.

    Args:
        data: data to be used by widget. Accepts DataSource as well as raw data.
        items: list of operations to be applied to data.INTERNALERROR
    """
    if isinstance(data, DataSource):
        return DataSource(data.func, *data.args, operations=items, **data.kwargs)

    if isinstance(data, pd.DataFrame):
        return DataSource(data, operations=items)

    def inner_decorator(func: Callable[..., Any]) -> Any:
        @functools.wraps(func)
        def _wrapper(*args: Any, **kwargs: Any) -> DataSource:
            res = func(*args, operations=items, **kwargs)
            return (
                res
                if isinstance(res, DataSource)
                else DataSource(func, *args, operations=items, **kwargs)
            )

        return _wrapper

    return inner_decorator

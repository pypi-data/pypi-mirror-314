"""Specs for Operations typing."""

from typing import Union

from .is_not_null import IsNotNull
from .limit import Limit
from .numeric_condition import NumericCondition
from .order_by import OrderBy

OperationItem = Union[
    Limit,
    OrderBy,
    NumericCondition,
    IsNotNull,
]

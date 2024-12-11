"""Enums for timeseries widget."""

import enum


class TransformChoices(enum.Enum):
    """Options for transforming data within Timeseries legend.

    Below are the various options for transformations of timeseries
    data within a Timeseries widget's legend.

    Attributes:
        CUMSUM: Transform series to the cumulative sum of its values.
        CUMPROD: Transform series to the cumulative product of its values.
        CUMRETURNPROD: Similar to CUMPROD but fixes the initial value as 0. Example
            used is to represent Return on Investment.
        CUMRETURNSUM: Similar to CUMSUM but fixes the initial value as 0. Example
            used is to represent Return on Investment.
        DRAWDOWN: Calculates drawdown based on the series values. Main use is to
            measure the decline of an investment from its peak value to its trough
            value.
        INDEX: Transforms the values to an index where the first value is 100 and the
            rest of the values follow the relative changes of the original data.
        ADD: Adds a scalar to all values in the series.
        SUBTRACT: Subtracts a scalar to all values in the series.
        DIVIDE: Divides a scalar to all values in the series.
        MULTIPLY: Multiplies a scalar to all values in the series.
    """

    CUMSUM = "CUMSUM"
    CUMPROD = "CUMPROD"
    CUMRETURNPROD = "CUMRETURNPROD"
    CUMRETURNSUM = "CUMRETURNSUM"
    DRAWDOWN = "DRAWDOWN"
    INDEX = "INDEX"
    ADD = "ADD"
    SUBTRACT = "SUBTRACT"
    DIVIDE = "DIVIDE"
    MULTIPLY = "MULTIPLY"

"""Spec for legend of a timeseries widget."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links.abstract import AbstractFactoryLinkItemsHandler

from .enums import TransformChoices
from .exceptions import TimeseriesTransformScalarRequiredError


class Transform(AbstractFactoryLinkItemsHandler):
    """Modify data representation in Timeseries with various transformations.

    Define specifications for transforming data within a Timeseries widget
    to modify or enhance the representation of data series. Select from a
    range of transformation choices to apply to the data, such as scaling,
    normalization, or logarithmic transformation, depending on analytical needs.
    """

    @type_check
    def __init__(
        self,
        *,
        transform: TransformChoices,
        scalar: Optional[Union[int, float]] = None,
    ) -> None:
        """Constructor for Transform.

        Args:
            transform: transform to apply to series data.
            scalar: Applies scalar value to data. Only applies when using the
                following transformations ADD, SUBTRACT, DIVIDE and MULTIPLY.
        """
        super().__init__()
        if (
            transform
            in [
                TransformChoices.ADD,
                TransformChoices.DIVIDE,
                TransformChoices.MULTIPLY,
                TransformChoices.SUBTRACT,
            ]
        ) and scalar is None:
            raise TimeseriesTransformScalarRequiredError(transformation=transform.value)

        self._transform = transform
        self._scalar = scalar

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {"transform": self._transform.value, "scalar": self._scalar}

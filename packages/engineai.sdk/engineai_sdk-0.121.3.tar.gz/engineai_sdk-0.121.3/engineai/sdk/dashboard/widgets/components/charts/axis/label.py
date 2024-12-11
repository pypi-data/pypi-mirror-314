"""Spec for label of axis band or line."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.enum.align import HorizontalAlignment
from engineai.sdk.dashboard.enum.align import VerticalAlignment
from engineai.sdk.dashboard.templated_string import DataField
from engineai.sdk.dashboard.templated_string import InternalDataField


class AxisLabel(AbstractFactory):
    """Spec for label of axis band or line."""

    @type_check
    def __init__(
        self,
        *,
        text: Optional[Union[str, DataField]] = None,
        x_position: Union[int, DataField] = -5,
        y_position: Union[int, DataField] = 2,
        horizontal_align: HorizontalAlignment = HorizontalAlignment.CENTER,
        vertical_align: VerticalAlignment = VerticalAlignment.TOP,
        rotation: Optional[Union[float, int]] = -90,
    ) -> None:
        """Construct spec for label of axis band or line.

        Args:
            text: name of column in pandas dataframe(s) used
                for the label text.
            x_position: name of column in pandas
                dataframe(s) used for the x value for the label position.
            y_position: name of column in pandas
                dataframe(s) used for they value for the label position.
            horizontal_align: horizontal alignment spec.
            vertical_align: vertical alignment spec.
            rotation: Rotation of the text label in degrees.
        """
        super().__init__()
        self.__text = InternalDataField(text)
        self.__x_position = InternalDataField(
            str(x_position) if isinstance(x_position, int) else x_position
        )
        self.__y_position = InternalDataField(
            str(y_position) if isinstance(y_position, int) else y_position
        )
        self.__rotation = rotation if rotation else 0
        self.__horizontal_align = horizontal_align
        self.__vertical_align = vertical_align

    def validate(self, data: pd.DataFrame) -> None:
        """Validate if data has the right value to build the label.

        Args:
            data (DataFrame): pandas dataframe which will be used for table.

        Raises:
            ChartNoDataColumnError: if a specific column does not exists in data
        """
        self.__text.validate(data=data)
        self.__x_position.validate(data=data)
        self.__y_position.validate(data=data)

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API.
        """
        return {
            "text": self.__text.build(),
            "xPosition": self.__x_position.build(),
            "yPosition": self.__y_position.build(),
            "rotation": self.__rotation,
            "horizontalAlign": self.__horizontal_align.value,
            "verticalAlign": self.__vertical_align.value,
        }

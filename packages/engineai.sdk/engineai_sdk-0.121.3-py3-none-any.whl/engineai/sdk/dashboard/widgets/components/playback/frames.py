"""Spec for Playback Frame widget."""

from typing import Any
from typing import Dict
from typing import Optional

import pandas as pd

from engineai.sdk.dashboard import formatting
from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting.typing import FormattingType
from engineai.sdk.dashboard.widgets.utils import build_data

from .exceptions import PlaybackItemsValidateNoDataColumnError


class Frames(AbstractFactory):
    """Spec for Playback Frame widget."""

    @type_check
    def __init__(
        self,
        *,
        id_column: str,
        label_column: str,
        label_formatting: Optional[FormattingType] = None,
    ) -> None:
        """Construct spec for Playback Frame widget.

        Args:
            id_column: Id Column to match the field in the Data
                for the Frame.
            label_column: Label Column to match the field in the
                Data for the Frame Label.
            label_formatting: Class to modify the Frame Label
                Formatting.
        """
        super().__init__()
        self.__id_column = id_column
        self.__label_column = label_column
        self.__label_formatting = label_formatting or formatting.TextFormatting()
        self.__dependency_id = " "

    @property
    def id_column(self) -> str:
        """Get Frames id column."""
        return self.__id_column

    def prepare(self, dependency_id: str) -> None:
        """Method for each Widget prepare before building."""
        self.__dependency_id = dependency_id

    def validate(
        self,
        data: pd.DataFrame,
    ) -> None:
        """Validates Frames specs.

        Args:
            data: Data related to Frames.

        Raises:
            PlaybackItemsValidateNoDataColumnError: if id column not found in frames
                column
            PlaybackItemsValidateNoDataColumnError: if label column not found in frames
                column
        """
        if self.__id_column not in data.columns:
            raise PlaybackItemsValidateNoDataColumnError(
                missing_column_name="id_column", missing_column=self.__id_column
            )
        if self.__label_column not in data.columns:
            raise PlaybackItemsValidateNoDataColumnError(
                missing_column_name="label_column", missing_column=self.__label_column
            )

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "idKey": self.__id_column,
            "labelKey": self.__label_column,
            "labelFormatting": self.__label_formatting.build_formatting(),
            "data": build_data(path=self.__dependency_id),
        }

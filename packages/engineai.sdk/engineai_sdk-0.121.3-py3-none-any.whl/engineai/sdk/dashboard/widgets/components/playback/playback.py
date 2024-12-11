"""Spec for a Playback widget."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.data import DataSource
from engineai.sdk.dashboard.data.http import Http
from engineai.sdk.dashboard.data.manager.manager import DependencyManager
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting.typing import FormattingType

from .exceptions import PlaybackNegativeUpdateIntervalError
from .frames import Frames
from .initial_state import InitialState


class Playback(DependencyManager):
    """Spec for Playback widget."""

    _DEPENDENCY_ID: str = "__PLAYBACK_FRAMES_DEPENDENCY__"
    _ID_COUNTER = 0

    @type_check
    def __init__(
        self,
        *,
        id_column: str = "id",
        data: Union[DataSource, pd.DataFrame, Http],
        label_column: Optional[str] = None,
        label_formatting: Optional[FormattingType] = None,
        update_interval: int = 1,
        loop: bool = False,
        auto_play: bool = False,
        initial_state: Optional[InitialState] = None,
    ) -> None:
        """Construct spec for Playback widget.

        Args:
            id_column: Id Column to match the field in the Data
                for the Frame.
            data: data for the widget. Can be a
                pandas dataframe or Storage object if the data is to be retrieved
                from a storage.
            label_column: Label Column to match the field in the
                Data for the Frame Label.
            label_formatting: Class to modify the Frame Label
                Formatting.
            update_interval: Configuration for update interval.
            loop: Configuration for Loop.
            auto_play: Configuration for Auto Play.
            initial_state: Class to add an initial state.
        """
        self.__data_id = self.__generate_id()
        super().__init__(data=data, base_path=self.__data_id)
        if update_interval < 0:
            raise PlaybackNegativeUpdateIntervalError
        self.__frames = Frames(
            id_column=id_column,
            label_column=label_column or id_column,
            label_formatting=label_formatting,
        )
        self.__update_interval = update_interval
        self.__loop = loop
        self.__auto_play = auto_play
        self.__initial_state = initial_state if initial_state else InitialState()

    @property
    def data_id(self) -> str:
        """Returns data id."""
        return self.__data_id

    def __generate_id(self) -> str:
        self._increment_id_counter()
        return f"playback_data_{self._ID_COUNTER}"

    @classmethod
    def _increment_id_counter(cls) -> None:
        cls._ID_COUNTER = cls._ID_COUNTER + 1

    @property
    def id_column(self) -> str:
        """Get Frames id column."""
        return self.__frames.id_column

    def prepare(self) -> None:
        """Method for each Widget prepare before building."""
        self.__frames.prepare(self.dependency_id)

    def validate(self, data: pd.DataFrame, **_: object) -> None:
        """Validate if Playback has all required information.

        Args:
            data (pd.DataFrame): data that is going to be used in frames
        """
        self.__initial_state.validate(id_column=self.id_column, data=data)
        self.__frames.validate(data=data)

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "frames": self.__frames.build(),
            "updateInterval": self.__update_interval * 1000,
            "loop": self.__loop,
            "autoPlay": self.__auto_play,
            "initialState": self.__initial_state.build(),
        }

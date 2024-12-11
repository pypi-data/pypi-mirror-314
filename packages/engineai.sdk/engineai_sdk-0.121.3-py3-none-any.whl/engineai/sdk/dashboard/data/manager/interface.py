"""Interface for dependency manager."""

from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import pandas as pd

StaticDataType = Union[pd.DataFrame, Dict[str, Any]]


class DependencyManagerInterface:
    """Interface for dependency manager."""

    _DEPENDENCY_ID: Optional[str] = None

    @property
    def query_parameter(self) -> str:
        """Query parameter."""
        return ""

    @property
    def dependency_id(self) -> str:
        """Dependency id."""
        if self._DEPENDENCY_ID is None:
            msg = f"Class {self.__class__.__name__}.DEPENDENCY_ID not defined."
            raise NotImplementedError(msg)
        return self._DEPENDENCY_ID

    @property
    @abstractmethod
    def data_id(self) -> str:
        """Returns data id.

        Returns:
            str: data id
        """

    @abstractmethod
    def validate(self, data: StaticDataType, **kwargs: object) -> None:
        """Page routing has no validations to do."""

    def post_process_data(self, data: StaticDataType) -> StaticDataType:
        """Post process data.

        Args:
            data: data to post process

        Returns:
            WidgetDataType: post processed data
        """
        return data

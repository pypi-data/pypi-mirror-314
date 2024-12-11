"""Chart Series Custom Entity."""

from typing import Any
from typing import Dict

from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.charts.series.entities.base import Entity


class CustomEntity(Entity):
    """Custom entity spec."""

    _INPUT_KEY = "standard"

    def __init__(self, name: TemplatedStringItem) -> None:
        """Construct custom entity.

        Args:
            name: name for custom entity.
        """
        super().__init__()
        self.__name = name

    def _build_entity(self) -> Dict[str, Any]:
        return {
            "name": build_templated_strings(items=self.__name),
        }

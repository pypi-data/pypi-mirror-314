"""Selectable layout exceptions."""

from engineai.sdk.dashboard.exceptions import EngineAIDashboardError


class SelectableLayoutError(EngineAIDashboardError):
    """Selectable layout base exception."""

    def __init__(self, selectable_class: str, *args: object) -> None:
        """Selectable layout base exception constructor.

        Args:
            selectable_class (str): selectable item or selectable section class.
        """
        super().__init__(selectable_class, *args)
        self.error_strings.append(f"{selectable_class}")


class SelectableWithDefaultSelectionError(SelectableLayoutError):
    """Selectable section has already a default selection exception."""

    def __init__(self, selectable_class: str, *args: object) -> None:
        """Selectable section has already a default selection exception constructor.

        Args:
            selectable_class (str): selectable section class.
        """
        super().__init__(selectable_class, *args)
        self.error_strings.append("section already has a Default Selection.")


class SelectableDuplicatedLabelError(SelectableLayoutError):
    """Selectable section has duplicated labels exception."""

    def __init__(
        self, selectable_class: str, selectable_item_label: str, *args: object
    ) -> None:
        """Selectable section has duplicated labels exception constructor.

        Args:
            selectable_class (str): selectable section class.
            selectable_item_label (str): selectable item label.
        """
        super().__init__(selectable_class, selectable_item_label, *args)
        self.error_strings.append(
            f"section already has an item with label='{selectable_item_label}'."
        )


class SelectableHasNoItemsError(SelectableLayoutError):
    """Selectable section has no items exception."""

    def __init__(self, selectable_class: str, *args: object) -> None:
        """Selectable section has no items exception constructor.

        Args:
            selectable_class (str): selectable section class.
        """
        super().__init__(selectable_class, *args)
        self.error_strings.append("section does not have items.")

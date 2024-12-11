"""Handle duplicated data paths."""

import ast
from pathlib import Path
from typing import Any
from typing import Optional
from typing import Set
from typing import Tuple


class DuplicatesChecker:
    """Handle duplicated data paths."""

    def __init__(self, duplicated_path: Optional[str] = None) -> None:
        """Constructor for the DuplicatesChecker Class."""
        self.duplicated_file: Optional[Any] = (
            self.__set_duplicated_file(duplicated_path)
            if duplicated_path is not None
            else None
        )
        self.content: Optional[Set[Tuple[str, ...]]] = (
            self.__set_duplicated_content(duplicated_path)
            if duplicated_path is not None
            else None
        )

    def __set_duplicated_file(self, duplicated_path: str) -> Any:
        Path(duplicated_path).parent.mkdir(parents=True, exist_ok=True)
        Path(duplicated_path).touch(exist_ok=True)
        return open(duplicated_path, "a+", encoding="utf-8")  # noqa

    def __set_duplicated_content(
        self,
        duplicated_path: str,
    ) -> Set[Tuple[str, ...]]:
        with open(duplicated_path, encoding="utf-8") as file:
            info = file.read().splitlines()
            return {ast.literal_eval(line) for line in info}

    def write(self, final_path: Optional[Tuple[str, ...]] = None) -> None:
        """Write duplicated path."""
        if final_path is not None and self.duplicated_file is not None:
            self.duplicated_file.write(str(final_path) + "\n")

    def close(self) -> None:
        """Close duplicated file."""
        if self.duplicated_file is not None:
            self.duplicated_file.close()

"""Spec for a file handler that will store the keys of the widgets options in a file."""

import atexit
import shutil
from pathlib import Path
from typing import Any
from typing import Iterable
from typing import Set

import pandas as pd

_TEMP_DIR = ".tmpkeys"
_KEYS_DIR = "keys"
_METADATA_DIR = "metadata"
_SPECIAL_CHAR = "@"


def close() -> None:
    """Close filesystem."""
    if Path.exists(Path(_TEMP_DIR)):
        shutil.rmtree(_TEMP_DIR)


class IOWriter:
    """Class that stores the keys of the widgets options in a file."""

    def __init__(self, path: str, write_keys: bool, separator: str = "/") -> None:
        """Constructor for the DataKeysWriter Class."""
        self.__keys_path = Path(_TEMP_DIR) / Path(_KEYS_DIR)
        self.__metadata_path = Path(_TEMP_DIR) / Path(_METADATA_DIR)
        self.__keys_path.mkdir(parents=True, exist_ok=True)
        self.__metadata_path.mkdir(parents=True, exist_ok=True)
        self.__fs: Any
        self.__separator = separator
        self.__write_keys = write_keys
        self.__path = self.__keys_path / _process_path(path, separator)

    def __enter__(self) -> "IOWriter":
        if self.__write_keys:
            self.__fs = open(self.__path, "a+", encoding="utf-8")
        return self

    def write_key(self, data: Any) -> None:
        """Write an option key in the file."""
        if self.__write_keys:
            line = ""

            if data is not None:
                try:
                    line = f"{''.join(tuple(map(str, *data)))}"
                except TypeError:
                    line = f"{f'{self.__separator}'.join(tuple(map(str, data)))}"

                self.__fs.write(f"{line}\n")

    def write_metadata(self, data: pd.DataFrame, metadata: Set[str], path: str) -> None:
        """Write the metadata of the widgets options in a file."""
        if len(metadata) > 0:
            try:
                (Path(self.__metadata_path) / Path(path)).parent.mkdir(
                    parents=True, exist_ok=True
                )
                data[list(metadata)].to_json(self.__metadata_path / f"{path}.json")
            except Exception as exc:
                msg = (
                    "All metadata columns were"
                    f" not found in data: {metadata=} , {data.columns=}"
                )
                raise ValueError(msg) from exc

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:  # noqa
        if self.__write_keys:
            self.__fs.close()


class IOReader:
    """Class that reads the keys of the widgets options from a file."""

    @staticmethod
    def keys(path: str, separator: str = "/") -> Iterable[str]:
        """Get the keys from the file."""
        if separator != path[-1]:
            yield path
        else:
            p = Path(_TEMP_DIR) / _KEYS_DIR / _process_path(path, separator)
            with open(p, encoding="utf-8") as fs:
                for line in iter(fs.readline, ""):
                    yield path + line.strip()

    @staticmethod
    def read_metadata(path: str) -> pd.DataFrame:
        """Read the metadata of the widgets options from a file."""
        p = Path(_TEMP_DIR) / _METADATA_DIR / f"{path}.json"
        try:
            return pd.read_json(p, dtype=False)
        except Exception as exc:
            msg = f"Metadata not found for {p}"
            raise KeyError(msg) from exc


def _process_path(path: str, separator: str = "/") -> str:
    p = path if not path.endswith(separator) else path[:-1]
    return f"{p.replace(separator, _SPECIAL_CHAR)}.txt"


atexit.register(close)

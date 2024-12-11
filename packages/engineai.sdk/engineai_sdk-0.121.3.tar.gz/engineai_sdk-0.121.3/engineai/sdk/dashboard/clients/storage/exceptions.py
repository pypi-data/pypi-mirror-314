"""Exceptions for the Storage."""

from typing import Optional


class StorageError(Exception):
    """Raised when an error occurs in the Storage."""

    def __init__(self, path: str, status_code: Optional[int] = None) -> None:
        """Constructor for StorageError exception."""
        message = f"Storage error at {path}."
        if status_code is not None:
            message = message[:-1] + f" with status code {status_code}."
        super().__init__(message)

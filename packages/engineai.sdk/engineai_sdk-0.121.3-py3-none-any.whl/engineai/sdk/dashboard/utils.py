"""Base Package Utils."""

import sys
import threading
from urllib.parse import urlparse
from uuid import UUID


def is_uuid(uuid_str: str, version: int = 4) -> bool:
    """Validates if uuid_str is a valid uuid within a certain version.

    Args:
        uuid_str (str): uuid string.
        version (int, optional): uuid version of uuid_str.

    Returns:
        bool: whether uuid_str is a uuid or not.
    """
    try:
        uuid_obj = UUID(uuid_str, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_str


def _validate_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def is_valid_url(url: str) -> None:
    """Check if the url is valid."""
    if not _validate_url(url):
        msg = f"Invalid URL: {url}"
        raise ValueError(msg)


class ProgressBar:
    """Class that handles a custom progress bar."""

    def __init__(self, total: int = -1, length: int = 50) -> None:
        """Constructor for ProgressBar."""
        self.total = total
        self.length = length
        self.lock = threading.Lock()
        self.counter = 0

    def write(self, message: str, flush: bool = True) -> None:
        """Write a message to stdout."""
        with self.lock:
            sys.stdout.write(f"\n{message}\n\n")
            if flush:
                sys.stdout.flush()

    def update(self) -> None:
        """Iterates the progress bar."""
        self.counter += 1
        progress = self.counter / self.total
        with self.lock:
            bar_format = (
                "\nProgress: [{:<" + str(self.length) + "}] {}%  Data Sources: {}/{}"
            )
            bar_output = bar_format.format(
                "=" * int(self.length * progress),
                int(progress * 100),
                self.counter,
                self.total,
            )
            sys.stdout.write("\r" + bar_output)
            sys.stdout.flush()

    def finish(self, message: str = "Done!") -> None:
        """Writes the final message to stdout."""
        with self.lock:
            sys.stdout.flush()
            sys.stdout.write(f"{message}\n")

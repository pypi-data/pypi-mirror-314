"""Custom ThreadPoolExecutor class that has an exceptions handler."""

import concurrent.futures
import contextvars
import logging
from threading import Lock
from typing import Any
from typing import Optional

logger = logging.getLogger(__name__)


class ThreadExecutor(concurrent.futures.ThreadPoolExecutor):
    """Custom ThreadPoolExecutor class that has an exceptions handler."""

    def __init__(self, max_workers: Optional[int] = None) -> None:
        """Initializes a new ThreadPoolExecutor instance.

        Args:
            max_workers: The maximum number of threads that can be used to
                execute the given calls.
        """
        self.parent_ctx = contextvars.copy_context()

        super().__init__(
            initializer=self._set_context,
            max_workers=max_workers,
            thread_name_prefix="engineai-sdk",
        )
        self._future_to_func = {}
        self._cancelled: Optional[Exception] = None
        self._cancellation_lock = Lock()

    @property
    def cancelled(self) -> Optional[Exception]:
        """Check if executor was cancelled."""
        return self._cancelled

    def _set_context(self) -> None:
        for var, value in self.parent_ctx.items():
            var.set(value)

    def submit(self, fn: Any, *args: Any, **kwargs: Any) -> concurrent.futures.Future:
        """Override submit method to add a callback to check for exceptions."""
        future = super().submit(fn, *args, **kwargs)
        self._future_to_func[future] = fn  # Store a reference to the submitted function
        future.add_done_callback(self._check_exceptions)
        return future

    def _check_exceptions(self, future: concurrent.futures.Future) -> None:
        if self._cancelled:
            return
        if future.exception():
            with self._cancellation_lock:
                self._cancelled = future.exception()
            failed_func = self._future_to_func[future]
            logger.info(
                "Task %s failed. Cancelling remaining tasks.",
                failed_func.__name__,
            )
            for f in self._future_to_func:
                if not f.done():
                    f.cancel()
            del self._future_to_func  # Clear the dictionary to release references

    def __exit__(self, exc_type, exc_val, exc_tb) -> Optional[bool]:  # noqa
        super().__exit__(exc_type, exc_val, exc_tb)
        if self.cancelled is not None:
            raise self.cancelled
        return False

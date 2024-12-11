"""Options for Dashboard storage type."""

import enum
from typing import Type

from engineai.sdk.dashboard.dependencies.datastore import DashboardBlobStorage
from engineai.sdk.dashboard.dependencies.datastore import DashboardFileShareStorage
from engineai.sdk.dashboard.dependencies.datastore import DashboardStorage


class StorageType(enum.Enum):
    """Options for Dashboard storage type."""

    BLOB = "azure-blob-storage"
    FILE_SHARE = "azure-file-share-storage"

    @classmethod
    def get_storage_class(cls, storage_type: str) -> Type[DashboardStorage]:
        """Returns the storage class based on storage type.

        Args:
            storage_type (str): Storage type

        Returns:
            Type[DashboardStorage]: Storage class
        """
        if storage_type == cls.BLOB.value:
            return DashboardBlobStorage
        if storage_type == cls.FILE_SHARE.value:
            return DashboardFileShareStorage
        msg = f"Storage type {storage_type} not implemented."
        raise NotImplementedError(msg)

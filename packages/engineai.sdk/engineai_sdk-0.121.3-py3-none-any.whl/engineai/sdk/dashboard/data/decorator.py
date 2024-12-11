"""Data Decorator Module."""

import functools
import inspect
import itertools
import logging
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Union
from typing import cast

import pandas as pd

from engineai.sdk.dashboard.clients.storage import Storage
from engineai.sdk.dashboard.clients.storage import StorageConfig
from engineai.sdk.dashboard.config import SKIP_DATA_VALIDATION
from engineai.sdk.dashboard.data.exceptions import DataProcessError
from engineai.sdk.dashboard.data.exceptions import DataRouteWithArgumentsError
from engineai.sdk.dashboard.data.exceptions import DataValidationError
from engineai.sdk.dashboard.exceptions import BaseDataValidationError
from engineai.sdk.dashboard.interface import OperationInterface as OperationItem
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.links.typing import GenericLink

from .duplicated import DuplicatesChecker
from .enums import StorageType
from .io_handler import IOReader
from .io_handler import IOWriter
from .manager.interface import DependencyManagerInterface as DependencyManager
from .manager.interface import StaticDataType

Func = Callable[..., StaticDataType]

logger = logging.getLogger(__name__)


class DataSource:
    """Decorator Class that stores data in the Dashboard Storage."""

    def __init__(
        self,
        func: Union[Func, StaticDataType],
        *args: GenericLink,
        operations: Optional[List[OperationItem]] = None,
        base_path: Optional[str] = None,
        storage_type: Optional[StorageType] = None,
        **kwargs: Any,
    ) -> None:
        """Decorator Class that stores data in the Dashboard Storage."""
        self.func: Func = (
            cast(Func, (lambda: func))
            if isinstance(func, (pd.DataFrame, Dict))
            else func
        )

        self.args: Tuple[GenericLink, ...] = args
        self.__base_path = (
            base_path
            if base_path is not None
            else f"{self.func.__module__}.{self.func.__name__}".replace(".", "/")
        )
        self.__separator = "/"
        self.__storage_type = storage_type
        self.kwargs: Dict[str, Any] = kwargs
        self.__operations: Optional[List[OperationItem]] = operations
        self.__component: DependencyManager

    @property
    def component(self) -> DependencyManager:
        """Component."""
        return self.__component

    @component.setter
    def component(self, component: DependencyManager) -> None:
        """Set component."""
        self.__component = component

    @property
    def storage_type(self) -> StorageType:
        """Storage type."""
        if self.__storage_type is None:
            msg = "Storage type not defined."
            raise NotImplementedError(msg)
        return self.__storage_type

    @storage_type.setter
    def storage_type(self, storage_type: StorageType) -> None:
        """Set storage type."""
        if self.__storage_type is None:
            self.__storage_type = storage_type

    @property
    def operations(self) -> Optional[List[OperationItem]]:
        """Get Operations."""
        return self.__operations

    def __validate_route_args(self, component: Any) -> None:
        if component.data_id == "route" and self.args:
            raise DataRouteWithArgumentsError

    def __check_http_dependencies(self) -> None:
        if len(self.args) > 0 and any("http" in repr(arg) for arg in self.args):
            raise DataProcessError(
                data_id=self.component.data_id,
                class_name=self.component.__class__.__name__,
                error_string="Currently, HTTP dependencies are not supported "
                "as data source's inputs.",
                function_name=self.func.__name__,
                options=None,
                function_arguments=self.func_args,
            )

    @classmethod
    def decorator(
        cls,
        _func: Optional[Func] = None,
        *,
        storage_type: Optional[StorageType] = None,
    ) -> Any:
        """Decorator to store data in the Dashboard Storage. Call as @data_source.

        Args:
            _func: Function to be decorated.
            storage_type: Storage type to use. This will override the storage
                type parameter, defined in dashboard instance.
        """

        def inner_decorator(func: Func) -> "Any":
            @functools.wraps(func)
            def wrapper(*args: GenericLink, **kwargs: Any) -> "DataSource":
                return cls(
                    func,
                    *args,
                    storage_type=storage_type,
                    **kwargs,
                )

            return wrapper

        if _func is None:
            return inner_decorator
        return inner_decorator(_func)

    @property
    def base_path(self) -> str:
        """Returns the base path of the data."""
        return self.__base_path

    @property
    def separator(self) -> str:
        """Returns the separator of the data."""
        return self.__separator

    @property
    def func_args(self) -> List[Any]:
        """Returns data source signature."""
        return list(
            filter(
                lambda x: x if "*" not in str(x) else None,
                list(inspect.signature(self.func).parameters.values()),
            )
        )

    def __call__(
        self,
        storage_config: StorageConfig,
        write_keys: bool,
        metadata: Set[str],
        duplicated_path: Optional[str] = None,
    ) -> None:
        """Stores the data in the storage."""
        storage = Storage(
            base_path=storage_config.base_path,
        )
        try:
            self.__validate_route_args(self.component)
            self.__check_http_dependencies()
            self.__store_data(
                storage=storage,
                write_keys=write_keys,
                function_name=self.__base_path,
                metadata=metadata,
                duplicated_path=duplicated_path,
            )
        finally:
            storage.close()

    def __store_data(
        self,
        storage: Storage,
        write_keys: bool,
        function_name: Optional[str],
        metadata: Set[str],
        duplicated_path: Optional[str] = None,
    ) -> None:
        all_options = self.get_args_data() if self.args else iter([None])
        duplicated = DuplicatesChecker(duplicated_path=duplicated_path)
        with IOWriter(self.__base_path, write_keys=write_keys) as writer:
            for options in all_options:
                try:
                    options_data = options if options else None
                    if duplicated.content is not None:
                        if options_data in duplicated.content:
                            continue
                        duplicated.write(options_data)
                    data = (
                        self.func(*options_data, **self.kwargs)
                        if options_data is not None
                        else self.func(**self.kwargs)
                    )
                except BaseException as error:
                    raise DataProcessError(
                        data_id=self.component.data_id,
                        class_name=self.component.__class__.__name__,
                        error_string=str(error),
                        function_name=function_name,
                        options=options,
                        function_arguments=self.func_args,
                    ) from error

                if self.component.data_id == "route":
                    self.__validate_and_store_route_data(
                        storage=storage,
                        data=data,
                        function_name=function_name,
                        writer=writer,
                    )
                else:
                    self.__validate_and_store_remaining_data(
                        storage=storage,
                        data=data,
                        options=options_data,
                        function_name=function_name,
                        writer=writer,
                    )
                    writer.write_metadata(
                        cast(pd.DataFrame, data),
                        metadata,
                        self._resolve_path(options_data),
                    )
            duplicated.close()

    def __validate_and_store_route_data(
        self,
        storage: Storage,
        data: StaticDataType,
        writer: IOWriter,
        function_name: Optional[str] = None,
    ) -> None:
        data_to_numpy = (df := cast(pd.DataFrame, data))[
            self.component.query_parameter
        ].to_numpy()
        for index in range(len(data_to_numpy)):
            route_options = [data_to_numpy[index]]
            self.__validate_and_store_remaining_data(
                storage=storage,
                data=df.iloc[index].to_frame().T,
                options=route_options,
                function_name=function_name,
                writer=writer,
            )

    def __validate_and_store_remaining_data(
        self,
        storage: Storage,
        data: StaticDataType,
        options: Any,
        writer: IOWriter,
        function_name: Optional[str] = None,
    ) -> None:
        self._validate_and_store(
            storage=storage,
            data=data,
            options=options,
            function_name=function_name,
        )
        writer.write_key(options)

    def get_args_data(self) -> Iterable[Tuple[str, ...]]:
        """Merge the arguments with the data."""
        paths = self._resolve_paths()
        yield from itertools.product(
            *(
                self._get_data(
                    arg=arg,
                    field=self.args[i].field,
                )
                for i, arg in enumerate(paths)
            )
        )

    def _resolve_paths(self) -> List[Tuple[str, GenericLink]]:
        """Get paths from the arguments."""
        return [self._get_arg_path(arg) for arg in self.args] if self.args else []

    def _get_arg_path(self, arg: Any) -> Tuple[str, GenericLink]:
        separator = (
            self.__separator
            if not isinstance(arg, WidgetField)
            or any(d.args for d in arg.link_component.data)
            else ""
        )
        return (
            f"{next(iter(arg.link_component.data)).base_path}{separator}",
            arg.link_component,
        )

    def _get_data(self, arg: Tuple[str, GenericLink], field: str) -> Iterable[Any]:
        """Get data from the storage, based on the path inserted."""
        path, component = arg
        logger.debug("Get DATA path: '%s'.", path)

        for key in IOReader.keys(path, self.separator):
            if component.data_id != "route":
                values = IOReader.read_metadata(key)
                yield from values[field].tolist()
            else:
                yield key.replace(path, "")

        logger.debug("Finished get data.")

    def __skip_validation(self) -> bool:
        return SKIP_DATA_VALIDATION or (
            any(operation.force_skip_validation for operation in self.operations)
            if self.operations is not None
            else False
        )

    def _validate_and_store(
        self,
        storage: Storage,
        data: StaticDataType,
        options: Optional[List[str]],
        function_name: Optional[str],
    ) -> None:
        if data is not None:  # Button use case
            if not self.__skip_validation():
                try:
                    self.component.validate(data, storage=storage)
                except BaseDataValidationError as error:
                    raise DataValidationError(
                        data=data,
                        data_id=self.component.data_id,
                        class_name=self.component.__class__.__name__,
                        error_string=str(error),
                        function_name=function_name,
                        options=options,
                    ) from error

            path = self._resolve_path(options)
            storage[f"{self.storage_type.value}/{path}"] = (
                self.component.post_process_data(data)
            )

    def _resolve_path(
        self,
        options: Optional[List[str]],
    ) -> str:
        if self.__base_path == options:
            return self.__base_path

        return (
            f"{self.__base_path}/"
            f"{f'{self.__separator}'.join(tuple(map(str, options)))}"
            if options
            else self.__base_path
        )


data_source = DataSource.decorator

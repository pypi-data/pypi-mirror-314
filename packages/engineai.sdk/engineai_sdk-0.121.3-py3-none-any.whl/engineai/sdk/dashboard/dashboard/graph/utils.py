"""Auxiliary functions for the graph module."""

import concurrent.futures
import itertools
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Set
from typing import Tuple
from typing import Union

from engineai.sdk.dashboard.clients.storage import StorageConfig
from engineai.sdk.dashboard.data import DataSource
from engineai.sdk.dashboard.data.enums import StorageType
from engineai.sdk.dashboard.interface import WidgetInterface as Widget

from .node import Node


def group_data(widgets: List[List[Widget]]) -> Dict[str, Set[Node]]:
    """Picks every widget in the dashboard and groups them by base_path.

    Every time a duplicated widget is found, it will be added to the same set.
    """
    result: Dict[str, Set[Node]] = {}
    for data_source in __get_data_sources(widgets):
        if isinstance(data_source, DataSource) and all(
            not arg.link_component.has_http_data for arg in data_source.args
        ):
            result.setdefault(data_source.base_path, set()).add(
                Node(data_source.base_path, data_source)
            )
    return result


def __get_data_sources(widgets: List[List[Widget]]) -> Iterable[Any]:
    return itertools.chain.from_iterable(
        widget.data for widget in itertools.chain(*widgets)
    )


def store_data_source(
    data_sources: Union[DataSource, Set[DataSource]],
    storage_config: StorageConfig,
    write_keys: bool,
    metadata: Set[str],
    storage_type: StorageType,
) -> None:
    """Executor function that stores the data from a data source."""
    if isinstance(data_sources, set):
        base_path = next(iter(data_sources)).base_path
        for data_source in data_sources:
            data_source.storage_type = storage_type
            data_source(
                storage_config=storage_config,
                write_keys=write_keys,
                metadata=metadata,
                duplicated_path=f"graph/{base_path}.txt",
            )
    else:
        data_sources.storage_type = storage_type
        data_sources(
            storage_config=storage_config,
            write_keys=write_keys,
            metadata=metadata,
            duplicated_path=None,
        )


def process_dependencies(
    node: str,
    pred: Any,
    blocked: List[str],
    futures: Dict[str, concurrent.futures.Future],
) -> Tuple[List[Any], List[str]]:
    """Auxiliary function that based on a specific node.

    Checks if its predecessors status.
    """
    dependencies: List[Any] = []
    for dependency in pred:
        if dependency in blocked:
            blocked.append(node)
            break
        dependencies.append(futures[dependency])
    return dependencies, blocked

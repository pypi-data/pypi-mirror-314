"""Specs for Dependencies Graph."""

import atexit
import concurrent.futures
import itertools
import logging
import shutil
from pathlib import Path
from typing import Dict
from typing import Iterable
from typing import List
from typing import Set
from typing import Tuple
from typing import Union

import networkx as nx
from typing_extensions import Unpack

from engineai.sdk.dashboard.abstract.typing import PrepareParams
from engineai.sdk.dashboard.config import TOTAL_WORKERS
from engineai.sdk.dashboard.dashboard.page.route import Route
from engineai.sdk.dashboard.data import DataSource
from engineai.sdk.dashboard.interface import WidgetInterface as Widget
from engineai.sdk.dashboard.links.typing import GenericLink
from engineai.sdk.dashboard.utils import ProgressBar

from .executor_config import ThreadExecutor
from .node import Node
from .utils import group_data
from .utils import process_dependencies
from .utils import store_data_source

logger = logging.getLogger(__name__)


class Graph:
    """Dependencies graph that will be used to manage the store process."""

    def __init__(
        self,
        widgets: List[List[Widget]],
        routes: List[Union[Route, None]],
        **kwargs: Unpack[PrepareParams],
    ) -> None:
        """Constructor for dependencies graph."""
        self.__instance: nx.Graph = nx.DiGraph()
        self.__add_nodes(data=group_data(widgets), routes=routes)
        self.__store_data(**kwargs)

    def __add_nodes(
        self, data: Dict[str, Set[Node]], routes: List[Union[Route, None]]
    ) -> None:
        self.__add_route_nodes(routes)
        self.__add_data_nodes(data)
        self.__get_metadata()

    def __add_route_nodes(self, routes: List[Union[Route, None]]) -> None:
        for route in set(
            filter(lambda x: x is not None and not x.has_http_data, routes)
        ):
            for data_source in route.data:
                self.__instance.add_node(
                    data_source.base_path,
                    nodes={
                        (
                            node := Node(
                                data_source.base_path,
                                data_source,
                            )
                        )
                    },
                    metadata=node.links,
                    fields=set(),
                )

    def __add_data_nodes(self, data: Dict[str, Set[Node]]) -> None:
        for base_path, nodes in data.items():
            node = next(iter(nodes))
            self.__instance.add_node(
                base_path,
                nodes=nodes,
                metadata=set(itertools.chain(*[n.links for n in nodes])),
                fields=set(),
            )
            for element in nodes:
                self.__add_edges(
                    element.data_source.args,
                    base_path,
                    node.data_source,
                )
                self.__add_edges(
                    element.data_source.component.widget_fields,
                    base_path,
                    node.data_source,
                )

    def __add_edges(
        self,
        dependencies: Iterable[GenericLink],
        base_path: str,
        data_source: DataSource,
    ) -> None:
        for dependency in dependencies:
            for dep_data_source in dependency.link_component.data:
                self.__add_data_source_edge(base_path, data_source, dep_data_source)

    def __add_data_source_edge(
        self,
        base_path: str,
        data_source: DataSource,
        dep_data_source: DataSource,
    ) -> None:
        self.__exists_in_graph(Node(dep_data_source.base_path, dep_data_source))
        self.__exists_in_graph(Node(base_path, data_source))
        self.__instance.add_edge(dep_data_source.base_path, base_path)

    def __exists_in_graph(self, node: Node) -> None:
        if node.name not in self.__instance.nodes:
            self.__instance.add_node(
                node.name, nodes={node}, metadata=node.links, fields=set()
            )
        else:
            self.__instance.nodes[node.name]["nodes"].add(node)
            self.__instance.nodes[node.name]["metadata"].union(node.links)

    def __get_metadata(self) -> None:
        """Gets metadata for each node."""
        instance_copy = self.__instance.copy()
        for node in nx.topological_sort(self.__instance):
            current_node = next(iter(self.__instance.nodes[node]["nodes"]))
            for successor in self.__instance.successors(node):
                for link in self.__instance.nodes[successor]["metadata"]:
                    if current_node.data_source == next(iter(link.link_component.data)):
                        instance_copy.nodes[node]["fields"].add(link.field)
        self.__instance = instance_copy

    def __store_data(self, **kwargs: Unpack[PrepareParams]) -> None:
        """Stores items data."""
        futures: Dict[str, concurrent.futures.Future] = {}
        completed: Set[str] = set()
        instance_copy = self.__instance.copy()

        pbar = ProgressBar(len(self.__instance), length=20)

        with ThreadExecutor(max_workers=TOTAL_WORKERS) as executor:
            while len(completed) != len(self.__instance):
                if executor.cancelled:
                    raise executor.cancelled
                blocked: List[str] = []
                for node in nx.topological_sort(instance_copy):
                    if executor.cancelled:
                        break
                    pred = self.__instance.predecessors(node)
                    dependencies, blocked = process_dependencies(
                        node, pred, blocked, futures
                    )

                    if node in blocked:
                        continue

                    _, not_done = concurrent.futures.wait(
                        dependencies,
                        return_when=concurrent.futures.FIRST_COMPLETED,
                    )

                    if len(not_done) > 0:
                        blocked.append(node)
                        continue

                    if executor.cancelled:
                        break

                    (
                        completed,
                        futures,
                    ) = self.__handle_next_running_node(
                        node,
                        completed,
                        futures,
                        executor,
                        pbar,
                        **kwargs,
                    )

                instance_copy.remove_nodes_from(completed)

    def __handle_next_running_node(
        self,
        node: str,
        completed: Set[str],
        futures: Dict[str, concurrent.futures.Future],
        executor: ThreadExecutor,
        pbar: ProgressBar,
        **kwargs: Unpack[PrepareParams],
    ) -> Tuple[Set[str], Dict[str, concurrent.futures.Future]]:
        if futures.get(node) is None:
            completed.add(node)
            future = self.__create_future(
                executor=executor,
                node=node,
                pbar=pbar,
                **kwargs,
            )
            futures[node] = future

        return completed, futures

    def __create_future(
        self,
        executor: ThreadExecutor,
        node: str,
        pbar: ProgressBar,
        **kwargs: Unpack[PrepareParams],
    ) -> concurrent.futures.Future:
        nodes = self.__instance.nodes[node]["nodes"]

        data_sources, write_keys = self.__prepare_future_info(nodes)

        future = executor.submit(
            store_data_source,
            data_sources=data_sources,
            storage_config=kwargs["storage"],
            write_keys=write_keys,
            metadata=self.__instance.nodes[node]["fields"],
            storage_type=kwargs["storage_type"],
        )
        future.add_done_callback(lambda _: pbar.update())
        return future

    def __prepare_future_info(
        self, nodes: Set[Node]
    ) -> Tuple[Union[DataSource, Set[DataSource]], bool]:
        data_sources = (
            next(iter(nodes)).data_source
            if len(nodes) == 1
            else {n.data_source for n in nodes}
        )

        graph_key = next(iter(nodes)).name

        write_keys = len(self.__instance.out_edges(graph_key)) > 0

        return data_sources, write_keys


def close() -> None:
    """Close filesystem."""
    if Path.exists(Path("graph")):
        shutil.rmtree("graph")


atexit.register(close)

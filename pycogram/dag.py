# -*- coding: utf-8 -*-
"""
Single-source shortest path algorithm for directed acyclic graphs.
"""

import math
from collections import deque

def dag(graph, source):
    """
    Given a directed acyclic graph(DAG) and a source within the graph,
    find shortest paths and distances for all nodes.

    Parameters
    ----------
    - graph: Graph
        a DAG graph.
    - source: node
        a hashable object representing the source in graph.

    Returns
    -------
    - dist: dict
        shortest distance to source for each node.
    - prev: dict
        last node on the shortest path for each node.

    Raises
    ------
    - ValueError
        if source is not in graph, or graph is cyclic.

    Reference
    ---------
    - https://en.wikipedia.org/wiki/Directed_acyclic_graph#Path_algorithms
    - Cormen T H. Introduction to algorithms[M]. MIT press, 2009.
    """

    if source not in graph.nodes:
        raise ValueError('The given source {} is not in the graph.'.format(source))
    if graph.is_cyclic:
        raise ValueError('The graph is cyclic.')

    unvisited_nodes = graph.nodes
    sorted_nodes = deque()
    dist = {}
    prev = {}

    def _visit(node):
        """
        visit a node in the DFS search.
        """
        unvisited_nodes.remove(node)
        for adj_node in graph.adjacent_nodes_of(node):
            if adj_node in unvisited_nodes:
                _visit(adj_node)
        sorted_nodes.appendleft(node)

    for node in graph.nodes:
        if node in unvisited_nodes:
            _visit(node)

    for node in sorted_nodes:
        dist[node] = math.inf
        prev[node] = None
    dist[source] = 0

    while sorted_nodes:
        next_node = sorted_nodes.popleft()
        for adj_node in graph.adjacent_nodes_of(next_node):
            new_dist = dist[next_node] + graph.get_weight(next_node, adj_node)
            if new_dist < dist[adj_node]:
                dist[adj_node] = new_dist
                prev[adj_node] = next_node

    return dist, prev

# -*- coding: utf-8 -*-
"""
Single-source shortest path algorithm for non-negative graphs.
"""

import math

def dijkstra(graph, source):
    """
    Given a graph and a source within the graph,
    find shortest paths and distances for all nodes.
    The edges in the graph must be non-negative.

    Parameters
    ----------
    - graph: Graph
        a non-negative graph.
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
        if source is not in graph or negative edge exists.

    Reference
    ---------
    - https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#pseudocode
    - Cormen T H. Introduction to algorithms[M]. MIT press, 2009.
    """
    if source not in graph.nodes:
        raise ValueError('The given source {} is not in the graph.'.format(source))
    if not graph.is_nonnegative:
        raise ValueError('There are non-positive edges in the graph.')

    unvisited_nodes = graph.nodes
    dist = {}
    prev = {}

    for node in graph.nodes:
        dist[node] = math.inf
        prev[node] = None
    dist[source] = 0

    while unvisited_nodes:
        min_node = min(unvisited_nodes, key=(lambda x: dist[x]))
        unvisited_nodes.remove(min_node)

        for adj_node in graph.adjacent_nodes_of(min_node):
            new_dist = dist[min_node] + graph.get_weight(min_node, adj_node)
            if new_dist < dist[adj_node]:
                dist[adj_node] = new_dist
                prev[adj_node] = min_node

    return dist, prev

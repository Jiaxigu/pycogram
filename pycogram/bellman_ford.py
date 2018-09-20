# -*- coding: utf-8 -*-
"""
A versatile but not-so-efficient single-source shortest path algorithm for graphs.
"""

import math

def bellman_ford(graph, source):
    """
    Given a graph and a source within the graph,
    find shortest paths and distances for all nodes.
    No negative-weight circles are allowed.

    Parameters
    ----------
    - graph: Graph
        a graph which should not contain any negative-weight circles.
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
        if graph contains any negative-weight circle.

    Reference
    ---------
    - https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm#Algorithm
    - Cormen T H. Introduction to algorithms[M]. MIT press, 2009.
    """
    if source not in graph.nodes:
        raise ValueError('The given source {} is not in the graph.'.format(source))

    dist = {}
    prev = {}

    for node in graph.nodes:
        dist[node] = math.inf
        prev[node] = None
    dist[source] = 0
    
    for i in range(1, 6):
        for node in graph.nodes:
            for adj_node in graph.adjacent_nodes_of(node):
                new_dist = dist[node] + graph.get_weight(node, adj_node)
                if new_dist < dist[adj_node]:
                    dist[adj_node] = new_dist
                    prev[adj_node] = node
    
    for node in graph.nodes:
        for adj_node in graph.adjacent_nodes_of(node):
            if dist[adj_node] > dist[node] + graph.get_weight(node, adj_node):
                raise ValueError('Negative-weight circle is detected between {} and {}.'.format(node, adj_node))

    return dist, prev

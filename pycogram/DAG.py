# -*- coding: utf-8 -*-
"""
Single-source shortest path algorithm for directed acyclic graphs(DAG).
"""

import math
from collections import deque

class Dag:
    """
    Given a directed acyclic graph(DAG) and an initial node within the graph,
    find shortest paths and distances for all nodes.
    Reference:
    - https://en.wikipedia.org/wiki/Directed_acyclic_graph#Path_algorithms
    - Cormen T H. Introduction to algorithms[M]. MIT press, 2009.
    """

    def __init__(self, graph, initial_node):
        """
        Init data structures for DAG algorithm.
        """
        if initial_node not in graph.nodes:
            raise ValueError('The initial node {} is not in the graph.'.format(initial_node))
        if graph.is_cyclic:
            raise ValueError('There are non-positive edges in the graph.')

        self._graph = graph
        self._initial_node = initial_node
        self._untouched = graph.nodes
        self._sorted = deque()
        self._dist = {}
        self._prev = {}

        self._topological_sort()
        self._run()

    def _topological_sort(self):
        """
        Topological sort on the DAG.
        """
        for node in self._graph.nodes:
            if node in self._untouched:
                self._visit(node)
        if len(self._graph.nodes) == len(self._sorted):
            print('Topological sort done...')
        else:
            raise ValueError('Topological sort failed: {} expected but {} sorted'
                             .format(
                                 len(self._graph.nodes),
                                 len(self._sorted)
                             ))

    def _visit(self, node):
        """
        visit a node in DFS search.
        """
        self._untouched.remove(node)
        for adj_node in self._graph.adjacent_nodes_of(node):
            if adj_node in self._untouched:
                self._visit(adj_node)
        self._sorted.appendleft(node)

    def _run(self):
        """
        Implement DAG algorithm to calculate shortest paths and distances for all nodes.
        """
        for node in self._sorted:
            self._dist[node] = math.inf
            self._prev[node] = None
        self._dist[self._initial_node] = 0

        while self._sorted:
            node = self._sorted.popleft()
            for adj_node in self._graph.adjacent_nodes_of(node):
                new_dist = self._dist[node] + self._graph.get_weight(node, adj_node)
                if new_dist < self._dist[adj_node]:
                    self._dist[adj_node] = new_dist
                    self._prev[adj_node] = node

        print('Successfully run DAG...')

    def shortest_distance_of(self, node):
        """
        Return the shortest distance from source of a given node.
        """
        if node not in self._graph.nodes:
            raise ValueError('Node {} is not in the graph'.format(node))
        else:
            return self._dist[node]

    def shortest_path_of(self, node):
        """
        Return the shortest path from source of a given node.
        """
        if node not in self._graph.nodes:
            raise ValueError('Node {} is not in the graph'.format(node))
        elif self._dist[node] == math.inf:
            return []
        else:
            current_node = node
            path = [node]
            while current_node != self._initial_node:
                current_node = self._prev[current_node]
                path.append(current_node)
            return path[::-1]

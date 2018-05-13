# -*- coding: utf-8 -*-
"""
Saving and extracting solutions for different graph problems.
"""

import math

class ShortestPath:
    """
    Solve single-source shortest path problem.
    """
    def __init__(self, graph, source, func):
        """
        Find solutions for the shortest path problem.
        """
        self._source = source
        self._dist, self._prev = func(graph, source)

    def shortest_distance_of(self, node):
        """
        Return the shortest distance from source to a given node.
        """
        if node not in self._dist:
            raise ValueError('Node {} is not in the graph'.format(node))
        else:
            return self._dist[node]

    def shortest_path_of(self, node):
        """
        Return the shortest path from source of a given node.
        """
        if node not in self._prev:
            raise ValueError('Node {} is not in the graph'.format(node))
        elif self._dist[node] == math.inf:
            return []
        else:
            current_node = node
            path = [node]
            while current_node != self._source:
                current_node = self._prev[current_node]
                path.append(current_node)
            return path[::-1]

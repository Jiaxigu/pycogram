# -*- coding: utf-8 -*-
"""
A minimalistic graph structure.
"""

from collections import defaultdict

class Graph:
    """
    Graph data structure. Represented as an adjacency list.
    The graph is a dictionary of nodes (as keys),
    adjacent nodes and weights (as keys/values in the sub-level dictionaries).
    Reference: https://stackoverflow.com/questions/19472530
    """

    def __init__(self, edges=None, directed=False):
        """
        Init a Graph instance given edges.
        If edges are not given, init an empty graph.
        """
        self._graph = defaultdict(dict)
        self._directed = directed
        if edges:
            self.add_edges(edges)

    def add_edges(self, edges):
        """
        Add edges (list of unweighted 2-tuples or/and weighted 3-tuples) to graph.
        """
        for edge in edges:
            if len(edge) == 2:
                node1, node2 = edge
                self.add(node1, node2)
            elif len(edge) == 3:
                node1, node2, weight = edge
                self.add(node1, node2, weight)
            else:
                raise ValueError('Edges must be 2- or 3-tuples but {} were given'.format(len(edge)))

    def add(self, node1, node2, weight=1.):
        """
        Add directed or bidirected edge between node1 and node2.
        If the edge already exists, update the edge weight.
        """
        self._graph[node1][node2] = weight
        if not self._directed:
            self._graph[node2][node1] = weight

    def remove(self, node, remove_edges_only=False):
        """
        Remove node and all edges to this node.
        If remove_edges_only is True, remove all outgoing edges from this node,
        but node itself and all incoming edges will be kept.
        """
        if not remove_edges_only:
            for related_edges in self._graph.values():
                try:
                    related_edges.pop(node)
                except KeyError:
                    pass
        try:
            del self._graph[node]
        except KeyError:
            pass

    @property
    def nodes(self):
        """
        Return all nodes in the graph as a set.
        """
        nodes = []
        for key, val in self._graph.items():
            nodes.append(key)
            nodes.extend([v for v in val.keys() if v not in nodes])
        return set(nodes)

    def adjacent_nodes_of(self, node):
        """
        Return all adjacent nodes in the graph of a given node.
        If the node is not in the graph, an empty set will be returned.
        """
        adj_nodes = set(self._graph[node].keys())
        if not adj_nodes:
            self.remove(node, remove_edges_only=True)
        return adj_nodes

    def get_weight(self, node1, node2):
        """
        Return the weight of the edge from node1 to node2.
        If there is no edge from node1 to node2 an error will be raised.
        """
        if not self.is_connected(node1, node2):
            raise ValueError('There is no edge between the given nodes')
        else:
            return self._graph[node1][node2]

    def is_connected(self, node1, node2):
        """
        Boolean value: is node1 directly connected to node2?
        """
        return node1 in self._graph and node2 in self._graph[node1]

    @property
    def is_positive(self):
        """
        Boolean value: is all edge weights positive?
        """
        return all([weight > 0 for edge in self._graph.values() for weight in edge.values()])

    @property
    def is_nonnegative(self):
        """
        Boolean value: is all edge weights non-negative?
        """
        return all([weight >= 0 for edge in self._graph.values() for weight in edge.values()])

    @property
    def is_cyclic(self):
        """
        Boolean value: does the graph contains a cycle?
        """
        path = set()
        visited = set()

        def visit(node):
            """
            Visit a node.
            """
            if node in visited:
                return False
            visited.add(node)
            path.add(node)
            for neighbour in self.adjacent_nodes_of(node):
                if neighbour in path or visit(neighbour):
                    return True
            path.remove(node)
            return False

        return any(visit(v) for v in self.nodes)

    def __str__(self):
        """
        override print.
        Calling print() now shows the adjacent list with weights as a dictionary.
        """
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))

    def __len__(self):
        """
        override len.
        Calling len() now shows the number of nodes.
        """
        return len(self.nodes)

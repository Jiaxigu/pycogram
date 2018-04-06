# -*- coding: utf-8 -*-
import math

class Dijkstra:
    """
    Given a graph instance and an initial node within the graph, find shortest paths for all nodes.
    The edges in the graph must be non-negative.
    """
    
    def __init__(self, graph, initial_node):
        """
        Init data structures for Dijkstra's algorithm.
        """
        if initial_node not in graph.nodes():
            raise ValueError('The initial node is not in the graph.')
        elif not graph.is_nonnegative():
            raise ValueError('There are non-positive edges in the graph.')
            
        self._Graph = graph
        self._unvisited_nodes = graph.nodes()
        self._initial_node = initial_node
        self._dist = {}
        self._prev = {}
        self._calculate()
        
    def _find_min_node(self):
        """
        Find the unvisited node with mininum distance.
        """
        return min(self._Graph._graph.keys(), key=(lambda x:self._dist[x] if x in self._unvisited_nodes else math.inf))
        
    def _calculate(self):
        """
        Calculate shortest paths and distances for all nodes. 
        """
        
        for v in self._unvisited_nodes:
            self._dist[v] = math.inf
            self._prev[v] = None
        
        self._dist[self._initial_node] = 0
        
        while self._unvisited_nodes:
            u = self._find_min_node()
            self._unvisited_nodes.remove(u)
            
            for adj_node in self._Graph.adjacent_nodes_of(u):
                new_dist = self._dist[u] + self._Graph.get_weight(u, adj_node)
                if new_dist < self._dist[adj_node]:
                    self._dist[adj_node] = new_dist
                    self._prev[adj_node] = u
                    
    def shortest_distance_of(self, node):
        """
        Return the shortest distance from source of a given node.
        """
        if node not in self._dist.keys():
            raise ValueError('Node is not in the graph')
        else:
            return self._dist[node]
    
    def shortest_path_of(self, node):
        """
        Return the shortest path from source of a given node.
        """
        current_node = node
        path = [node]
        while current_node != self._initial_node:
            current_node = self._prev[current_node]
            path.append(current_node)
        return path[::-1]
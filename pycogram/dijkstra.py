# -*- coding: utf-8 -*-
import math

class Dijkstra:
    """
    Given a graph and an initial node within the graph, find shortest paths and distances for all nodes.
    The edges in the graph must be non-negative.
    Reference: 
    - https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#pseudocode
    - Cormen T H. Introduction to algorithms[M]. MIT press, 2009.
    """
    
    def __init__(self, graph, initial_node):
        """
        Init data structures for Dijkstra's algorithm.
        """
        if initial_node not in graph.nodes:
            raise ValueError('The initial node {} is not in the graph.'.format(initial_node))
        if not graph.is_nonnegative:
            raise ValueError('There are non-positive edges in the graph.')
            
        self._Graph = graph
        self._unvisited_nodes = graph.nodes
        self._initial_node = initial_node
        self._dist = {}
        self._prev = {}
        self._run()
        
    """
    Implementation of Dijkstra's.
    """
    
    def _find_min_node(self):
        """
        Find the unvisited node with mininum distance.
        """
        return min(self._unvisited_nodes, key=(lambda x:self._dist[x]))
        
    def _run(self):
        """
        Implement Dijkstra's algorithm to calculate shortest paths and distances for all nodes. 
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
        
        print('Successfully run Dijkstra...')
    
    """
    Interpret the results.
    """
    
    def shortest_distance_of(self, node):
        """
        Return the shortest distance from source of a given node.
        """
        if node not in self._Graph.nodes:
            raise ValueError('Node {} is not in the graph'.format(node))
        else:
            return self._dist[node]
    
    def shortest_path_of(self, node):
        """
        Return the shortest path from source of a given node.
        """
        if node not in self._Graph.nodes:
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
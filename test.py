#-*- encoding: UTF-8 -*-
import unittest
import gc
from pycogram import *

class GraphTestCases(unittest.TestCase):
    """
    Test cases for graph.
    The graph is undirected.
    """
        
    def setUp(self):
        self.graph = Graph([(1, 2, 3.), (1, 3, 2.), (2, 4, 6.), (3, 4)], directed=False)
        
    def tearDown(self):
        del(self.graph)
        gc.collect()
    
    def test_len(self):
        self.assertEqual(len(self.graph), 4)
    
    def test_add(self):
        # update weight
        self.graph.add(1, 2, 9.)
        self.assertEqual(len(self.graph), 4)
        # new edge
        self.graph.add(4, 5)
        self.assertEqual(len(self.graph), 5)

        
    def test_add_wrong_tuple(self):
        with self.assertRaises(ValueError):
            self.graph.add_edges([(1, 3, 5., 1.)])
        with self.assertRaises(ValueError):
            self.graph.add_edges([(1,)])
    
    def test_remove(self):
        # remove a node
        self.graph.remove(4)
        self.assertEqual(len(self.graph), 3)
        # remove a non-existant node
        self.graph.remove('Hello')
        self.assertEqual(len(self.graph), 3)
    
    def test_get_nodes(self):
        self.assertEqual(len(self.graph.nodes()), 4)
    
    def test_adjacent_nodes(self):
        self.assertEqual(self.graph.adjacent_nodes_of(1), {2, 3})
        self.assertEqual(len(self.graph.adjacent_nodes_of('Kool')), 0)
    
    def test_get_weight(self):
        self.assertEqual(self.graph.get_weight(3, 4), 1.)
        with self.assertRaises(ValueError):
            self.graph.get_weight(1, 10)
            
    def test_is_positive(self):
        self.assertEqual(self.graph.is_positive(), True)
        self.assertEqual(self.graph.is_nonnegative(), True)
        # add a zero-weight edge
        self.graph.add(1, 4, 0.)
        self.assertEqual(self.graph.is_positive(), False)
        self.assertEqual(self.graph.is_nonnegative(), True)
        # add a negative-weight edge
        self.graph.add(2, 3, -2.)
        self.assertEqual(self.graph.is_positive(), False)
        self.assertEqual(self.graph.is_nonnegative(), False) 

        
class DirectedGraphTestCases(unittest.TestCase):
    """
    Extra test cases for directed graph.
    """
    
    def setUp(self):
        self.graph = Graph(directed=True)
    
    def tearDown(self):
        del(self.graph)
        
    def test_directed(self):
        self.graph.add(1, 2, 3.)
        self.assertEqual(self.graph.get_weight(1, 2), 3.)
        with self.assertRaises(ValueError):
            self.graph.get_weight(2, 1)
    
    def test_str_override(self):
        self.graph.add(1, 2, 3.)
        self.assertEqual(str(self.graph), 'Graph({1: {2: 3.0}})')
        

class DijkstraTestCases(unittest.TestCase):
    """
    Test cases for Dijkstra's algorithm.
    """
    def setUp(self):
        self.graph = Graph([(1, 2, 3.), (1, 3, 2.), (2, 4, 1.), (3, 4, 6.), (2, 3, 0.5)], directed=False)
        self.dijkstra = Dijkstra(self.graph, 1)
        
    def tearDown(self):
        del(self.graph)
        del(self.dijkstra)
        gc.collect()
        
    def test_shortest_distance(self):
        self.assertEqual(self.dijkstra.shortest_distance_of(1), 0.)
        self.assertEqual(self.dijkstra.shortest_distance_of(4), 3.5)
    
    def test_shortest_path(self):
        self.assertEqual(self.dijkstra.shortest_path_of(1), [1])
        self.assertEqual(self.dijkstra.shortest_path_of(4), [1, 3, 2, 4])
        
        
class DijkstraExceptionTestCases(unittest.TestCase):
    """
    Test cases for exception handling in the Dijkstra class.
    """
    def setUp(self):
        self.graph = Graph([(1, 2, 3.), (1, 3, 2.), (2, 4, 1.), (3, 4, 6.), (2, 3, 0.5)], directed=False)
        
    def tearDown(self):
        del(self.graph)
        gc.collect()
        
    def test_initial_node_exception(self):
        with self.assertRaises(ValueError):
            d = Dijkstra(self.graph, 'Initial')
    
    def test_negative_weight_exception(self):
        self.graph.add(1, 2, -1.)
        with self.assertRaises(ValueError):
            d = Dijkstra(self.graph, 1)
        

def suite_loader():
    test_cases = (GraphTestCases, DirectedGraphTestCases, DijkstraTestCases, DijkstraExceptionTestCases,)
    suite = unittest.TestSuite()
    for test_case in test_cases:
        tests = unittest.defaultTestLoader.loadTestsFromTestCase(test_case)
        suite.addTests(tests)
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite_loader')
#-*- encoding: UTF-8 -*-
"""
Test cases for pycogram.
"""

import unittest
import gc
import math
from pycogram import *

class GraphTestCases(unittest.TestCase):
    """
    Test cases for graph.
    The graph is undirected.
    """
    def setUp(self):
        self.graph = Graph([
            (1, 2, 3.),
            (1, 3, 2.),
            (2, 4, 6.),
            (3, 4)
        ], directed=False)

    def tearDown(self):
        del self.graph
        gc.collect()

    def test_len(self):
        self.assertEqual(len(self.graph), 4)

    def test_add(self):
        self.graph.add(1, 2, 9.)
        self.assertEqual(len(self.graph), 4)
        self.graph.add(4, 5)
        self.assertEqual(len(self.graph), 5)

    def test_add_wrong_tuple(self):
        with self.assertRaises(ValueError):
            self.graph.add_edges([(1, 3, 5., 1.)])
        with self.assertRaises(ValueError):
            self.graph.add_edges([(1,)])

    def test_remove(self):
        self.graph.remove(4)
        self.assertEqual(len(self.graph), 3)
        self.graph.remove('Hello')
        self.assertEqual(len(self.graph), 3)

    def test_get_nodes(self):
        self.assertEqual(len(self.graph.nodes), 4)

    def test_adjacent_nodes(self):
        self.assertEqual(self.graph.adjacent_nodes_of(1), {2, 3})
        self.assertEqual(len(self.graph.adjacent_nodes_of('Kool')), 0)
        self.assertEqual(len(self.graph), 4)

    def test_get_weight(self):
        self.assertEqual(self.graph.get_weight(3, 4), 1.)
        with self.assertRaises(ValueError):
            self.graph.get_weight(1, 10)

    def test_is_positive(self):
        self.assertEqual(self.graph.is_positive, True)
        self.assertEqual(self.graph.is_nonnegative, True)
        self.graph.add(1, 4, 0.)
        self.assertEqual(self.graph.is_positive, False)
        self.assertEqual(self.graph.is_nonnegative, True)
        self.graph.add(2, 3, -2.)
        self.assertEqual(self.graph.is_positive, False)
        self.assertEqual(self.graph.is_nonnegative, False)

class DirectedGraphTestCases(unittest.TestCase):
    """
    Extra test cases for directed graph.
    """

    def setUp(self):
        self.graph = Graph(directed=True)

    def tearDown(self):
        del self.graph

    def test_directed(self):
        self.graph.add(1, 2, 3.)
        self.assertEqual(len(self.graph), 2)
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
        self.graph = Graph([
            (1, 2, 3.),
            (1, 3, 2.),
            (2, 4, 1.),
            (3, 4, 6.),
            (2, 3, 0.5)
        ], directed=False)

    def tearDown(self):
        del self.graph
        gc.collect()

    def test_dijkstra_correctness(self):
        dist, prev = dijkstra(self.graph, 1)
        self.assertEqual(dist[1], 0.)
        self.assertEqual(dist[4], 3.5)
        self.assertEqual(prev[1], None)
        self.assertEqual(prev[4], 2)

    def test_source_exception(self):
        with self.assertRaises(ValueError):
            dijkstra(self.graph, 'Initial')

    def test_negative_weight_exception(self):
        self.graph.add(1, 2, -1.)
        with self.assertRaises(ValueError):
            dijkstra(self.graph, 1)

class DagTestCases(unittest.TestCase):
    """
    Test cases for DAG algorithm.
    """
    def setUp(self):
        nodes = [
            ('r', 's', 5),
            ('s', 't', 2),
            ('t', 'x', 7),
            ('x', 'y', -1),
            ('y', 'z', -2),
            ('r', 't', 3),
            ('t', 'y', 4),
            ('t', 'z', 2),
            ('s', 'x', 6),
            ('x', 'z', 1)
        ]
        self.graph = Graph(nodes, directed=True)

    def tearDown(self):
        del self.graph
        gc.collect()

    def test_dag_correctness(self):
        dist, prev = dag(self.graph, 's')
        self.assertEqual(dist['x'], 6)
        self.assertEqual(dist['r'], math.inf)
        self.assertEqual(prev['r'], None)
        self.assertEqual(prev['z'], 'y')

    def test_source_exception(self):
        with self.assertRaises(ValueError):
            dag(self.graph, 'Initial')

    def test_cyclic_graph_exception(self):
        self.graph.add('x', 's', 1.)
        with self.assertRaises(ValueError):
            dag(self.graph, 's')

class BellmanFordTestCases(unittest.TestCase):
    """
    Test cases for Bellman-Ford algorithm.
    """
    def setUp(self):
        nodes = [
            ('s', 't', 6),
            ('t', 'x', 5),
            ('x', 't', -2),
            ('s', 'y', 7),
            ('y', 'x', -3),
            ('y', 'z', 9),
            ('t', 'y', 8),
            ('t', 'z', -4),
            ('z', 's', 2),
            ('z', 'x', 7)
        ]
        self.graph = Graph(nodes, directed=True)

    def tearDown(self):
        del self.graph
        gc.collect()

    def test_bf_correctness(self):
        dist, prev = dag(self.graph, 's')
        self.assertEqual(dist['x'], 6)
        self.assertEqual(dist['z'], -2)
        self.assertEqual(prev['t'], 's')
        self.assertEqual(prev['y'], 'x')

    def test_source_exception(self):
        with self.assertRaises(ValueError):
            bellman_ford(self.graph, 'Initial')

    def test_negative_circle_exception(self):
        exp_nodes = [
            ('a', 'b', 1),
            ('b', 'a', -2)
        ]
        exp_graph = Graph(exp_nodes, directed=True)
        with self.assertRaises(ValueError):
            bellman_ford(self.graph, 'a')

class SolutionTestCases(unittest.TestCase):
    """
    Test cases for Solution module.
    """
    def setUp(self):
        nodes = [
            ('r', 's', 5),
            ('s', 't', 2),
            ('t', 'x', 7),
            ('x', 'y', -1),
            ('y', 'z', -2),
            ('r', 't', 3),
            ('t', 'y', 4),
            ('t', 'z', 2),
            ('s', 'x', 6),
            ('x', 'z', 1)
        ]
        self.graph = Graph(nodes, directed=True)
        self.sp = ShortestPath(self.graph, 's', dag)

    def tearDown(self):
        del self.graph
        gc.collect()

    def test_correctness(self):
        self.assertEqual(self.sp.shortest_distance_of('r'), math.inf)
        self.assertEqual(self.sp.shortest_path_of('s'), ['s'])
        self.assertEqual(self.sp.shortest_path_of('y'), ['s', 'x', 'y'])
        self.assertEqual(self.sp.shortest_path_of('r'), [])

    def test_distance_exception(self):
        with self.assertRaises(ValueError):
            self.sp.shortest_distance_of('a')

    def test_path_exception(self):
        with self.assertRaises(ValueError):
            self.sp.shortest_path_of('nope')

def suite_loader():
    test_cases = (
        GraphTestCases,
        DirectedGraphTestCases,
        DijkstraTestCases,
        DagTestCases,
        BellmanFordTestCases,
        SolutionTestCases,
    )
    suite = unittest.TestSuite()
    for test_case in test_cases:
        tests = unittest.defaultTestLoader.loadTestsFromTestCase(test_case)
        suite.addTests(tests)
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite_loader')

#-*- encoding: UTF-8 -*-
import unittest
from pycogram import *

class GraphTestCases(unittest.TestCase):
        
    def setUp(self):
        self.graph = Graph([(1, 2, 3.), (1, 3, 2.), (2, 4, 6.), (3, 4, 1.)])
        
    def tearDown(self):
        del(self.graph)
        gc.collect()
    
    def test_len(self):
        self.assertEqual(len(self.graph), 4)
    
    def test_add(self):
        self.graph.add(4, 5)
        self.assertEqual(len(self.graph), 5)

def suite_loader():
    test_cases = (GraphTestCases,)
    suite = unittest.TestSuite()
    for test_case in test_cases:
        tests = unittest.defaultTestLoader.loadTestsFromTestCase(test_case)
        suite.addTests(tests)
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite_loader')
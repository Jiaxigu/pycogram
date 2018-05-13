[![Build Status](https://travis-ci.org/Jiaxigu/pycogram.svg?branch=master)](https://travis-ci.org/Jiaxigu/pycogram)
[![Coverage Status](https://coveralls.io/repos/github/Jiaxigu/pycogram/badge.svg?branch=master)](https://coveralls.io/github/Jiaxigu/pycogram?branch=master)

# pycogram

A minimalistic python compilation of graph algorithms.

## Algorithms

- __Shortest path__
	- Dijkstra's Algorithm
	- DAG

## Requirement

- python >= 3.5

## Install (sudo might be required)

	python setup.py install

## Testing

	python test.py -v

## Usage

### Init

Create an directed graph with edges (Example from Introduction to Algorithms, 3rd Edition):

	edges = [
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
	g = Graph(edges, directed=True)

	
### Run algorithms

Run DAG to find the shortest path:

	sp = ShortestPath(g, source='s', func=dag)
	sp.shortest_distance_of('y')
	>>> 5
	sp.shortest_path_of('z')
	>>> ['s', 'x', 'y', 'z']



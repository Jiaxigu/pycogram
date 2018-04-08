[![Build Status](https://travis-ci.org/Jiaxigu/pycogram.svg?branch=master)](https://travis-ci.org/Jiaxigu/pycogram)
[![Coverage Status](https://coveralls.io/repos/github/Jiaxigu/pycogram/badge.svg?branch=master)](https://coveralls.io/github/Jiaxigu/pycogram?branch=master)

# pycogram
A minimalistic python compilation of graph algorithms.

## Algorithms

- __Shortest path__
	- Dijkstra's Algorithm

## Requirement

- python >= 3.5

## Install (sudo might be required)

	>>> python setup.py install

## Testing

	>>> python test.py -v

## Usage

### Init

Create an empty, directed graph:

	>>> g = Graph(directed=True)

Create an undirected graph:

	>>> g = Graph([(1, 2, 3.), (1, 3, 2.), (2, 4, 1.), (3, 4, 6.), (2, 3, 0.5))], directed=False)
	
### Run algorithms

Run Dijkstra's algorithm to find the shortest path:

	>>> d = Dijkstra(g, 1)
	>>> d.shortest_path_of(4)
	<<< [1, 3, 2, 4]
	>>> d.shortest_distance_of(4)
	<<< 3.5













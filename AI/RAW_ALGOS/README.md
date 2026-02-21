# RAW_ALGOS

Pure-Python algorithms: sorting, searching, and graph traversal.

## Modules
- `sorting.py`: Quicksort, mergesort.
- `searching.py`: Linear search, binary search.
- `graph.py`: BFS, DFS, Dijkstra (weighted).

## Quick start
```python
from RAW_ALGOS import quicksort, binary_search, dijkstra

arr = [3, 1, 4, 2]
print(quicksort(arr))
print(binary_search([1, 2, 3, 4], 3))

graph = {"A": [("B", 1.0), ("C", 3.0)], "B": [("C", 1.0)]}
print(dijkstra(graph, "A"))
```

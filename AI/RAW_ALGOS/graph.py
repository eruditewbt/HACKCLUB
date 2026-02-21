import heapq
from collections import deque


def bfs(graph, start):
    """Breadth-first traversal of adjacency dict graph."""
    visited = set([start])
    order = []
    q = deque([start])
    while q:
        node = q.popleft()
        order.append(node)
        for neigh in graph.get(node, []):
            if neigh not in visited:
                visited.add(neigh)
                q.append(neigh)
    return order


def dfs(graph, start):
    """Depth-first traversal of adjacency dict graph."""
    visited = set()
    order = []

    def _visit(node):
        visited.add(node)
        order.append(node)
        for neigh in graph.get(node, []):
            if neigh not in visited:
                _visit(neigh)

    _visit(start)
    return order


def dijkstra(graph, start):
    """Shortest paths for weighted graph: graph[u] = list of (v, w)."""
    dist = {start: 0.0}
    pq = [(0.0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist.get(u, None):
            continue
        for v, w in graph.get(u, []):
            nd = d + w
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist

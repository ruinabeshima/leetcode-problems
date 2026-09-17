from collections import deque, defaultdict
import heapq

def bfs(start, graph): 
    queue = deque([start])
    visited = {start}

    while queue:
        node = queue.popleft()
        print(node)

        for neighbor in graph[node]: 
            if neighbor not in visited: 
                visited.add(neighbor)
                queue.append(neighbor)


def iterative_dfs(start, graph): 
    stack = [start]
    visited = {start}

    while stack: 
        node = stack.pop() 
        print(node)

        for neighbor in graph[node]: 
            if neighbor not in visited: 
                visited.add(neighbor)
                stack.append(neighbor)


def recursive_dfs(node, graph, visited):
    if node in visited: 
        return 

    print(node)
    visited.add(node)
    for neighbor in graph[node]: 
        recursive_dfs(neighbor, graph, visited)

"""
BFS which counts the steps from start to node A. 
Key point: At the top of each while iteration, the queue contains 
exactly ONE level. 
Increment count after draining one level 
"""
def bfs_with_levels(start, target, graph):
    queue = deque([start])
    visited = {start}
    steps = 0 

    while queue:
        # Drain one level by removing all elements in that queue 
        for i in range(len(queue)): 
            node = queue.popleft() 

            if node == target: 
                return steps 

            for neighbor in graph[node]: 
                if neighbor not in visited: 
                    visited.add(neighbor)
                    queue.append(neighbor)

        steps += 1 

    return -1          


def dfs_on_grid(grid, r, c):
    rows, cols = len(grid), len(grid[0])

    # Base cases 
    if r < 0 or r >= rows or c < 0 or c >= cols: 
        return 
    if grid[r][c] == "0": 
        return 

    # MARK before recursing (for O(1) extra space)
    # Use a visited set when the grid is read-only / values matter later
    grid[r][c] = "0"

    dfs_on_grid(grid, r + 1, c)
    dfs_on_grid(grid, r - 1, c)
    dfs_on_grid(grid, r, c + 1)
    dfs_on_grid(grid, r, c - 1)
    

""" 
Union-Find: UNDIRECTED
1. Find: Seeing if node A and node B are connected in a graph 
2. Join: Connecting two nodes which have not been connected

Logic: Give every group a single "parent"/representative 
Two nodes are in the same group = they have the same parent 
Parent is the root node. 
"""

class DSU: 
    def __init__(self, n): 
        self.parent = list(range(n)) # Everyone is their own root 
        self.rank = [0] * n 
        self.count = n 

    """ 
    Find: Walk up to the root 
    Path compression: Going up by one parent each is O(n) and is slow. 
    Instead, skip the parent and go straight to the grandparent
    """
    def find(self, x): 
        while self.parent[x] != x: 
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x 


    """ 
    Union: Find both roots and make one point at the other 
    Union By rank: Hang the short tree under the taller tree. 
    Rank is the rough estimate of the tree's height. 
    """
    # Union: Find both roots and make one point at the other 
    def union(self, x, y): 
        rx, ry = self.find(x), self.find(y)

        # Same root = same group 
        if rx == ry: 
            return False 

        # Swap to hang ry (shorter) below rx 
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx 

        self.parent[ry] = rx

        # Both trees are the same height, so the merged tree got taller
        if self.rank[rx] == self.rank[ry]: 
            self.rank[rx] += 1 

        # How many trees there are 
        self.count -= 1 
        return True 


r""" 
Kahn's Algorithm: DIRECTED 
You have tasks with prerequisites, and you have to find a valid order 
to do them all. 

0 → 2      "do 0 before 2"
1 → 2
2 → 3
2 → 4
3 → 5
4 → 5


Valid Order: 
   0     1
    \   /
      2
     / \
    3   4
     \ /
      5


Key point: A task with 0 unmet prerequisites can be done right now.

graph[u] = who depends on u. When u finishes, this is the list of 
tasks to notify. 
indegree[v] = how many prerequisites of v are still unfinished  
"""

def topological_sort(n, edges): 
    graph = defaultdict(list)
    indegree = [0] * n 

    for u, v in edges: 
        graph[u].append(v)
        indegree[v] += 1 

    # Add nodes with indegree 0 (they don't depend on anything so can 
    # be processed)
    queue = deque([i for i in range(n) if indegree[i] == 0])

    order = []
    while queue: 
        node = queue.popleft() 
        order.append(node)

        # What depends on this node?
        for neighbor in graph[node]: 
            indegree[neighbor] -= 1 
            if indegree[neighbor] == 0: 
                queue.append(neighbor)


    # In built cycle detection 
    return order if len(order) == n else []

         
""" 
Dijkstra's Algorithm 
Edges have WEIGHTS, and shortest means smallest total weight 

Neighbors now carry a weight, so each entry is a tuple 

graph = {
    0: [(1, 4), (2, 1)],        # 0 connects to 1 (cost 4) and 2 (cost 1)
    1: [(0, 4), (2, 2), (3, 5)],
    2: [(0, 1), (1, 2), (3, 8)],
    3: [(1, 5), (2, 8), (4, 3)],
    4: [(3, 3)],
}


BFS doesn't work anymore as the queue handed nodes in distance order. 
Key Point: Swap the queue for a min-heap, which always hands you the 
smallest weight-distance.
DIJKSTRA: BFS BUT WITH A PRIORITY QUEUE
"""
def djikstra(start, graph, n): 
    dist = [float('inf')] * n 
    dist[start] = 0 
    heap = [(0, start)] # (Distance, node )

    while heap: 
        d, u = heapq.heappop(heap)

        # Stale entry - skip 
        if d > dist[u]: 
            continue 

        for v, w in graph[u]:
            nd = d + w 
            if nd < dist[v]: 
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

        return dist





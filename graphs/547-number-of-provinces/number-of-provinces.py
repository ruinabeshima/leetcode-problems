class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        graph = defaultdict(list)
        rows, cols = len(isConnected), len(isConnected[0])
        visited = set() 

        for i in range(rows): 
            for j in range(cols): 
                if i != j and isConnected[i][j] == 1: 
                    graph[i].append(j)

        def dfs(node):
            visited.add(node)
            for neighbor in graph[node]: 
                if neighbor not in visited: 
                    dfs(neighbor)

        provinces = 0 
        for i in range(rows): 
            if i not in visited: 
                dfs(i) 
                provinces += 1 

        return provinces


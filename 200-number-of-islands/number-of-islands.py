class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        rows, cols = len(grid), len(grid[0])
        seen = set()
        islands = 0 

        def dfs(row, col): 
            seen.add((row, col))

            directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
            for dr, dc in directions: 
                r, c = row + dr, col + dc
                if r in range(rows) and c in range(cols) and grid[r][c] == "1" and (r, c) not in seen: 
                    dfs(r, c)

        def iterative_dfs(row, col): 
            stack = [[row, col]]
            seen.add((row, col))
            directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]

            while stack: 
                row, col = stack.pop() 
                for dr, dc in directions: 
                    r, c = row + dr, col + dc
                    if r in range(rows) and c in range(cols) and grid[r][c] == "1" and (r, c) not in seen: 
                        stack.append([r, c])
                        seen.add((r, c))

        def iterative_bfs(row, col): 
            queue = deque() 
            queue.append([row, col])
            seen.add((row, col))
            directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]

            while queue: 
                row, col = queue.popleft()
                for dr, dc in directions: 
                    r, c = row + dr, col + dc 
                    if r in range(rows) and c in range(cols) and grid[r][c] == "1" and (r, c) not in seen:
                        seen.add((r, c))
                        queue.append([r, c])

        for row in range(rows): 
            for col in range(cols): 
                if grid[row][col] == "1" and (row, col) not in seen: 
                    iterative_bfs(row, col)
                    islands += 1 
        
        return islands 

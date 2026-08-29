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

        for row in range(rows): 
            for col in range(cols): 
                if grid[row][col] == "1" and (row, col) not in seen: 
                    dfs(row, col)
                    islands += 1 
        
        return islands 

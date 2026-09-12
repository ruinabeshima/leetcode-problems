class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        nrows, ncols = len(grid), len(grid[0])
        maxArea = 0 

        def dfs(r, c):
            if r < 0 or r >= nrows or c < 0 or c >= ncols: 
                return 0 
            if grid[r][c] == 0: 
                return 0 

            grid[r][c] = 0 
            
            return 1 + dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1) + dfs(r, c - 1)

        for i in range(nrows): 
            for j in range(ncols): 
                if grid[i][j] == 1: 
                    maxArea = max(maxArea, dfs(i, j))

        return maxArea
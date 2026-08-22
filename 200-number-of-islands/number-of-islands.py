class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        rows, cols = len(grid), len(grid[0])
        seen = set()
        islands = 0 

        def bfs(r, c): 
            q = collections.deque()
            q.append((r, c))
            seen.add((r, c))

            directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
            while q:
                r, c = q.popleft()
                for dr, dc in directions:
                    row, col = r + dr, c + dc
                    if row in range(rows) and col in range(cols) and grid[row][col] == "1" and (row, col) not in seen:
                        seen.add((row, col))
                        q.append((row, col))

        for r in range(rows): 
            for c in range(cols): 
                if grid[r][c] == "1" and (r, c) not in seen:
                    bfs(r, c)
                    islands += 1

        return islands 



        
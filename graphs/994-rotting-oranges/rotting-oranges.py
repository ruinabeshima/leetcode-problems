class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        queue = deque()
        steps, fresh = 0, 0
        rows, cols = len(grid), len(grid[0])

        # Add rotten oranges to the queue 
        for i in range(rows): 
            for j in range(cols): 
                if grid[i][j] == 2: 
                    queue.append((i, j))
                elif grid[i][j] == 1: 
                    fresh += 1 

        if fresh == 0: 
            return 0


        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        while queue and fresh > 0: 
            for _ in range(len(queue)): 
                r, c = queue.popleft()
        
                for dr, dc in directions: 
                    nrow, ncol = r + dr, c + dc 
                    if nrow in range(rows) and ncol in range(cols) and grid[nrow][ncol] == 1:
                        fresh -= 1 
                        queue.append((nrow, ncol)) 
                        grid[nrow][ncol] = 2

            steps += 1 

        return steps if fresh == 0 else -1 



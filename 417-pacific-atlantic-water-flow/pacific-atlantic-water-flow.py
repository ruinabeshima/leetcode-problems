class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        rows, cols = len(heights), len(heights[0])
        result = []

        # Initialise pacific and atlantic sets 
        pacific = set()
        atlantic = set()
        for row in range(rows):
            pacific.add((row, 0))
            atlantic.add((row, cols - 1))
        for col in range(cols):
            pacific.add((0, col))
            atlantic.add((rows - 1, col))

        # bfs 
        def bfs(r, c):
            p_found, a_found = False, False 
            q = collections.deque()
            q.append((r, c))
            seen = set()

            while q: 
                row, col = q.popleft()

                if (row, col) in pacific: 
                    p_found = True 
                if (row, col) in atlantic: 
                    a_found = True 

                if p_found and a_found: 
                    result.append((r, c))
                    break

                directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
                for dr, dc in directions:
                    drow = row + dr 
                    dcol = col + dc 
                    if drow in range(rows) and dcol in range(cols) and (drow, dcol) not in seen and heights[drow][dcol] <= heights[row][col]: 
                        if (drow, dcol) in pacific: 
                            p_found = True 
                        if (drow, dcol)in atlantic: 
                            a_found = True 
                        q.append((drow, dcol))
                        seen.add((drow, dcol))



        # Look at every coordinate 
        for row in range(rows): 
            for col in range(cols): 
                bfs(row, col)

        return result

            




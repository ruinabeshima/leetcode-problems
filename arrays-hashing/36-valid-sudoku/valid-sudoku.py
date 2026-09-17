class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        
        # Checking rows for duplicates 
        for i in range(9): 
            rows = set()
            for j in range(9): 
                if board[i][j] != ".":
                    if board[i][j] in rows: 
                        return False 
                    rows.add(board[i][j])

        # Columns 
        for i in range(9): 
            cols = set()
            for j in range(9): 
                if board[j][i] != ".": 
                    if board[j][i] in cols: 
                        return False 
                    cols.add(board[j][i])

        # 3x3 boxes 
        grid = defaultdict(set)
        for i in range(9): 
            for j in range(9): 
                if board[i][j] != ".": 
                    key = (i//3, j//3)
                    if board[i][j] in grid[key]: 
                        return False 
                    grid[key].add(board[i][j])

        return True 


             
                
    


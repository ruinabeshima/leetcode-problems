class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m = len(matrix) # Whole 2D Matrix 
        n = len(matrix[0]) # Each row 

        left = 0 
        right = m * n - 1 

        while right >= left: 
            complement = left + (right - left) // 2 
            row = complement // n
            col = complement % n 
            if (matrix[row][col] == target):
                return True
            elif (matrix[row][col] < target): 
                left = complement + 1 
            else: 
                right = complement - 1 

        return False




        return search_list
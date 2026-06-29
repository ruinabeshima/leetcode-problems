class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        search_list = [] 
        for row in matrix: 
            for num in row: 
                search_list.append(num)


        left = 0 
        right = len(search_list) - 1
        while right >= left: 
            complement = left + (right - left) // 2 
            if search_list[complement] == target: 
                return True 
            elif search_list[complement] < target: 
                left = complement + 1 
            else: 
                right = complement - 1 
        return False 

        return search_list
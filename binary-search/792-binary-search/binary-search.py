class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left = 0 
        right = len(nums) - 1 

        while right >= left: 
            complement = (left + right) // 2 
            if nums[complement] == target: 
                return complement 
            elif nums[complement] < target: 
                left = complement + 1 
            else: 
                right = complement - 1 
        
        return -1
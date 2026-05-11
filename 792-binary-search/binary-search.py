class Solution:
    def search(self, nums: List[int], target: int) -> int:
        lower = 0 
        upper = len(nums) - 1 

        while lower <= upper: 
            complement = (upper + lower) // 2 

            if nums[complement] == target: 
                return complement 
            elif nums[complement] < target: 
                lower = complement + 1 
            elif nums[complement] > target: 
                upper = complement - 1

        return -1 

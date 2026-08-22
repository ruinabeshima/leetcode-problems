class Solution:
    def rob(self, nums: List[int]) -> int:

        n = len(nums)- 1
        if n == -1:
            return 0
        if n == 0: 
            return nums[0]
        if n == 1: 
            return max(nums[1], nums[0])
        
        prev, curr = nums[0], max(nums[1], nums[0])
       
        for i in range(2, len(nums)): 
            prev, curr = curr, max(nums[i] + prev, curr)

        return curr 
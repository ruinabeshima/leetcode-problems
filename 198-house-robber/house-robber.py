class Solution:
    def rob(self, nums: List[int]) -> int:

        n = len(nums)- 1
        if n == -1:
            return 0
        if n == 0: 
            return nums[0]
        if n == 1: 
            return max(nums[1], nums[0])
        memo = {0: nums[0], 1: max(nums[1], nums[0])}
       
        def maxMoney(n):
            if n in memo: 
                return memo[n]
            else: 
                memo[n] = max(nums[n] + maxMoney(n - 2), maxMoney(n - 1))
                return memo[n]

        return maxMoney(n)
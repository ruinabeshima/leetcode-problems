class Solution:
    def rob(self, nums: List[int]) -> int:
        n = len(nums) - 1 
        if n == 0: 
            return nums[0]
        memo = {}

        def maxMoney(i, start):
            if (i, start) in memo: 
                return memo[(i, start)]
            else: 
                if i < start: 
                    memo[(i, start)] = 0 
                elif i == start: 
                    memo[(i, start)] = nums[start]
                else: 
                    memo[(i, start)] = max(nums[i] + maxMoney(i - 2, start), maxMoney(i - 1, start))
                return memo[(i, start)]

        return max(maxMoney(n - 1, 0), maxMoney(n, 1))


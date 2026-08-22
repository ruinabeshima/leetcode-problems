class Solution:
    def climbStairs(self, n: int) -> int:
        memo = {1:1, 2:2}
        
        def s(n): 
            if n in memo:
                return memo[n]
            else: 
                memo[n] = s(n - 1) + s(n - 2)
                return memo[n]
        
        return s(n)

class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        missing = set(nums)

        for i in range(0, len(nums) + 1): 
            if i not in missing: 
                return i
        
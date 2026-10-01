class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        # Prefix 
        prefix = [1 for i in range(len(nums))]
        track = 1 
        for i in range(len(nums)): 
            prefix[i] = track
            track *= nums[i]

        # Suffixes
        track = 1 
        for i in range(len(nums) - 1, -1, -1):
            prefix[i] *= track
            track *= nums[i]

        return prefix

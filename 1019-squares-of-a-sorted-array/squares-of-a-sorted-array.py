class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        for i in range(len(nums)): 
            nums[i] = abs(nums[i])

        nums.sort() 

        for j in range(len(nums)): 
            nums[j] = nums[j] * nums[j]

        return nums
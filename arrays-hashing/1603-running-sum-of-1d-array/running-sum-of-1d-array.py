class Solution:
    def runningSum(self, nums: List[int]) -> List[int]:
        left = 0 
        right = 1

        while right < len(nums): 
            nums[right] += nums[left] 
            left += 1 
            right += 1 

        return nums
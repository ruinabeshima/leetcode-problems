class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        nums_sum = sum(nums[:k])
        max_average = nums_sum / k

        for i in range(k, len(nums)): 
            nums_sum = nums_sum + nums[i] - nums[i - k]
            max_average = max(nums_sum / k, max_average)

        return max_average
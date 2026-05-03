class Solution:
    def runningSum(self, nums: List[int]) -> List[int]:
        runningSum = [] 

        for i in range(0, len(nums)): 
            if i == 0: 
                runningSum.append(nums[0])
            else: 
                runningSum.append(nums[i] + runningSum[i - 1])

        return runningSum
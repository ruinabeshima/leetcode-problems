class Solution:
    def getConcatenation(self, nums: List[int]) -> List[int]:
        ans = [0 for i in range(len(nums) * 2)]

        for index, num in enumerate(nums):  
            ans[index] = num 
            ans[index + len(nums)] = num

        return ans
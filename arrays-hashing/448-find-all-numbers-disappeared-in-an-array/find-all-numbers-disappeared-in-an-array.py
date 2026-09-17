class Solution:
    def findDisappearedNumbers(self, nums: List[int]) -> List[int]:
        missing = set(nums) 
        values = []

        for i in range(1, len(nums) + 1): 
            if i not in missing: 
                values.append(i)

        return values
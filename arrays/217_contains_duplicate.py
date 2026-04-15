from typing import List


class Solution:
    # With dictionaries - O(n) time. Value does not matter
    def containsDuplicatewithDict(self, nums: List[int]) -> bool:  # type: ignore
        duplicate = {}
        for num in nums:
            if num in duplicate:
                return True
            duplicate[num] = True

        return False

    """ 
    Sets are like dictionaries but with keys only, no values 
    """

    # With sets - O(n) time
    def containsDuplicate(self, nums: List[int]) -> bool:  # type: ignore
        duplicate = set()
        for num in nums:
            if num in duplicate:
                return True
            duplicate.add(num)
        return False


"""
Test Cases: 
1. True 
2. False 
3. True 
"""

sol = Solution()
print(sol.containsDuplicatewithDict([1, 2, 3, 1]))
print(sol.containsDuplicatewithDict([1, 2, 3, 4]))
print(sol.containsDuplicatewithDict([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]))

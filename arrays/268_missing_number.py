from typing import List


class Solution:
    # Brute force - O(n^2) time
    def attempt1(self, nums: List[int]) -> int:  # type: ignore
        for i in range(len(nums) + 1):
            if i not in nums:
                return i

    # Sets - O(n) time
    def attempt2(self, nums: List[int]) -> int:  # type: ignore
        nums_set = set(nums)

        for i in range(len(nums) + 1):
            if i not in nums_set:
                return i

    """
    Gauss' Formula - Find total and subtract from actual sum 
    O(1) space 
    """

    def attempt3(self, nums: List[int]) -> int:  # type: ignore
        return len(nums) * (len(nums) + 1) // 2 - sum(nums)


"""
Test Cases:
1. 2
2. 2
3. 1
"""

sol = Solution()
print(sol.attempt1([3, 0, 1]))
print(sol.attempt1([0, 1, 3, 4, 5, 6, 7, 2, 9]))
print(sol.attempt1([0]))

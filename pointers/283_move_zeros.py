from typing import List


""" 
Two pointer technique 
Right pointer scans the array to find non zero elements 
Left pointer tracks where the next non zero element should be placed
O(n) time, O(1) space
"""


class Solution:
    def moveZeroes(self, nums: List[int]) -> None:  # type: ignore
        left = 0

        for right in range(0, len(nums)):
            if nums[right] != 0:
                nums[right], nums[left] = nums[left], nums[right]
                left += 1


"""
Test Cases:
1. [1, 3, 12, 0, 0]
2. [0]
"""

sol = Solution()
sol.moveZeroes([0, 1, 0, 3, 12])
print([0, 1, 0, 3, 12])
sol.moveZeroes([0])
print([0])

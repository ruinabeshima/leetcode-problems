from typing import List


class Solution:

    # Brute force - O(n^2) time
    def attempt1(self, nums: List[int]) -> List[int]:  # type: ignore
        missing = []

        for i in range(0, len(nums)):
            if i + 1 not in nums:
                missing.append(i + 1)

        return missing

    # Using a set - O(n) time
    def attempt2(self, nums: List[int]) -> List[int]:  # type: ignore
        nums_set = set(nums)
        missing = []

        for i in range(len(nums)):
            if i + 1 not in nums_set:
                missing.append(i + 1)

        return missing

    """
    In-place approach: An interview trick 
    The values in the array must fall between 1 and n, so they can be mapped to a valid index. 
    Use the sign (positive / negative) of each element as a boolean flag to record whether you've seen the number in the array, without needing extra space 
    Actual values are still recoverable with abs() - returns the ABSOLUTE number
    
    THIS METHOD IS STILL O(N) TIME, BUT IT IS O(1) SPACE  
    """

    def attempt3(self, nums: List[int]) -> List[int]:  # type: ignore
        for num in nums:
            idx = abs(num) - 1
            nums[idx] = -abs(nums[idx])

        # Remaining positive values - that number was never seen
        return [i + 1 for i, n in enumerate(nums) if n > 0]


"""
Test Cases:
1. [5, 6]
2. [2]
"""

sol = Solution()
print(sol.attempt3([4, 3, 2, 7, 8, 2, 3, 1]))
print(sol.attempt3([1, 1]))

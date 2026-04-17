from typing import List


class Solution:
    """
    Attempt 1: Find absolute value, sort, then square
    O(n log n) time, O(1) space
    """

    def attempt1(self, nums: List[int]) -> List[int]:  # type: ignore

        # Replace with positive values
        for i in range(0, len(nums)):
            nums[i] = abs(nums[i])

        # Sort
        nums = sorted(nums)

        # Square
        for i in range(0, len(nums)):
            nums[i] = nums[i] * nums[i]

        return nums

    """
    Two pointers at the end of the array 
    Square the value with the larger absolute value and add it at the end of the result array (which has a pointer at the back)
    Update left and right pointers, as well as result array pointer 
    O(n) time and O(n) space (which is unavoidable as you cannot sort in O(1) space)
    """

    def attempt2(self, nums: List[int]) -> List[int]:  # type: ignore
        left = 0
        right = len(nums) - 1
        result = [0] * len(nums)
        result_pointer = len(nums) - 1

        while right >= left:
            if abs(nums[left]) > abs(nums[right]):
                result[result_pointer] = nums[left] ** 2
                left += 1
                result_pointer -= 1
            else:
                result[result_pointer] = nums[right] ** 2
                right -= 1
                result_pointer -= 1

        return result


"""
Test Cases:
1. [0, 1, 9, 16, 100]
2. [4, 9, 9, 49, 121]
"""

sol = Solution()
print(sol.attempt1([-4, -1, 0, 3, 10]))
print(sol.attempt1([-7, -3, 2, 3, 11]))

from typing import List


class Solution:

    # Dict O(n) time and O(n) space
    def attempt1(self, nums: List[int]) -> List[int]:  # type: ignore
        num_list = {}
        duplicates = []

        for num in nums:
            if num in num_list:
                num_list[num] += 1
            else:
                num_list[num] = 1

        for key in num_list:
            if num_list[key] == 2:
                duplicates.append(key)

        return duplicates

    # In-place algorithm: O(1) space
    def attempt1(self, nums: List[int]) -> List[int]:  # type: ignore
        duplicates = []

        for num in nums:
            idx = abs(num) - 1

            if nums[idx] < 0:
                duplicates.append(abs(num))
            else:
                nums[idx] = -abs(nums[idx])

        return duplicates


"""
Test Cases:
1. [2, 3]
2. [3]
3. []
"""

sol = Solution()
print(sol.attempt1([4, 3, 2, 7, 8, 2, 3, 1]))
print(sol.attempt1([1, 1, 2, 3, 3]))
print(sol.attempt1([1]))

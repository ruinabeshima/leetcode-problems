from typing import List


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:  # type: ignore
        numbers = {}

        # Define a dictionary - add 1 to the total if number exists, add new number if not O(n) 
        for number in nums:
            if number not in numbers:
                numbers[number] = 1
            else:
                numbers[number] += 1

        # Sort the dict by VALUES not keys O(n log n)
        frequent = sorted(numbers, key=lambda x: numbers[x])
        # Return last k values O(n)
        return frequent[-k:]


"""
Test Cases:
1. [1, 2]
2. [1]
"""

sol = Solution()
print(sol.topKFrequent([1, 1, 1, 2, 2, 3], 2))
print(sol.topKFrequent([1], 1))

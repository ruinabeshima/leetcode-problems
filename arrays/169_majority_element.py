from typing import List


class Solution:

    # Dict
    def attempt1(self, nums: List[int]) -> int:  # type: ignore
        num_list = {}

        for num in nums:
            if num in num_list:
                num_list[num] += 1
            else:
                num_list[num] = 1

        # Return maximum index
        return max(num_list, key=lambda x: num_list[x])

    """
    Boyer-Moore Voting Algorithm 
    Majority element appears more than n/2 times. 
    Candidate is the most "voted for" value, and if the count is 0 it means there are equal on each side 
    Increase count by 1 if same number as candidate, and descrease if not 
    O(1) time 
    """

    def attempt2(self, nums: List[int]) -> int:  # type: ignore
        count = 0
        candidate = None

        for num in nums:
            if count == 0:
                candidate = num

            if num == candidate:
                count += 1
            else:
                count -= 1

        return candidate  # type: ignore


"""
Test Cases:
1. 3
2. 2
"""

sol = Solution()
print(sol.attempt1([3, 2, 3]))
print(sol.attempt1([2, 2, 1, 1, 1, 2, 2]))

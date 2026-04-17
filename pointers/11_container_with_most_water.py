from typing import List

"""
Pointers on both sides 
Calculate the area using smaller height x width 
Set the max height as a variable 
Move the pointer with the smaller height inwards as thats the only way to get a greater area
O(n) time, with 0(1) space 
"""


class Solution:
    def maxArea(self, height: List[int]) -> int:  # type: ignore
        max_area = 0
        left = 0
        right = len(height) - 1

        while left < right:
            area = min(height[left], height[right]) * (right - left)
            if area > max_area:
                max_area = area

            if height[right] > height[left]:
                left += 1
            else:
                right -= 1

        return max_area


"""
Test Cases:
1. 49
2. 1
"""

sol = Solution()
print(sol.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]))
print(sol.maxArea([1, 1]))

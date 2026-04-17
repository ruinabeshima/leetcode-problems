from typing import List


class Solution:

    # Brute force - O(n^2) time
    def attempt1(self, nums: List[int]) -> List[int]:  # type: ignore
        products = []

        for i in range(0, len(nums)):
            product = 1
            for j in range(0, len(nums)):
                if nums[j] != nums[i]:
                    product *= nums[j]
            products.append(product)

        return products

    """ 
    Product of everything to the left of i * Product of everything to the right of i 
    O(n) time
    """

    def attempt2(self, nums: List[int]) -> List[int]:
        # You cannot index into an empty list
        left = [0] * len(nums)
        right = [0] * len(nums)
        products = [0] * len(nums)

        for i in range(0, len(nums)):
            if i == 0:
                left[i] = 1
            else:
                left[i] = left[i - 1] * nums[i - 1]

        for i in range(len(nums) - 1, -1, -1):
            if i == len(nums) - 1:
                right[i] = 1
            else:
                right[i] = right[i + 1] * nums[i + 1]

        for i in range(0, len(nums)):
            products[i] = left[i] * right[i]

        return products

    # O(1) space
    def attempt3(self, nums: List[int]) -> List[int]:  # type: ignore

        # You cannot index into an empty list
        right = [0] * len(nums)
        products = [0] * len(nums)

        for i in range(0, len(nums)):
            if i == 0:
                products[i] = 1
            else:
                products[i] = products[i - 1] * nums[i - 1]

        right_product = 1
        for i in range(len(nums) - 1, -1, -1):
            products[i] *= right_product
            right_product *= nums[i]

        return products


"""
Test Cases:
1. [24, 12, 8, 6]
2. [0, 0, 9, 0]
"""

sol = Solution()
print(sol.attempt2([1, 2, 3, 4]))
print(sol.attempt2([-1, 1, 0, -3, 3]))

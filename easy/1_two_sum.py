from typing import List


class Solution:
    # O(n^2) time
    def bruteForce(self, nums: List[int], target: int) -> List[int]:  # type: ignore
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]

    """
    Hashmaps: Stores key-value pairs 
    O(1) for looking up any key 
    In python dictionaries are hash maps 

    ex. Store value 5, index 0 
    hashMap[5] = 0
    
    Print the index
    print(hashMap[5])
     """

    # O(n) time
    def twoSum(self, nums: List[int], target: int) -> List[int]:  # type: ignore
        hashMap = {}
        # enumerate() - Looping convenience, gets both index and value
        for index, num in enumerate(nums):
            complement = target - num
            if complement in hashMap:
                return [index, hashMap[complement]]
            hashMap[num] = index


sol = Solution()

"""
Test Cases: 
1. Expected: [0, 1]
2. Expected: [1, 2]
3. Expected: [0, 1]
"""

print(sol.bruteForce([2, 7, 11, 15], 9))
print(sol.bruteForce([3, 2, 4], 6))
print(sol.bruteForce([3, 3], 6))

print(sol.twoSum([2, 7, 11, 15], 9))
print(sol.twoSum([3, 2, 4], 6))
print(sol.twoSum([3, 3], 6))

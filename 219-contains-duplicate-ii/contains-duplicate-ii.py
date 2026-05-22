class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        hashmap = {}

        for index, num in enumerate(nums):  
            if num in hashmap and abs(index - hashmap[num]) <= k: 
                return True
            hashmap[num] = index
        return False 
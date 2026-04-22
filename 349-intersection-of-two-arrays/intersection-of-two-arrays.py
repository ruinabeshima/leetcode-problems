class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        intersection = []
        nums_1_set = set(nums1)

        for num in nums2: 
            if num in nums_1_set: 
                intersection.append(num)
                nums_1_set.remove(num)
        
        return intersection 

        
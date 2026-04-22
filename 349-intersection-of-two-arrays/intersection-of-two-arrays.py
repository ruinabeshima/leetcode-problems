class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        intersection = []
        nums_1_set = set(nums1)
        nums_2_set = set(nums2)

        for num in nums_2_set: 
            if num in nums_1_set: 
                intersection.append(num)
        
        return intersection 

        
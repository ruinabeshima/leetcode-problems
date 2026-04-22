class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        nums1_dict = {} 
        intersection = []

        for num in nums1: 
            if num in nums1_dict: 
                nums1_dict[num] += 1 
            else: 
                nums1_dict[num] = 1

        for num in nums2: 
            if num in nums1_dict and nums1_dict[num] > 0: 
                intersection.append(num)
                nums1_dict[num] -= 1

        return intersection 

        
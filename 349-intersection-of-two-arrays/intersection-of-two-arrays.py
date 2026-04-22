class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        intersection = []
        nums_set = set()

        for num1 in nums1: 
            for num2 in nums2: 
                if num1 == num2: 
                    if num1 not in nums_set: 
                        nums_set.add(num1)

        for key in nums_set: 
            intersection.append(key)
        
        return intersection 

        
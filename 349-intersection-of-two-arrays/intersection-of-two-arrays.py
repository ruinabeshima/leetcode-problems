class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        intersection = [] 

        for num1 in nums1: 
            for num2 in nums2: 
                if num1 == num2: 
                    if num1 not in intersection: 
                        intersection.append(num1)
        
        return intersection 

        
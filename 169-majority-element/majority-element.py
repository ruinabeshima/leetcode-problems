class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        dict = {} 

        for num in nums: 
            dict[num] = dict.get(num, 0) + 1

        count = 0 
        max_key = 0 
        for key in dict: 
            if dict[key] > count: 
                count = dict[key]
                max_key = key

        return max_key
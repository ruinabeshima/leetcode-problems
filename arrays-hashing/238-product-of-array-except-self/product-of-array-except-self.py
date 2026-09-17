class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        res = [1 for i in range(len(nums))]

        # Prefix 
        res[0] = 1
        for i in range(1, len(nums)): 
            res[i] = res[i - 1] * nums[i - 1]

        # Postfix 
        postfix = 1 
        for j in range(len(nums) - 2, -1, -1): 
            postfix *= nums[j + 1]
            res[j] *= postfix

        return res

        
        
        


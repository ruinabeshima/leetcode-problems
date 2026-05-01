class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        left = 0 
        right = len(nums) - 1 

        while right >= left: 
            if nums[left] == val and nums[right] != val:
                nums[left] = nums[right]
                left += 1 
                right -= 1 
            elif nums[right] == val: 
                right -= 1 
            else: 
                left += 1 

        return left 
             
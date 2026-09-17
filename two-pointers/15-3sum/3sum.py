class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort() 
        output = [] 

        for curr in range(len(nums)):
            # Skipping duplicates
            if curr > 0 and nums[curr] == nums[curr - 1]: 
                continue 

            l, r = curr + 1, len(nums) - 1 
            while r > l: 
                curr_sum = nums[curr] + nums[l] + nums[r]
                if curr_sum == 0: 
                    output.append([nums[curr], nums[r], nums[l]])
                    l += 1 
                    r -= 1
                    # Avoid duplicates 
                    while nums[l] == nums[l - 1] and r > l: 
                        l += 1 
                    while nums[r] == nums[r + 1] and r > l: 
                        r -= 1 

                elif curr_sum < 0: 
                    l += 1 
                elif curr_sum > 0: 
                    r -= 1 
            
        
        return output 

            

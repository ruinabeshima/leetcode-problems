class Solution:
    def trap(self, height: List[int]) -> int:
        maxLeft = height[0]
        maxRight = height[len(height) - 1]

        l, r = 1, len(height) - 2 
        amount = 0 

        while l <= r: 
            if maxLeft <= maxRight:
                maxLeft= max(maxLeft, height[l])
                amount += maxLeft - height[l]
                l += 1 
            else: 
                maxRight = max(maxRight, height[r])
                amount += maxRight - height[r]
                r -= 1 


        return amount



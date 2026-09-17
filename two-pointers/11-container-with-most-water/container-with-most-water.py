class Solution:
    def maxArea(self, height: List[int]) -> int:
        maxArea = 0 
        left, right = 0, len(height) - 1 

        while right > left: 
            area = (right - left) * min(height[right], height[left])
            maxArea = max(maxArea, area)

            if height[right] < height[left]: 
                right -= 1 
            else: 
                left += 1 
        
        return maxArea
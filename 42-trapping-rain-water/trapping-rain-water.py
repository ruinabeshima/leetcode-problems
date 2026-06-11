class Solution:
    def trap(self, height: List[int]) -> int:
        # Finding max left 
        maxLeft = [0 for i in range(len(height))] 
        for i in range(1, len(height)):
            maxLeft[i] = max(maxLeft[i - 1], height[i - 1])
        
        # Finding max right 
        maxRight = [0 for i in range(len(height))] 
        for i in range(len(height) - 2, -1, -1):
            maxRight[i] =  max(maxRight[i + 1], height[i + 1])

        # Finding min 
        min_height = [0 for i in range(len(height))]
        for i in range(len(height)): 
            min_height[i] = min(maxLeft[i], maxRight[i])

        # Compare 
        amount = 0 
        for i in range(len(height)): 
            curr_amount = min_height[i] - height[i]
            if curr_amount > 0: 
                amount += curr_amount 

        return amount



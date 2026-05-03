class Solution:
    def numOfSubarrays(self, arr: List[int], k: int, threshold: int) -> int:
        count = 0 

        nums_sum = sum(arr[:k])
        if nums_sum / k >= threshold: 
            count += 1 
        
        for i in range(k, len(arr)): 
            nums_sum = nums_sum + arr[i] - arr[i - k]
            if nums_sum / k >= threshold: 
                count += 1 
        
        return count
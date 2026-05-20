class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left = 0
        right = len(numbers) - 1 

        while right > left: 
            if numbers[right] + numbers[left] == target:
                return [left + 1, right + 1]
            elif numbers[right] + numbers[left] > target: 
                right -= 1
            else: 
                left += 1 
            
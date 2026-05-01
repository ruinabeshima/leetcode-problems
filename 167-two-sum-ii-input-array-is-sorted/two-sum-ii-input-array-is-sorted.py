class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left = 0 
        right = len(numbers) - 1 

        while right >= left: 
            complement = target - numbers[right]
            if numbers[left] == complement:  
                return [left + 1, right + 1]
            elif complement > numbers[left]: 
                left += 1 
            else: 
                right -= 1 


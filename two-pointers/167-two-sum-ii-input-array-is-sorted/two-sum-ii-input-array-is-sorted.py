class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left = 0 
        right = len(numbers) - 1 

        while right > left: 
            curr_sum = numbers[right] + numbers[left]

            if curr_sum == target: 
                return [left + 1, right + 1]
            elif curr_sum > target: 
                right -= 1 
            elif curr_sum < target: 
                left += 1 
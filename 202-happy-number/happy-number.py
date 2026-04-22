class Solution:
    def isHappy(self, n: int) -> bool:
        num_set = set() 

        while n != 1: 
            sum = 0 
            for digit in str(n): 
                sum += int(digit) * int(digit)
            
            if sum in num_set: 
                return False 
            num_set.add(sum)
            n = sum 
        return True 

        
class Solution:
    def isHappy(self, n: int) -> bool:
        
        def next_val(num): 
            total = 0 
            while num: 
                digit = num % 10 
                # Extract last digit 
                total += digit * digit 
                num = num // 10 
                # Integer division - remove last digit 
            return total 

        slow = n 
        fast = next_val(n) 
        # Fast starts one step ahead 

        while fast != 1 and slow != fast: 
            slow = next_val(slow)
            fast = next_val(next_val(fast))

        return fast == 1 
    
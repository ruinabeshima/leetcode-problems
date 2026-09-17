class Solution:
    def validPalindrome(self, s: str) -> bool:
        def isPalindrome(left, right): 
            while right > left: 
                if s[right] != s[left]: 
                    return False 
                right -= 1 
                left += 1 
            return True 

        left = 0 
        right = len(s) - 1 
        while right > left: 
            if s[right] != s[left]: 
                return isPalindrome(left, right - 1) or isPalindrome(left + 1, right)
            right -= 1 
            left += 1 
        
        return True

class Solution:
    def isPalindrome(self, s: str) -> bool:
        t = "".join(char.lower() for char in s if char.isalnum())
        
        left = 0 
        right = len(t) - 1

        while left < right: 
            if t[left] != t[right]: 
                return False 
            left += 1 
            right -= 1 

        return True 
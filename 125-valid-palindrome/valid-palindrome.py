class Solution:
    def isPalindrome(self, s: str) -> bool:
        s = s.lower().strip() 
        left = 0 
        right = len(s) - 1 

        while right >= left: 
            if s[right].isalnum() and s[left].isalnum() and s[right] != s[left]: 
                return False 
            
            if s[right].isalnum() == False and s[left].isalnum() == True: 
                right -= 1 
            elif s[left].isalnum() == False and s[right].isalnum() == True: 
                left += 1 
            else: 
                left += 1 
                right -= 1
        return True 

        


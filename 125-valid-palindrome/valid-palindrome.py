class Solution:
    def isPalindrome(self, s: str) -> bool:
        left = 0 
        right = len(s) - 1 

        while right >= left: 
            if s[right].isalnum() == False and s[left].isalnum() == True: 
                right -= 1 
            elif s[left].isalnum() == False and s[right].isalnum() == True: 
                left += 1 
            elif s[left].isalnum() == False and s[right].isalnum() == False: 
                right -= 1 
                left += 1 
            else: 
                if s[right].lower() != s[left].lower(): 
                    return False 
                left += 1 
                right -= 1
        return True 

        


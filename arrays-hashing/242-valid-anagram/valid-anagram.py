class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t): 
            return False 

        s_set = {} 
        for char in s: 
            s_set[char] = s_set.get(char, 0) + 1 

        for char in t: 
            if char in s_set: 
                s_set[char] -= 1 
        
        for key in s_set: 
            if s_set[key] != 0: 
                return False 
        return True 
        
            

        
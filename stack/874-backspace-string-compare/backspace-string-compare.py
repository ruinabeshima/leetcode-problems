class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:
        i = len(s) -1 
        j = len(t) -1
        s_skip = 0 
        t_skip = 0

        while i >= 0 or j >= 0: 
            while i >= 0: 
                if s[i] == "#":
                    s_skip += 1 
                    i -= 1 
                elif s_skip > 0:
                    s_skip -= 1  
                    i -= 1 
                else: 
                    break
        
            while j >= 0: 
                if t[j] == "#":
                    t_skip += 1 
                    j -= 1 
                elif t_skip > 0:
                    t_skip -= 1  
                    j -= 1 
                else: 
                    break

            if i >= 0 and j >= 0:
                if s[i] != t[j]:
                    return False
            elif i >= 0 or j >= 0:
                return False

            i -= 1
            j -= 1

        return True                
class Solution:
    # O(n) time and O(n) space
    def attempt1(self, s: str, t: str) -> bool:  # type: ignore
        s_result = []
        t_result = []

        for char in s:
            if char != "#":
                s_result.append(char)
            elif s_result:
                s_result.pop()

        for char in t:
            if char != "#":
                t_result.append(char)
            elif t_result:
                t_result.pop()

        return s_result == t_result
    

    """
    What the fuck was this
    Review later
    """
    def attempt2(self, s: str, t: str) -> bool:  # type: ignore
        i = len(s) - 1 
        j = len(t) - 1 
        skip_s = 0 
        skip_t = 0 

        while i >= 0 or j >= 0: 
          while i >= 0: 
            if s[i] == "#": 
                i -= 1 
                skip_s += 1 
            elif skip_s != 0: 
              i -= 1
              skip_s -= 1 
            else: 
                break 
          

          while j >= 0: 
            if t[j] == "#": 
                skip_t += 1 
                j -= 1
            elif skip_t != 0: 
                j -= 1
                skip_t -= 1
            else: 
              break

          if i >= 0 and j >= 0:
            if s[i] != t[j]:
                return False
            elif i >= 0 or j >= 0:
                return False

          j -= 1 
          i -= 1 

        return True      


    


"""
Test Cases:
1. True
2. True
3. False
"""

sol = Solution()
print(sol.attempt1("ab#c", "ad#c"))
print(sol.attempt1("ab##", "c#d#"))
print(sol.attempt1("a#c", "b"))

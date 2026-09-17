class Solution:
    def countSubstrings(self, s: str) -> int:
        substrings = 0 

        for i in range(len(s)): 
            
            # Odd palindromes 
            left, right = i, i 
            while left >= 0 and right < len(s) and s[right] == s[left]: 
                substrings += 1
                left -= 1 
                right += 1 

            # Even palindroms 
            left, right = i, i + 1 
            while left >= 0 and right < len(s) and s[right] == s[left]: 
                substrings += 1
                left -= 1 
                right += 1 

        return substrings

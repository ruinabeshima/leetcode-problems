class Solution:
    def longestPalindrome(self, s: str) -> str:
        maxLength = 0 
        string = ""

        for i in range(len(s)): 
            left, right = i, i 
            while left >= 0 and right < len(s) and s[left] == s[right]: 
                if (right - left + 1) > maxLength: 
                    string = s[left:right + 1]
                    maxLength = right - left + 1
                left -= 1 
                right += 1 

            left, right = i, i + 1
            while left >= 0 and right < len(s) and s[left] == s[right]: 
                if (right - left + 1) > maxLength: 
                    string = s[left:right + 1]
                    maxLength = right - left + 1
                left -= 1 
                right += 1 

        return string
        



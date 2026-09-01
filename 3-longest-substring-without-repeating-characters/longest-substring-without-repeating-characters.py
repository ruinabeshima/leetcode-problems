class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        maxLength = 0 
        left = 0
        letters = set() 

        for right in range(len(s)): 
            while s[right] in letters: 
                letters.remove(s[left])
                left += 1 
            
            letters.add(s[right])
            maxLength = max(maxLength, right - left + 1)

        return maxLength


        


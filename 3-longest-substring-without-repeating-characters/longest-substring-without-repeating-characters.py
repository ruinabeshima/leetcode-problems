class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        left = -1 
        max_length = 0
        seen = {}  

        for right in range(len(s)):
            if s[right] in seen and seen[s[right]] > left: 
                left = seen[s[right]]
            
            seen[s[right]] = right 
            max_length = max(max_length, right - left)

        return max_length 

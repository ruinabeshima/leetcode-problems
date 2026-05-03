class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        left = -1 
        max_length = 0 

        for right in range(len(s)): 
            
            for j in range(left + 1, right): 
                if s[j] == s[right]:
                    left = j
                    break 

            max_length = max(max_length, right - left)

        return max_length

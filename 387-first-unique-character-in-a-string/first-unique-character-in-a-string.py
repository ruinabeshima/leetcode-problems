class Solution:
    def firstUniqChar(self, s: str) -> int:
        letter_dict = {} 

        for char in s: 
            letter_dict[char] = letter_dict.get(char, 0) + 1
        
        for i in range(0, len(s)): 
            if letter_dict[s[i]] == 1: 
                return i

        return -1
class Solution:
    def findTheDifference(self, s: str, t: str) -> str:
        s_dict = {} 

        for letter in s: 
            s_dict[letter] = s_dict.get(letter, 0) + 1

        for letter in t: 
            if letter not in s_dict: 
                return letter
            elif s_dict[letter] == 0: 
                return letter
            else: 
                s_dict[letter] -= 1 
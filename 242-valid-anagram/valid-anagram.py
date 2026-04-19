class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        letters_dict = {}

        for letter in s: 
            if letter in letters_dict: 
                letters_dict[letter] += 1 
            else: 
                letters_dict[letter] = 1


        for letter in t: 
            if letter not in letters_dict: 
                return False 

            if letter in letters_dict: 
                letters_dict[letter] -= 1
             
        
        for key in letters_dict: 
            if letters_dict[key] != 0: 
                return False 
        return True 

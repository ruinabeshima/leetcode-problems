class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        ransom_dict = {} 

        for letter in ransomNote: 
            ransom_dict[letter] = ransom_dict.get(letter, 0) + 1
        
        for letter in magazine:
            if letter in ransom_dict and ransom_dict[letter] > 0: 
                ransom_dict[letter] -= 1

        for key in ransom_dict: 
            if ransom_dict[key] != 0:
                return False 
        
        return True
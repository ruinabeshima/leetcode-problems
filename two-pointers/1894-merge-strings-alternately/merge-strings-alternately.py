class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        pointer_1 = 0 
        pointer_2 = 0 
        result = ""

        while pointer_1 < len(word1) and pointer_2 < len(word2): 
            result += word1[pointer_1]
            pointer_1 += 1 
            result += word2[pointer_2]
            pointer_2 += 1 

        result += word1[pointer_1:]
        result += word2[pointer_2:]

        return result
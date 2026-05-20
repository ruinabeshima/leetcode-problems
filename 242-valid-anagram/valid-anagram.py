class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t): 
            return False 

        hashMap = {} 

        for index, char in enumerate(s): 
            if char in hashMap: 
                hashMap[char] += 1 
            else: 
                hashMap[char] = 1

        for char in t: 
            if char in hashMap:
                hashMap[char] -= 1 

        for key in hashMap: 
            if hashMap[key] != 0: 
                return False 
        return True 
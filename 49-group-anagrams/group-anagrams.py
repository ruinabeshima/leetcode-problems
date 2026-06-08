class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        hashmap = {} 

        for str in strs: 
            letters = [0] * 26 

            for letter in str: 
                letters[ord(letter) - ord("a")] += 1 

            if tuple(letters) in hashmap: 
                hashmap[tuple(letters)].append(str)
            else: 
                hashmap[tuple(letters)] = [str] 

        
        return [hashmap[key] for key in hashmap]

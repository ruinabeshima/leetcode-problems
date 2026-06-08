class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        hashmap = defaultdict(list)

        for str in strs: 
            letters = [0] * 26 

            for letter in str: 
                letters[ord(letter) - ord("a")] += 1 
            hashmap[tuple(letters)].append(str)

        return list(hashmap.values())

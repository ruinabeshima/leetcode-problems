class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        hashmap = {} 

        for str in strs: 
            sorted_str = "".join(sorted(str))

            if sorted_str in hashmap: 
                hashmap[sorted_str].append(str)
            else: 
                hashmap[sorted_str] = [str] 

        
        return [hashmap[key] for key in hashmap]

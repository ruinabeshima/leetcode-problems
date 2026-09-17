class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        hashmap = defaultdict(list)
        result = [] 

        for string in strs: 
            sorted_string = "".join(sorted(string))
            hashmap[sorted_string].append(string)

        for key in hashmap: 
            result.append(hashmap[key])
        
        return result



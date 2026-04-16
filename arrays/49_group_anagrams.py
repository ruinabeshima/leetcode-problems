"""
Logic:
Loop through the array
for each word check if the other words are anagrams
add to array
for next word if its already in the array skip it
"""

from typing import List


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:  # type: ignore
        anagrams = {}
        response = []

        for word in strs:
            signature = "".join(sorted(word))
            if signature not in anagrams:
                anagrams[signature] = []
            anagrams[signature].append(word)

        # Returns all values in the dict as an array instead of another loop
        return list(anagrams.values())


"""
Test Cases:
1. [["bat"],["nat","tan"],["ate","eat","tea"]]
2. [[""]]
3. [["a"]]
"""

sol = Solution()
print(sol.groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
print(sol.groupAnagrams([""]))
print(sol.groupAnagrams(["a"]))

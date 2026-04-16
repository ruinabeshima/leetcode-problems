"""
Logic:
create a single dictionary with letters in S as keys, and how many times that letter appears as the value
subtract by one for each letter in T, and if every value in the dict is 0, then it is an anagram
O(n) time
"""


class Solution:
    # Dictionary - O(n) time
    def isAnagramWithDict(self, s: str, t: str) -> bool:  # type: ignore
        word = {}

        if len(s) != len(t):
            return False

        for letter in s:
            if letter in word:
                word[letter] += 1
            else:
                word[letter] = 1

        for letter in t:
            if letter in word:
                word[letter] -= 1
            else:
                return False

        # or "return all(val == 0 for val in word.values())"
        for letter in word:
            if word[letter] != 0:
                return False
        return True


"""
Test Cases:
1. True
2. False
3. True
"""

sol = Solution()
print(sol.isAnagramWithDict("anagram", "nagaram"))
print(sol.isAnagramWithDict("rat", "car"))
print(sol.isAnagramWithDict("listen", "silent"))

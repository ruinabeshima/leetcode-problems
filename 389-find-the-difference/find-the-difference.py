class Solution:
    def findTheDifference(self, s: str, t: str) -> str:
        return chr(sum(ord(letter) for letter in t) - sum(ord(letter) for letter in s))
class Solution:
    def isValid(self, s: str) -> bool:
        pairs = {"}":"{", ")":"(", "]":"["}
        stack = []

        for char in s: 
            if char in ["{", "[", "("]:
                stack.append(char)
            elif char in pairs and stack and stack[-1] == pairs[char]: 
                stack.pop()
            else: 
                return False 
            

        if stack: 
            return False
        return True 


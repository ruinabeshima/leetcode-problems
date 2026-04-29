class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:
        arr1 = []
        arr2 = [] 

        for char in s: 
            if char == "#" and len(arr1) > 0: 
                arr1.pop()
            elif char == "#" and len(arr1) == 0: 
                continue
            else: 
                arr1.append(char)

        for char in t: 
            if char == "#" and len(arr2) > 0: 
                arr2.pop()
            elif char == "#" and len(arr2) == 0: 
                continue
            else: 
                arr2.append(char)

        if len(arr1) != len(arr2): 
            return False

        for i in range(len(arr1)):
            if (arr1[i] != arr2[i]):
                return False 

        return True
    
            
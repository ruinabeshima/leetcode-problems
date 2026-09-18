class Solution:

    def encode(self, strs: List[str]) -> str:
        encoded_string = ""

        for s in strs: 
            encoded_string += str(len(s)) + "#" + s

        return encoded_string


    def decode(self, s: str) -> List[str]:
        decoded_strs = []

        i = 0 
        while i < len(s): 
            j = i 

            # Find length of string 
            while s[j] != "#": 
                j += 1 
            length = int(s[i:j])

            # Append string to list 
            decoded_strs.append(s[j + 1:j + length + 1])

            # Update i past the length prefix, the "#" and the payload 
            i = j + length + 1 

        return decoded_strs

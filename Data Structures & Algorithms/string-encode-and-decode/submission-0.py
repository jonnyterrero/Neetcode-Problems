from typing import List

class Solution:
    def encode(self, strs: List[str]) -> str:
        encoded = ""

        for s in strs:
            encoded += str(len(s)) + "#" + s

        return encoded

    def decode(self, s: str) -> List[str]:
        decoded = []
        i = 0

        while i < len(s):
            # Step 1: find the separator after the length
            j = i
            while s[j] != "#":
                j += 1

            # Step 2: extract the length
            length = int(s[i:j])

            # Step 3: extract the actual string
            start = j + 1
            end = start + length
            decoded.append(s[start:end])

            # Step 4: move pointer to next encoded string
            i = end

        return decoded
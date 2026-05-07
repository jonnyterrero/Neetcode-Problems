class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # If lengths differ, they cannot be anagrams
        if len(s) != len(t):
            return False

        count = {}

        # Count characters in s
        for char in s:
            if char in count:
                count[char] += 1
            else:
                count[char] = 1

        # Subtract characters using t
        for char in t:
            if char not in count:
                return False

            count[char] -= 1

            if count[char] < 0:
                return False

        return True
class Solution:
    def isPalindrome(self, s: str) -> bool:
        left = 0
        right = len(s) - 1

        while left < right:
            # Move left pointer until it points to a letter or digit
            while left < right and not s[left].isalnum():
                left += 1

            # Move right pointer until it points to a letter or digit
            while left < right and not s[right].isalnum():
                right -= 1

            # Compare characters case-insensitively
            if s[left].lower() != s[right].lower():
                return False

            # Move both pointers inward
            left += 1
            right -= 1

        return True
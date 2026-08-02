class Solution:
    def isValid(self, s: str) -> bool:
        """Return True when every bracket is correctly matched and ordered."""

        # Each closing bracket maps to the opening bracket it requires.
        matching: dict[str, str] = {
            ")": "(",
            "]": "[",
            "}": "{",
        }

        # Stores opening brackets that have not yet been closed.
        stack: list[str] = []

        for bracket in s:
            if bracket in matching:
                # A closing bracket cannot appear without an unmatched opener.
                if not stack:
                    return False

                most_recent_opening = stack.pop()

                # The most recently opened bracket must be closed first.
                if most_recent_opening != matching[bracket]:
                    return False
            else:
                # Under the problem constraints, this must be an opening bracket.
                stack.append(bracket)

        # Any remaining opening bracket was never closed.
        return len(stack) == 0
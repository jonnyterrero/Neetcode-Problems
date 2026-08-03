from typing import List


class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        """
        Return the number of days until a warmer temperature occurs.

        Time complexity: O(n)
        Space complexity: O(n)
        """
        number_of_days: int = len(temperatures)

        # result[i] remains 0 if no warmer future day exists.
        result: List[int] = [0] * number_of_days

        # The stack stores indices of unresolved days.
        # Their temperatures remain non-increasing from bottom to top.
        stack: List[int] = []

        for current_day, current_temperature in enumerate(temperatures):

            # Resolve every previous day whose temperature is lower
            # than the current temperature.
            while (
                stack
                and current_temperature > temperatures[stack[-1]]
            ):
                previous_day: int = stack.pop()

                # The difference in indices is the number of days waited.
                result[previous_day] = current_day - previous_day

            # This day now waits for its own future warmer day.
            stack.append(current_day)

        return result
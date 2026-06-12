from typing import List

class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left = 0
        right = len(numbers) - 1

        while left < right:
            current_sum = numbers[left] + numbers[right]

            if current_sum == target:
                # Return 1-indexed positions
                return [left + 1, right + 1]

            elif current_sum < target:
                # Need a larger sum
                left += 1

            else:
                # Need a smaller sum
                right -= 1
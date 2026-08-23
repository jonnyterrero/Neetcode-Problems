from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        """Return the index of target in nums, or -1 if target is absent."""

        left: int = 0
        right: int = len(nums) - 1

        while left <= right:
            # Find the midpoint of the current search interval.
            mid: int = left + (right - left) // 2

            # Case 1: target found.
            if nums[mid] == target:
                return mid

            # Case 2: target must be in the right half.
            if nums[mid] < target:
                left = mid + 1

            # Case 3: target must be in the left half.
            else:
                right = mid - 1

        # Search interval became empty.
        return -1
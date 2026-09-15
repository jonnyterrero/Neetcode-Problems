class Solution:
    def findMin(self, nums: list[int]) -> int:
        # Search interval that is guaranteed to contain the minimum.
        left = 0
        right = len(nums) - 1

        # Continue until only one candidate remains.
        while left < right:
            mid = left + (right - left) // 2

            # If mid is larger than the rightmost value,
            # the rotation point/minimum must be to the right.
            if nums[mid] > nums[right]:
                left = mid + 1

            # Otherwise, mid could itself be the minimum,
            # so keep mid and eliminate everything to its right.
            else:
                right = mid

        # left == right, so this index must contain the minimum.
        return nums[left]
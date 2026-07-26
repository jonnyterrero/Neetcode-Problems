class Solution:
    def trap(self, height: list[int]) -> int:
        """
        Return the total area of rainwater trapped between the bars.

        Time complexity: O(n)
        Space complexity: O(1)
        """
        if not height:
            return 0

        left: int = 0
        right: int = len(height) - 1

        left_max: int = 0
        right_max: int = 0
        trapped_water: int = 0

        while left <= right:
            # Record the tallest walls found from each direction.
            left_max = max(left_max, height[left])
            right_max = max(right_max, height[right])

            if left_max <= right_max:
                # A sufficiently tall right boundary is known to exist,
                # so the left side determines the water level here.
                trapped_water += left_max - height[left]
                left += 1
            else:
                # A sufficiently tall left boundary is known to exist,
                # so the right side determines the water level here.
                trapped_water += right_max - height[right]
                right -= 1

        return trapped_water


if __name__ == "__main__":
    solution = Solution()

    example: list[int] = [0, 2, 0, 3, 1, 0, 1, 3, 2, 1]
    result: int = solution.trap(example)

    print(f"Trapped water: {result}")
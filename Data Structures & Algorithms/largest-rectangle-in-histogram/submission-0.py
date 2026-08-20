from typing import List


class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        stack = []
        max_area = 0

        for i, height in enumerate(heights):
            start = i

            while stack and stack[-1][1] > height:
                index, previous_height = stack.pop()

                width = i - index
                area = previous_height * width

                max_area = max(max_area, area)

                start = index

            stack.append((start, height))

        n = len(heights)

        for index, height in stack:
            width = n - index
            area = height * width

            max_area = max(max_area, area)

        return max_area
from typing import List


class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        # The slowest possible eating speed.
        left = 1

        # Eating this fast guarantees every pile takes at most one hour.
        right = max(piles)

        # Search for the smallest feasible eating speed.
        while left < right:
            mid = left + (right - left) // 2

            hours_needed = 0

            # Determine how many hours Koko needs at speed `mid`.
            for pile in piles:
                hours_needed += (pile + mid - 1) // mid

            if hours_needed <= h:
                # mid works, but a smaller speed may also work.
                right = mid
            else:
                # mid is too slow, so eliminate it and everything below it.
                left = mid + 1

        # left == right is the smallest feasible speed.
        return left
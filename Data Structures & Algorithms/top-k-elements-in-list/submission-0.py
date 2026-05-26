from typing import List

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # Step 1: Count how often each number appears
        count = {}

        for num in nums:
            count[num] = count.get(num, 0) + 1

        # Step 2: Create buckets where index = frequency
        # Maximum possible frequency is len(nums)
        freq = [[] for _ in range(len(nums) + 1)]

        for num, occurrences in count.items():
            freq[occurrences].append(num)

        # Step 3: Collect the k most frequent elements
        result = []

        for occurrences in range(len(freq) - 1, 0, -1):
            for num in freq[occurrences]:
                result.append(num)

                if len(result) == k:
                    return result
class Solution(object):
    def twoSum(self, nuims, target):
        """
        :type nums: list[int]
        :type target: int
        :rtype: List[int]
        """

        seen = {}

        for i, num in enumerate(nuims):
            complement = target - num

            if complement in seen:
                return [seen[complement],i]

            seen[num] = i
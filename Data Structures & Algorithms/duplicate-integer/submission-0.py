class Solution(object):
    def hasDuplicate(self,nums):
        """
        :type nums List[int]
        :rtype:bool
        """

        seen = set()
        for num in nums:
            if num in seen:
                return True

            seen.add(num)
        return False

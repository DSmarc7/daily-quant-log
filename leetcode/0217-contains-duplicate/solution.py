class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        memo = set()
        for x in nums:
            if x in memo:
                return True
            memo.add(x)
        return False

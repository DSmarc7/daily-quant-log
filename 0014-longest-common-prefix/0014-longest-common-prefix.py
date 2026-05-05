class Solution(object):
    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        arr = strs
        arr.sort()

        # Get the first and last strings after sorting
        first = arr[0]
        last = arr[-1]
        minLength = min(len(first), len(last))

        i = 0
        # Find the common prefix between the first
        # and last strings
        while i < minLength and first[i] == last[i]:
            i += 1

        # Return the common prefix
        return first[:i]
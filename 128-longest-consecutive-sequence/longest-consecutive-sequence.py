class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums: 
            return 0

        # Convert to set 
        nums_set = set(nums)
        max_seq = 1

        for num in nums_set: 
            if num - 1 not in nums_set: 
                count = num 
                seq = 1 
                while count + 1 in nums_set: 
                    seq += 1 
                    count += 1 
                max_seq = max(seq, max_seq)

        return max_seq
class solution:
    def twoSum(nums, target):
        num_map = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_map:
                return [num_map[complement], i]
            num_map[num] = i
        return []
print(solution.twoSum([2,7,11,15],9))


# Brute Force Solution

class Solution:
    def twoSum(self, nums, target):
        print(f"Input: nums = {nums}, target = {target}")
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                print(f"Checking indices {i} and {j}: {nums[i]} + {nums[j]}")
                if nums[i] + nums[j] == target:
                    print(f"Found: {nums[i]} + {nums[j]} = {target}")
                    return [i, j]
        print("No two sum found")
        return []

print(Solution().twoSum([2, 7, 11, 15], 9))
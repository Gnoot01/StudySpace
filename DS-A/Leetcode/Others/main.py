def remove_element(nums, val):
    """
    Remove all occurrences of val in nums in-place and return the new length of the modified list
    No allocating extra memory space for another list or otherwise. S: O(1)
    Can only use in-built list method .pop()
    Eg. [-2, 1, -3, 4, -1, 2, 1, -5], 1 => 6, [1, 1, 1, 1, 1], 1 => 0 
    """
    i = 0
    while i < len(nums):
        if nums[i] == val:
            nums.pop(i)
        else:
            i += 1
    return len(nums)


def find_max_min(nums: list[int]):
    """
    Returns a tuple containing the maximum and minimum values in the list.
    """
    mini = maxi = nums[0]
    for num in nums:
        if num > maxi:
            maxi = num
        elif num < mini:
            mini = num
    return (maxi, mini)


def remove_duplicates(nums: list[int]):
    """
    Given a sorted non-decreasing list, rearrange so all unique elements appear at the beginning
    May contain duplicates, S: O(1), T: O(n)
    Eg. [] => 0, [1, 1, 1] => 1, [1, 2, 3] => 3, [1, 1, 2, 2, 3, 4, 5, 5] => 5
    """
    # My ans, better as can see exactly which are repeated aft the unique elements
    # Eg. [1, 1, 2, 2, 3, 4, 5, 5] => [1, 2, 3, 4, 5, 1, 2, 5]
    unique_count = 0
    if len(nums) > 0:
        unique_count += 1
        temp = nums[0]
        length = len(nums)
        i = 1
        iterations = 0
        while i < length and iterations < length - 1:
            # Diff num
            if nums[i] > temp:
                unique_count += 1
                temp = nums[i]
                i += 1
            else:
                nums.append(nums.pop(i))

            iterations += 1

    return unique_count

    # # Alternative (I don't understand)
    # # Eg. [1, 1, 2, 2, 3, 4, 5, 5] => [1, 2, 3, 4, 5, 4, 5, 5]
    # def remove_duplicates(nums):
    # if not nums:
    #     return 0

    # write_pointer = 1

    # for read_pointer in range(1, len(nums)):
    #     if nums[read_pointer] != nums[read_pointer - 1]:
    #         nums[write_pointer] = nums[read_pointer]
    #         write_pointer += 1

    # return write_pointer


def rotate(nums: list[int], k):
    """
    Move list to the right by k steps. In-place, no return
    """
    # Preventing overshot
    k = k % len(nums)
    # Moves last k elements to beginning of list, concatenated to remaining n-k elements
    nums[:] = nums[-k:] + nums[:-k]


def rotate(matrix):
    """
    Given n x n 2D matrix, rotate by 90 degrees clockwise. S: O(1)
    Eg. [[1,2,3],[4,5,6],[7,8,9]] => [[7,4,1],[8,5,2],[9,6,3]]
    123 456 789 => 147 256 389 => 147 258 369 => 741 852 963
    """
    n = len(matrix)

    # Transpose matrix
    for i in range(n):
        for j in range(i, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    for row in matrix:
        row.reverse()


def max_subarray(nums: list[int]):
    """
    Find contiguous subarray with largest sum and returns its sum
    """
    if not nums:
        return 0

    max_sum = curr_sum = nums[0]

    for num in nums[1:]:
        # Determines which number to start off with - bigger is preferred
        # Eg. [-2, 1, ...] continue with -1 or restart with 1
        curr_sum = max(num, curr_sum + num)
        max_sum = max(max_sum, curr_sum)

    return max_sum


def missing_number(nums, n):
    """
    Find the missing number in a given strictly increasing nums that is supposed to have up to n integers.
    """
    total = (n + 1) * (n // 2)
    return total - sum(nums)


def first_second(nums):
    """
    Find first, second best scores from nums, which may contain duplicates
    """
    max1 = max2 = float('-inf')
    for num in nums:
        if num > max1:
            max2 = max1
            max1 = num
        # *
        elif num > max2 and num != max1:
            max2 = num
    return max1, max2

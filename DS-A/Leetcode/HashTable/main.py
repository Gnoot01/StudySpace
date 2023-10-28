class HashTable:
    def __init__(self, size=7):
        self.data_map = [None] * size


def item_in_common(list1, list2):
    """
    Takee 2 lists as input and return True if there is at least one common item between the two lists, False otherwise.
    """
    # Basically testing on properties of HashTable -> searching = O(1)
    d = {}
    for ele in list1:
        d[ele] = True
    for ele in list2:
        if ele in d:
            return True
    return False


def find_duplicates(nums: list[int]):
    """
    Find all duplicates within a list
    """
    d = {}
    duplicates = []
    for num in nums:
        # NOT if not d[ele]! as KeyError 1
        if not d.get(num):
            d[num] = True
        else:
            duplicates.append(num)
    return duplicates

    # # Alternative
    # num_counts = {}
    # for num in nums: num_counts[num] = num_counts.get(num, 0) + 1
    # duplicates = [num for num, count in num_counts.items() if count > 1]
    # return duplicates


def first_non_repeating_char(string):
    """
    Finds the first non-repeating character in the given string. Else, returns None
    Eg. leetcode => l, hello => h,  lol => o, aabbcc => None
    """
    ch_counts = {}
    for ch in string:
        ch_counts[ch] = ch_counts.get(ch, 0) + 1
    for ch in string:
        if ch_counts[ch] == 1:
            return ch
    return None


def group_anagrams(strings: list):
    """
    Given list of lower-cased strings, group anagrams
    ["eat", "tea", "tan", "ate", "nat", "bat"] => [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
    ["abc", "cba", "bac", "foo", "bar"] => [['abc', 'cba', 'bac'], ['foo'], ['bar']]
    ["listen", "silent", "triangle", "integral", "garden", "ranged"] => [['listen', 'silent'], ['triangle', 'integral'], ['garden', 'ranged']]
    """
    # O(n)
    groups = {}
    for string in strings:
        # ate -> ['a', 'e', 't'] -> aet
        canonical = ''.join(sorted(string))
        if canonical in groups:
            groups[canonical].append(string)
        else:
            groups[canonical] = [string]
    return list(groups.values())

    # # Alternative O(n^2)
    # d = {}
    # groups = []
    # covered = []
    # for string in strings:
    #     d[string] = {}
    #     for ch in string: d[string][ch] = True

    # for i in range(len(strings)):
    #     string1 = strings[i]
    #     temp = [string1]
    #     for string2 in strings[i+1:]:
    #         if d[string1].keys() == d[string2].keys() and not string2 in covered:
    #             temp.append(string2)
    #             covered.append(string2)
    #     if not string1 in covered:
    #         covered.append(string1)
    #         groups.append(temp)
    # return groups

# Target: ALW somehow involve complement! Eg. target - ...


def two_sum(nums: list[int], target):
    """
    find the indices of two numbers in nums that add up to the target
    *In 1 pass through the array*
    Cannot iterate through others! Eg. d
    Eg. [5, 1, 7, 2, 9, 3], 10 => [1, 4], [10, 15, 5, 2, 8, 1, 7], 12 => [1, 2, 3, 4, 5], 10 => []
    """
    d = {}
    for i, num in enumerate(nums):
        if num in d:
            return [d[num], i]
        d[target - num] = i
    return []

    # # Similar model alternative
    # d = {}
    # for i, num in enumerate(nums):
    #     complement = target - num
    #     if complement in d:
    #         return [d[complement], i]
    #     d[num] = i
    # return []


def subarray_sum(nums: list[int], target):
    """"
    Finds the indices of a contiguous subarray in nums that add up to target
    [1, 2, 3, 4, 5], 9 => [1, 3], [1, 2, 3, 4, 5], 12 => [2, 4], [-1, 2, 3, -4, 5], 0 => [0, 3], [], 5 => []
    """
    # O(n)
    # Initialized as such so that if first num == target, returns -1 + 1 = 0 (index of first num)
    sums_d = {0: -1}
    current_sum = 0
    for i, num in enumerate(nums):
        current_sum += num
        if current_sum - target in sums_d:
            # if exceeded, gets index which made it exceed + 1
            return [sums_d[current_sum - target] + 1, i]
        sums_d[current_sum] = i
    return []

    # # O(n^2)
    # d = {}
    # for i, num_i in enumerate(nums):
    #     prev_complement = target - num_i
    #     d[prev_complement] = [i]
    #     # i+1 required to not re-visit past nums, thus also no need for if num_i == num_j: continue
    #     for j, num_j in enumerate(nums[i+1:]):
    #         new_complement = prev_complement - num_j
    #         # Cannot terminate early Eg. once <0, since -ves might be in nums too!
    #         # Eg. [1,2,3,4,-1], 9 => [0,4]
    #         d[new_complement] = d[prev_complement] + [j + i + 1]
    #         prev_complement = new_complement
    #     if d.get(0): return [d[0][0], d[0][-1]]

    # return []


# # USING SETS since O(1) for Eg. if ... in ... vs O(n) if list

def remove_duplicates(l):
    """
    Remove all duplicates from given list
    """
    return list(set(l))


def has_unique_chars(string):
    """
    Given a string, return True if all the characters are unique, False otherwise
    """
    return len(string) == len(set(string))


def find_pairs(l1, l2, target):
    """
    Find all pairs of numbers (1 from l1, 1 from l2 that sum up to target)
    Eg. [1, 2, 3, 4, 5], [2, 4, 6, 8, 10], 7 => [(5, 2), (3, 4), (1, 6)]
    """
    set1 = set(l1)
    pairs = []
    for num in l2:
        if target - num in set1:
            pairs.append((target - num, num))
    return pairs


def longest_consecutive_sequence(nums):
    """
    Given unsorted list, Find length of strictly increasing 
    """
    num_set = set(nums)
    longest_sequence = 0
    # **Still iterate thru list! num_set just for O(1) searching (in ...)
    for num in nums:
        # Ensure num is start of new sequence, not part of anth
        # Don't need account for strictly increasing + decreasing, since this
        # auto finds min in num_set to start increasing sequence from
        if num - 1 not in num_set:
            current_num = num
            current_sequence = 1

            while current_num + 1 in num_set:
                current_num += 1
                current_sequence += 1

            longest_sequence = max(longest_sequence, current_sequence)

    return longest_sequence

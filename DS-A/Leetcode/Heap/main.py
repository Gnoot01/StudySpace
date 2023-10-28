class MaxHeap:
    def __init__(self):
        self.heap = []


def find_kth_smallest(nums: list[int], k: int):
    """
    Find the kth smallest number in list
    List may contain duplicates, k is guaranteed to be within range of len(list)
    Challenge: find using MaxHeap
    Eg. [3, 2, 1, 5, 6, 4] , 2 => 2, [3,2,3,1,2,4,5,5,6], 7 => 5
    """

    max_heap = MaxHeap()
    for num in nums:
        max_heap.insert(num)
        # limits the size of the heap to k => At any point, heap only contains the smallest k numbers from the list
        if len(max_heap.heap) > k:
            max_heap.remove()
    # Returns kth smallest
    return max_heap.remove()

    # # Alternative
    # max_heap = MaxHeap()
    # for num in nums:
    #     max_heap.insert(num)
    # for _ in range(len(nums) - k + 1):
    #     kth_smallest = max_heap.remove()
    # return kth_smallest


def stream_max(nums: list[int]):
    """
    Return list of the same length, where each element is the maximum number seen so far
    Eg. [1, 2, 2, 1, 3, 3, 3, 2, 2] => [1, 2, 2, 2, 3, 3, 3, 3, 3], [-1, -2, -3, -4, -5] => [-1, -1, -1, -1, -1]
    """
    max_heap = MaxHeap()
    max_stream = []
    for num in nums:
        max_heap.insert(num)
        # .remove() is NOT the only way to get top value!
        max_stream.append(max_heap.heap[0])
    return max_stream

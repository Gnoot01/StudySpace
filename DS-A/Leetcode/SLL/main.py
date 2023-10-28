class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class SLL:
    def __init__(self, value):
        new_node = Node(value)
        self.head = new_node
        self.tail = new_node

    def append(self, value):
        new_node = Node(value)
        if self.head == None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        return True

    # **2 pointer techniques!
    def find_middle_node(self):
        """
        Return middle node in the linked list WITHOUT USING LENGTH.
        If the linked list has an even number of nodes, return the first node of the second half of the list.
        """
        slow = fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    #
    def has_loop(self):
        """
        Detect if linked list has a cycle/loop efficiently, using Floyd's cycle-finding algo

        """
        slow = fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False

    # **Dummy technique!
    def partition_list(self, x):
        """
        Take an integer x and partition the linked list such that all nodes with values < x come before nodes with values >= x.
        Preserve original relative order of the nodes
        Ignore tail pointer for this exercise
        Eg. partition_list(4): 2 → 8 → 1 → 4 → 3 → 7 => 2 → 1 → 3 → 8 → 4 → 7
        """
        if not self.head:
            return None

        dummy1 = Node(0)
        dummy2 = Node(0)
        prev1 = dummy1
        prev2 = dummy2
        curr_node = self.head

        while curr_node:
            if curr_node.value < x:
                prev1.next = curr_node
                prev1 = curr_node
            else:
                prev2.next = curr_node
                prev2 = curr_node
            curr_node = curr_node.next

        # Ending off 2nd linked list + combining into 1
        prev2.next = None
        prev1.next = dummy2.next
        self.head = dummy1.next

    #
    def remove_duplicates(self):
        """
        removes all duplicate values from the list, in-place
        Preserve original relative order of the nodes
        Ignore tail pointer for this exercise
        Eg. 1 → 2 → 3 → 3 → 2 → 4 => 1 → 2 → 3 → 4
        """
        nodes_set = set()
        curr_node = self.head
        before_node = None
        while curr_node:
            if curr_node.value in nodes_set:
                before_node.next = curr_node.next
                self.length -= 1
            else:
                nodes_set.add(curr_node.value)
                before_node = curr_node
            curr_node = curr_node.next

    #
    def binary_to_decimal(self):
        """
        Convert a binary number, represented as a linked list, to its decimal equivalent 
        Eg. 1010 => 10
        """
        curr_node = self.head
        decimal = 0
        while curr_node:
            self.length -= 1
            decimal += 2**(self.length) * curr_node.value
            # without using self.length, this shifts the bit to the left
            # num = num * 2 + current.value
            curr_node = curr_node.next
        return decimal

    #
    def reverse_between(self, start_i, end_i):
        """
        Reverse the nodes of the linked list from start_index to end_index (inclusive) in-place, time complexity O(n)
        Ignore tail pointer for this exercise
        Eg. reverse_between(1, 3): 1 → 2 → 3 → 4 → 5 => 1 → 4 → 3 → 2 → 5
        """
        if self.length <= 1:
            return
        dummy = Node(0)
        dummy.next = self.head
        before_node = dummy
        for _ in range(start_i):
            before_node = before_node.next

        curr_node = before_node.next
        for _ in range(end_i - start_i):
            after_node = curr_node.next
            curr_node.next = after_node.next
            after_node.next = before_node.next
            before_node.next = after_node
        self.head = dummy.next


#
def find_kth_from_end(linked_list, k):
    """
    Return the k-th node from the end of the linked list WITHOUT USING LENGTH
    Eg. find_kth_from_end(2): 1 → 2 → 3 → 4 => 3
    """
    slow = fast = linked_list.head
    # Moving fast k nodes ahead of slow
    for _ in range(k):
        # if fast becomes None, linked_list has < k nodes
        if fast is None:
            return None
        fast = fast.next

    # Advance slow & fast simultaneously, so slow will be at k when fast is at 2k
    while fast:
        slow = slow.next
        fast = fast.next
    return slow


def sum_reversed_lists(ll_a, ll_b):
    """
    2 numbers represented by linked list, where each node contains 1 digit stored in reverse (1's place is head)
    * Think of manually adding in table fashion => carry_over is needed 
    Eg. 7 -> 1 -> 6 + 5 -> 9 -> 2 = 617 + 295 = 912 => 2 -> 1 -> 9
    """
    curr_a = ll_a.head
    curr_b = ll_b.head
    carry_over = 0
    sll = SLL()
    while curr_a or curr_b:
        result = carry_over
        if curr_a:
            result += curr_a.value
            curr_a = curr_a.next
        if curr_b:
            result += curr_b.value
            curr_b = curr_b.next
        # Appending digitPlace as node
        sll.append(int(result % 10))
        # Moving onto next digitPlace
        carry_over = result / 10

    return sll


def intersection(ll_a, ll_b):
    """
    Given 2 SLL, determine where 2 they intersect.
    Intersection is defined based on reference, not value
    Eg. ✅ 9 -> 4 -> 2 -> 11(i) -> 14(i), 2 -> 0 -> 4 -> 7 -> 11(i) -> 14(i) => 11
        ❌ 9 -> 4 -> 2 -> 11(i) -> 14(i), 2 -> 0 -> 4 -> 7 -> 11(j) -> 14(j)
    """
    # Hint: Since after intersection every reference will be same, check tail reference if intersecting first!
    if ll_a.tail is not ll_b.tail:
        return False

    len_a = len(ll_a)
    len_b = len(ll_b)

    shorter = ll_a if len_a < len_b else ll_b
    longer = ll_b if len_a < len_b else ll_a

    diff = len(longer) - len(shorter)
    longer_node = longer.head
    shorter_node = shorter.head

    for _ in range(diff):
        longer_node = longer_node.next

    while shorter_node is not longer_node:
        shorter_node = shorter_node.next
        longer_node = longer_node.next

    return longer_node

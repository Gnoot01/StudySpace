class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class DLL:
    def __init__(self, value):
        new_node = Node(value)
        self.head = new_node
        self.tail = new_node
        self.length = 1

    def is_palindrome(self):
        """
        [1, 2, 3, 2, 1] => True
        [1, 2, 3, 4, 5] => False
        """
        if self.length <= 1:
            return True
        forward_node = self.head
        backward_node = self.tail
        for _ in range(self.length // 2):
            if forward_node.value != backward_node.value:
                return False
            forward_node = forward_node.next
            backward_node = backward_node.prev
        return True

    def reverse(self):
        # Same as SLL reverse, except .prev
        # Swap head & tail
        temp = self.head
        self.head = self.tail
        self.tail = temp
        # before_node, temp, after_node
        before_node = None
        for _ in range(self.length):
            after_node = temp.next
            temp.next = before_node
            temp.prev = after_node
            before_node = temp
            temp = after_node

        # # Alternative
        # curr_node = self.head
        # while curr_node:
        #     curr_node.prev, curr_node.next = curr_node.next, curr_node.prev
        #     curr_node = curr_node.prev
        # self.head, self.tail = self.tail, self.head

    def swap_pairs(self):
        """
        1 <-> 2 <-> 3 <-> 4 => 2 <-> 1 <-> 4 <-> 3
        1 <-> 2 <-> 3 <-> 4 <-> 5 => 2 <-> 1 <-> 4 <-> 3 <-> 5
        """
        curr_node = self.head
        # To rmbr head and point back to head easily at end
        dummy_node = Node(0)
        dummy_node.next = curr_node
        before_node = dummy_node

        while curr_node and curr_node.next:
            second_node = curr_node.next
            # Swapping next
            before_node.next = second_node
            curr_node.next = second_node.next
            second_node.next = curr_node
            # Swapping prev
            second_node.prev = before_node
            curr_node.prev = second_node

            if curr_node.next:
                curr_node.next.prev = curr_node

            before_node = curr_node
            curr_node = curr_node.next

        self.head = dummy_node.next

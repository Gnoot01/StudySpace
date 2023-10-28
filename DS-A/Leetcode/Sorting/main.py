class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self, value):
        new_node = Node(value)
        self.head = new_node
        self.tail = new_node
        self.length = 1

    def bubble_sort(self):
        """
        Bubble sort linked list in ascending order. 
        No other data structures shld be used, may contain duplicates.
        * Swap values, no need to account for pointers! (.next)
        Eg. [4,2,6,5,1,3] => [4,2,5,1,3,6] => [4,2,1,3,5,6] ..=> [1,2,3,4,5,6]
        """
        if self.length < 2:
            return
        sorted_until = None

        while sorted_until != self.head.next:
            curr_node = self.head
            # Since elements aft sorted_until are alr sorted
            while curr_node.next != sorted_until:
                after_node = curr_node.next
                if curr_node.value > after_node.value:
                    curr_node.value, after_node.value = after_node.value, curr_node.value
                curr_node = curr_node.next
            # sorted_until = 6 => 5 => 4 => 3 => 2
            sorted_until = curr_node

    def selection_sort(self):
        """
        Selection sort linked list in ascending order. 
        No other data structures shld be used, may contain duplicates.
        * Swap values, no need to account for pointers! (.next)
        Eg. [4,2,6,5,1,3] => [1,2,6,5,4,3] => [1,2,6,5,4,3] ..=> [1,2,3,4,5,6]
        """
        if self.length < 2:
            return
        curr_node = self.head
        while curr_node.next:
            smallest_node = curr_node
            inner_current = curr_node.next

            while inner_current:
                if inner_current.value < smallest_node.value:
                    smallest_node = inner_current
                inner_current = inner_current.next

            if smallest_node != curr_node:
                curr_node.value, smallest_node.value = smallest_node.value, curr_node.value
            curr_node = curr_node.next
        self.tail = curr_node

    def insertion_sort(self):
        """
        Insertion sort linked list in ascending order. 
        No other data structures shld be used, may contain duplicates.
        * Swap values, no need to account for pointers! (.next)
        Eg. [4,2,6,5,1,3] => [1,2,6,5,4,3] => [1,2,6,5,4,3] ..=> [1,2,3,4,5,6]
        """
        if self.length < 2:
            return

        sorted_list_head = self.head
        unsorted_list_head = self.head.next
        sorted_list_head.next = None

        while unsorted_list_head:
            curr_node = unsorted_list_head
            unsorted_list_head = unsorted_list_head.next

            if curr_node.value < sorted_list_head.value:
                curr_node.next = sorted_list_head
                sorted_list_head = curr_node
            else:
                search_pointer = sorted_list_head
                while search_pointer.next and curr_node.value > search_pointer.next.value:
                    search_pointer = search_pointer.next
                curr_node.next = search_pointer.next
                search_pointer.next = curr_node

        self.head = sorted_list_head
        temp = self.head
        while temp.next:
            temp = temp.next
        self.tail = temp

    def merge(self, other_list):
        """
        Takes another linkedlist and merges it with current, in ascending order
        """
        dummy_node = Node(0)
        # curr_node to keep track of position in merged
        # ** THIS MEANS initially, dummy_node & curr_node are both pointers to the same node, same chain. ∴ while curr_node moves, dummy_node stays but points to same growing chain
        curr_node = dummy_node
        other_head = other_list.head

        # Moving self.head is SMART as the rest would be auto-connected to it
        while self.head and other_head:
            if self.head.value < other_head.value:
                curr_node.next = self.head
                self.head = self.head.next
            else:
                curr_node.next = other_head
                other_head = other_head.next
            curr_node = curr_node.next

        # NO NEED WHILE LOOP HERE! as self.head auto connects the rest
        # If first list still has nodes left
        if self.head:
            curr_node.next = self.head
        # else second list still has nodes left
        else:
            curr_node.next = other_head
            self.tail = other_list.tail

        # ** THATS WHY able to do this
        self.head = dummy_node.next
        self.length += other_list.length

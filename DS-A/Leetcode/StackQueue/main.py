class Stack:
    def __init__(self):
        self.stack_list = []

    def print_stack(self):
        for i in range(len(self.stack_list)-1, -1, -1):
            print(self.stack_list[i])

    def peek(self):
        return None if self.is_empty else self.stack_list[-1]

    def push(self, value):
        self.stack_list.append(value)

    def pop(self):
        return None if self.is_empty else self.stack_list.pop()

    @property
    def size(self):
        return len(self.stack_list)

    @property
    def is_empty(self):
        return len(self.stack_list) == 0


def is_balanced_parentheses(parentheses: str):
    """
    Check if a parentheses string is balanced
    """
    stack = Stack()
    for ch in parentheses:
        if ch == "(":
            stack.push(ch)
        # Eg. ())
        elif stack.is_empty or stack.pop() != "(":
            return False
    # Eg. (()
    return stack.is_empty


def reverse_string(string):
    """
    Reverse a given string
    """
    stack = Stack()
    reversed = ""
    for ch in string:
        stack.push(ch)
    while not stack.is_empty():
        reversed += stack.pop()
    return reversed


def sort_stack(input_stack: Stack):
    """
    Sorted in ascending order: lowest at top -> highest at bottom
    Only allowed to use 1 additional stack
    """
    # input_stack = ascending => sorted_stack = descending
    sorted_stack = Stack()
    # Only 1 additional stack, but use variables to hold extra!
    while not input_stack.is_empty():
        temp = input_stack.pop()
        while not sorted_stack.is_empty() and sorted_stack.peek() > temp:
            input_stack.push(sorted_stack.pop())
        sorted_stack.push(temp)
    while not sorted_stack.is_empty():
        input_stack.push(sorted_stack.pop())

    # 2                                                                   5      1
    # 4             2          5    1      3             1      2         4      2
    # 5        5    4          4    2      2      2      3      3         3      3
    # 1      1 4    5          2    4      4      4 3    4      4         2      4
    # 3 ..-> 3 2 -> 3 1 ..-> 3 1 -> 5 3 -> 5 1 -> 5 1 -> 5 2 -> 5 1 ..->  1 ..-> 5

    # Lastly, Queue using double stacks...

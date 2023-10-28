class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def dfs_in_order(self):
        results = []

        def traverse(current_node):
            if current_node.left is not None:
                traverse(current_node.left)
            results.append(current_node.value)
            if current_node.right is not None:
                traverse(current_node.right)
        traverse(self.root)
        return results

    def inorder(self, curr_node, results):
        if curr_node:
            self.inorder(curr_node.left, results)
            results.append(curr_node.value)
            self.inorder(curr_node.right, results)
        return results

    def is_valid_bst(self):
        """
        Assuming unique values only in tree (no duplicates), check if BST is valid
        valid BST: in-order traversal should give strictly increasing values
        """
        vals = self.dfs_in_order()
        prev = vals[0]
        for val in vals[1:]:
            if val <= prev:
                return False
            prev = val
        return True

    def kth_smallest(self, k):
        """
        Given BST, find kth smallest element in BST
        2 Approaches: Iterative + Stack / Recursive
        In-order traversal!
        Eg. [5,3,7,2,4,6,8], 1/3/6 => 2/4/7
        """
        # Iterative + Stack: O(height + k)
        stack = []
        curr_node = self.root
        # As curr_node may be None due to leaf having 0 children
        while stack or curr_node:
            while curr_node:
                stack.append(curr_node)
                # Gets to min value
                curr_node = curr_node.left

            # Pops to trace back to root route
            curr_node = stack.pop()
            k -= 1
            if k == 0:
                return curr_node.value
            # Enables in-order traversal
            curr_node = curr_node.right

        return None

        # # Recursive
        # self.kth_smallest_count = 0
        # return self.__kth_smallest_helper(self.root, k)

        # # O(n) as every node is traversed first
        # vals = self.inorder(self.root, [])
        # # Ensuring valid k values (positive) & non-empty list
        # if k <= len(vals) and k-1 >= 0 and len(vals) > 0:
        #     return vals[k-1]
        # return None

    def __kth_smallest_helper(self, curr_node, k):
        if not curr_node:
            return None

        left_result = self.__kth_smallest_helper(curr_node.left, k)
        if left_result:
            return left_result

        self.kth_smallest_count += 1
        if self.kth_smallest_count == k:
            return curr_node.value

        right_result = self.__kth_smallest_helper(curr_node.right, k)
        if right_result:
            return right_result

        return None

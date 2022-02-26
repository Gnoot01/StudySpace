public class Node {
    int data;
    Node left;
    Node right;

    Node(int data) {
        this.data = data;
    }
}

import java.util.LinkedList;
import java.util.Queue;
import java.util.Stack;

public class BinarySearchTree {
    Node root;

    boolean search(int key) {
        while (root != null) {
            if (key < root.data) root = root.left;
            else if (key > root.data) root = root.right;
            else return true;
        }
        return false;
    }

    void insert(int key) {
        Node node = new Node(key);
        if (root == null) {
            root = node;
            return;
        }
        Node parent = null;
        Node temp = root;
        // Traversing to correct position
        while (temp != null) {
            if (temp.data > key) {
                parent = temp;
                temp = temp.left;
            } else if (temp.data < key) {
                parent = temp;
                temp = temp.right;
            }
        }
        if (parent.data > key) parent.left = node;
        else parent.right = node;
    }

    void delete(int key) {
        Node parent = null;
        Node curr = root;
        // Search key and set its parent pointer
        while (curr != null && curr.data != key) {
            parent = curr;
            if (key < curr.data) curr = curr.left;
            else curr = curr.right;
        }
        // Key not found

        if (curr == null) return;
        // Case 1: Node to delete has no children
        if (curr.left == null && curr.right == null) {
            // if tree is only 1 node, set it to null
            if (curr == root) root = null;
            else {
                // if leaf node, release node from parent's left/right respectively
                if (parent.left == curr) parent.left = null;
                else parent.right = null;
            }
        }

        // Case 2: Node has two children. Copy the successor to the node. Apply case 1/3 to delete that successor
        // Successor: deleted node's right subtree's leftMOST child (right-left/left-right to ensure closest value replaces deleted node)
        else if (curr.left != null && curr.right != null) {
            parent = null;
            Node successor = curr.right;
            while (successor.left != null) {
                parent = successor;
                successor = successor.left;
            }
            if (parent != null) parent.left = successor.right;  // Dont understand these 2 parts, isnt it the same as
            else curr.right = successor.right;                  // = to null?
            curr.data = successor.data;
        }

        // Case 3: Node has a single child node. Release the node and replace it with its child, so the child holds the deleted node's place in the tree
        else {
            Node child = null;
            // if deleted node had right child only
            if (curr.left == null) child = curr.right;
                // if deleted node had left child only
            else child = curr.left;
            // if root isn't the deleted node with 1 child
            if (curr != root) {
                if (curr == parent.left) parent.left = child;
                else parent.right = child;
            } else root = child;
        }
    }

    //(Root, Left, Right)
    void printPreorder(Node node) {
        if (node == null) return;
        System.out.print(node.data + " ");
        printPreorder(node.left);
        printPreorder(node.right);
    }

    //Recursive: (Left, Root, Right)
    //Iterative with stack
    void printInorder(Node node) {
        Node temp = node;
        Stack<Node> stack = new Stack<>();
        while (temp != null || !stack.isEmpty()) {
            if (temp != null) {
                stack.add(temp);
                temp = temp.left;
            } else {
                temp = stack.pop();
                System.out.print(temp.data + " ");
                temp = temp.right;
            }
        }
        System.out.println();
    }

    //Iterative without stack
    void morrisInorderTraversal(Node node) {
        // leftSuccessor = from left subtree, rightMost node = inorder predecessor = comes before curr in sorted order
        Node leftSuccessor;
        Node curr = node;
        if (curr == null) return;
        while (curr != null) {
            if (curr.left == null) {
                System.out.print(curr.data + " ");
                curr = curr.right;
            } else {
                // Find curr's leftSuccessor
                leftSuccessor = curr.left;
                while (leftSuccessor.right != null && leftSuccessor.right != curr)
                    leftSuccessor = leftSuccessor.right;
                //Make curr as right child of its leftSuccessor
                if (leftSuccessor.right == null) {
                    leftSuccessor.right = curr;
                    curr = curr.left;
                }
                // Revert the tree
                else {
                    leftSuccessor.right = null;
                    System.out.print(curr.data + " ");
                    curr = curr.right;
                }
            }
        }
        System.out.println();
    }

    //(Left, Right, Root)
    void printPostorder(Node node) {
        if (node == null) return;
        printPostorder(node.left);
        printPostorder(node.right);
        System.out.print(node.data + " ");
    }

    // via BFS
    void printLevelorder(Node node) {
        if (node == null) return;
        Queue<Node> queue = new LinkedList<>();
        queue.add(node);
        while (!queue.isEmpty()) {
            // Poll removes head
            Node curr = queue.poll();
            System.out.print(curr.data + " ");
            /*Enqueue left child */
            if (curr.left != null) queue.add(curr.left);
            /*Enqueue right child */
            if (curr.right != null) queue.add(curr.right);
        }
    }
}

public class Main {
    public static void main(String[] args) {
        BinarySearchTree tree = new BinarySearchTree();
        tree.insert(13);
        tree.insert(15);
        tree.insert(20);
        tree.insert(18);
        tree.insert(26);
        tree.insert(22);
        tree.insert(24);
        tree.insert(25);
        tree.insert(17);
        tree.printPostorder(tree.root);
        tree.printInorder(tree.root);
        tree.printLevelorder(tree.root);

    }
}

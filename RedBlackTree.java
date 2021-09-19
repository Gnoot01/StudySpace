// I find RBT difficult to implement in code, and write in my notes. Hence, I shall leave this here for future reviews, but link to this in my notes.

// https://www.geeksforgeeks.org/red-black-tree-set-2-insert/ , modified
public class RBT {
    public Node root;//root node

    public RBT() {
        root = null;
    }

    Node rotateLeft(Node node) {
        Node x = node.right;
        Node y = x.left;
        x.left = node;
        node.right = y;
        node.parent = x; // parent resetting is also important.
        if (y != null) y.parent = node;
        return (x);
    }

    Node rotateRight(Node node) {
        Node x = node.left;
        Node y = x.right;
        x.right = node;
        node.left = y;
        node.parent = x;
        if (y != null) y.parent = node;
        return (x);
    }

    public void insert(int data) {
        // Case 1: If tree is empty, create newNode as root B.
        if (this.root == null) {
            this.root = new Node(data);
            this.root.colour = 'B';
        } else this.root = insertHelp(this.root, data);
    }

    // Respective rotations are performed during traceback.
    // rotations are done if flags are true.
    boolean LL = false;
    boolean RR = false;
    boolean LR = false;
    boolean RL = false;

    // .left & .right here is sibling
    Node insertHelp(Node newNode, int data) {
        // conflict=true when RR conflict
        boolean conflict = false;

        if (newNode == null) return (new Node(data));
            // Case 2: If tree is not empty, create newNode as leaf R.
        else if (data < newNode.data) {
            newNode.left = insertHelp(newNode.left, data);
            newNode.left.parent = newNode;
            if (newNode != this.root) {
                if (newNode.colour == 'R' && newNode.left.colour == 'R')
                    conflict = true;
            }
        } else {
            newNode.right = insertHelp(newNode.right, data);
            newNode.right.parent = newNode;
            if (newNode != this.root) {
                if (newNode.colour == 'R' && newNode.right.colour == 'R')
                    conflict = true;
            }
        }

        // Rotation
        if (this.LL) // for left rotate.
        {
            newNode = rotateLeft(newNode);
            newNode.colour = 'B';
            newNode.left.colour = 'R';
            this.LL = false;
        } else if (this.RR) // for right rotate
        {
            newNode = rotateRight(newNode);
            newNode.colour = 'B';
            newNode.right.colour = 'R';
            this.RR = false;
        } else if (this.RL)  // for right and then left
        {
            newNode.right = rotateRight(newNode.right);
            newNode.right.parent = newNode;
            newNode = rotateLeft(newNode);
            newNode.colour = 'B';
            newNode.left.colour = 'R';

            this.RL = false;
        } else if (this.LR)  // for left and then right.
        {
            newNode.left = rotateLeft(newNode.left);
            newNode.left.parent = newNode;
            newNode = rotateRight(newNode);
            newNode.colour = 'B';
            newNode.right.colour = 'R';
            this.LR = false;
        }

        if (conflict) {
            if (newNode.parent.right == newNode) {
                // Parent's sibling is B
                if (newNode.parent.left == null || newNode.parent.left.colour == 'B') {
                    if (newNode.left != null && newNode.left.colour == 'R')
                        this.RL = true;
                    else if (newNode.right != null && newNode.right.colour == 'R')
                        this.LL = true;
                } else { // case when parent's sibling is R
                    newNode.parent.left.colour = 'B';
                    newNode.colour = 'B';
                    if (newNode.parent != this.root)
                        newNode.parent.colour = 'R';
                }
            } else {
                if (newNode.parent.right == null || newNode.parent.right.colour == 'B') {
                    if (newNode.left != null && newNode.left.colour == 'R')
                        this.RR = true;
                    else if (newNode.right != null && newNode.right.colour == 'R')
                        this.LR = true;
                } else {
                    newNode.parent.right.colour = 'B';
                    newNode.colour = 'B';
                    if (newNode.parent != this.root)
                        newNode.parent.colour = 'R';
                }
            }
            conflict = false;
        }
        return (newNode);
    }

    /////////////////////////////////////////////////////////////////////////////////////////////////
    // helper function to print inorder traversal
    void inorderTraversalHelper(Node node) {
        if (node != null) {
            inorderTraversalHelper(node.left);
            System.out.printf("%d ", node.data);
            inorderTraversalHelper(node.right);
        }
    }

    //function to print inorder traversal
    public void inorderTraversal() {
        inorderTraversalHelper(this.root);
    }

    // helper function to print the tree.
    void printTreeHelper(Node root, int space) {
        int i;
        if (root != null) {
            space = space + 10;
            printTreeHelper(root.right, space);
            System.out.printf("\n");
            for (i = 10; i < space; i++) {
                System.out.printf(" ");
            }
            System.out.printf("%d", root.data);
            System.out.printf("\n");
            printTreeHelper(root.left, space);
        }
    }

    // function to print the tree.
    public void printTree() {
        printTreeHelper(this.root, 0);
    }
}

// Deleting method: https://www.geeksforgeeks.org/red-black-tree-set-3-delete-2/
// RBT using keys, generics and other stuff a little tough to understand as of now: https://algs4.cs.princeton.edu/33balanced/RedBlackBST.java.html

// YT vid explaining how RBT works: 
// https://www.youtube.com/watch?v=qA02XWRTBdw&list=PLdo5W4Nhv31bbKJzrsKfMpo_grxuLl8LU&index=68
// https://www.youtube.com/watch?v=w5cvkTXY0vQ&list=PLdo5W4Nhv31bbKJzrsKfMpo_grxuLl8LU&index=66

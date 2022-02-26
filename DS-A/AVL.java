public class AVL<T extends Comparable<T>> {

    public class Node implements TreePrinter.PrintableNode {
        int BF;
        T data;
        int height;
        Node left, right;

        public Node(T data) {
            this.data = data;
        }

        @Override
        public TreePrinter.PrintableNode getLeft() {
            return left;
        }

        @Override
        public TreePrinter.PrintableNode getRight() {
            return right;
        }

        @Override
        public String getText() {
            return data.toString();
        }
    }

    Node root;

    // Tree containing a single node has a height of 0.
    public int height() {
        return (root == null) ? 0 : root.height;
    }

    // Return true/false depending on whether a value exists in the tree.
    public boolean contains(Node node, T data) {
        if (node == null) return false;

        int cmp = data.compareTo(node.data);
        // Left subtree
        if (cmp < 0) return contains(node.left, data);
        //Right subtree
        if (cmp > 0) return contains(node.right, data);
        return true;
    }

    // Update node's height and BF
    private void update(Node node) {
        int leftNodeHeight = (node.left == null) ? -1 : node.left.height;
        int rightNodeHeight = (node.right == null) ? -1 : node.right.height;

        // Update this node's height.
        node.height = 1 + Math.max(leftNodeHeight, rightNodeHeight);

        // Update balance factor.
        node.BF = rightNodeHeight - leftNodeHeight;
    }

    private Node balance(Node node) {
        // Left heavy subtree
        if (node.BF == -2) {
            // LL
            if (node.left.BF <= 0) return LL(node);
                // LR
            else return LR(node);

            // Right heavy subtree
        } else if (node.BF == +2) {
            // RR
            if (node.right.BF >= 0) return RR(node);
                // RL
            else return RL(node);

        }
        // BF = -1/0/+1
        return node;
    }

    // Rightmost left subtree
    private T findMax(Node node) {
        while (node.right != null) node = node.right;
        return node.data;
    }

    // Leftmost right subtree
    private T findMin(Node node) {
        while (node.left != null) node = node.left;
        return node.data;
    }

    private Node rotateLeft(Node node) {
        Node newParent = node.right;
        node.right = newParent.left;
        newParent.left = node;
        update(node);
        update(newParent);
        return newParent;
    }

    private Node rotateRight(Node node) {
        Node newParent = node.left;
        node.left = newParent.right;
        newParent.right = node;
        update(node);
        update(newParent);
        return newParent;
    }

    // Rotation Cases
    private Node LL(Node node) {
        return rotateRight(node);
    }

    private Node LR(Node node) {
        node.left = rotateLeft(node.left);
        return LL(node);
    }

    private Node RR(Node node) {
        return rotateLeft(node);
    }

    private Node RL(Node node) {
        node.right = rotateRight(node.right);
        return RR(node);
    }

    // Insertion
    public boolean insert(T data) {
        if (data == null) return false;
        if (!contains(root, data)) {
            root = insert(root, data);
            return true;
        }
        return false;
    }

    private Node insert(Node node, T data) {
        if (node == null) return new Node(data);

        int cmp = data.compareTo(node.data);
        if (cmp < 0) node.left = insert(node.left, data);
        else node.right = insert(node.right, data);
        update(node);
        // Re-balance tree if BF +-2
        return balance(node);
    }

    // Deletion
    public boolean delete(T data) {
        if (data == null) return false;
        if (contains(root, data)) {
            root = delete(root, data);
            return true;
        }
        return false;
    }

    private Node delete(Node node, T data) {
        if (node == null) return null;

        int cmp = data.compareTo(node.data);
        if (cmp < 0) node.left = delete(node.left, data);
        else if (cmp > 0) node.right = delete(node.right, data);
            // Found
        else {

            // Has right subtree or no subtree. Simply swap with delete node
            if (node.left == null) {
                return node.right;

                // Has left subtree or no subtree. Simply swap with delete node
            } else if (node.right == null) {
                return node.left;

                // 2 subtrees. Simply swap with Leftmost right subtree/ Rightmost left subtree
                // Best choice to remove from longer subtree to help with balancing
            } else {

                // Rightmost left subtree
                if (node.left.height > node.right.height) {
                    // Swapping & Deleting
                    T successorValue = findMax(node.left);
                    node.data = successorValue;
                    node.left = delete(node.left, successorValue);

                    // Leftmost right subtree
                } else {
                    // Swapping & Deleting
                    T successorValue = findMin(node.right);
                    node.data = successorValue;
                    node.right = delete(node.right, successorValue);
                }
            }
        }
        update(node);
        return balance(node);
    }

    @Override
    public String toString() {
        return TreePrinter.getTreeDisplay(root);
    }
}
    public static void main(String[] args) {
        AVL<Integer> tree = new AVL<>();
        tree.insert(14);
        tree.insert(17);
        tree.insert(11);
        tree.insert(7);
        tree.insert(53);
        tree.insert(4);
        tree.insert(13);
        tree.insert(12);
        tree.insert(8);
        tree.insert(60);
        tree.insert(19);
        tree.insert(16);
        tree.insert(20);
        tree.delete(8);
        tree.delete(7);
        tree.delete(11);
        tree.delete(14);
        tree.delete(17);

        System.out.println(tree);
    }

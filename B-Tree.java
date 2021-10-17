/* https://www.geeksforgeeks.org/insert-operation-in-b-tree/?ref=lbp
There is an alternative insertion algorithm from the Cormen book, where before going down to a node, we split it if it is full. (proactive) 
+: never traverse a node twice. -: may do unnecessary splits.
If we don’t split a node before going down to it and split it only if a new key is inserted (reactive),
we may end up traversing all nodes again from leaf to root, when all nodes on the path from the root to leaf are full, causing a cascading splitting effect
*/

class Node {

    int order;
    int[] keys;
    int count; // count of keys in a node
    Node[] children;
    boolean isLeaf;

    public Node(int order, boolean isLeaf) {

        this.order = order;
        this.isLeaf = isLeaf;
        this.keys = new int[2 * this.order - 1]; // Node has 2*order-1 keys at most
        this.children = new Node[2 * this.order];
        this.count = 0;
    }

    // Find the first location index equal to or greater than key
    public int findKey(int key) {

        int index = 0;
        // The conditions for exiting the loop are: 1.index == count, i.e. scan all of them once
        // 2. index < count, i.e. key found or greater than key
        while (index < count && keys[index] < key)
            index++;
        return index;
    }


    public void remove(int key) {

        int index = findKey(key);
        if (index < count && keys[index] == key) { // Find key
            if (isLeaf) // key in leaf node
                removeFromLeaf(index);
            else // key is not in the leaf node
                removeFromNonLeaf(index);
        } else {
            if (isLeaf) { // If the node is a leaf node, then the node is not in the B tree
                System.out.printf("The key %d does not exist in the tree\n", key);
                return;
            }

            // Otherwise, the key to be deleted exists in the subtree with the node as the root

            // This flag indicates whether the key exists in the subtree whose root is the last child of the node
            // When index is equal to count, the whole node is compared, and flag is true
            boolean flag = index == count;

            if (children[index].count < order) // When the child node of the node is not full, fill it first
                fill(index);


            //If the last child node has been merged, it must have been merged with the previous child node, so we recurse on the (index-1) child node.
            // Otherwise, we recurse to the (index) child node, which now has at least the keys of the minimum order
            if (flag && index > count) children[index - 1].remove(key);
            else children[index].remove(key);
        }
    }

    public void removeFromLeaf(int index) {

        // Shift from index
        for (int i = index + 1; i < count; ++i) keys[i - 1] = keys[i];
        count--;
    }

    public void removeFromNonLeaf(int index) {

        int key = keys[index];

        // If the subtree before key (children[index]) has at least t keys
        // Then find the precursor 'pred' of key in the subtree with children[index] as the root
        // Replace key with 'pred', recursively delete pred in children[index]
        if (children[index].count >= order) {
            int pred = getPred(index);
            keys[index] = pred;
            children[index].remove(pred);
        }
        // If children[index] has fewer keys than order, check children[index+1]
        // If children[index+1] has at least order keys, in the subtree whose root is children[index+1]
        // Find the key's successor 'succ' and recursively delete succ in children[index+1]
        else if (children[index + 1].count >= order) {
            int succ = getSucc(index);
            keys[index] = succ;
            children[index + 1].remove(succ);
        } else {
            // If the count of keys of children[index] and children[index+1] is less than order
            // Then key and children[index+1] are combined into children[index]
            // Now children[index] contains the 2t-1 key
            // Release children[index+1], recursively delete the key in children[index]
            merge(index);
            children[index].remove(key);
        }
    }

    public int getPred(int index) { // Rightmost Left subtree
        Node curr = children[index];
        while (!curr.isLeaf) curr = curr.children[curr.count];
        return curr.keys[curr.count - 1];
    }

    public int getSucc(int index) { // Leftmost Right subtree
        Node curr = children[index + 1];
        while (!curr.isLeaf) curr = curr.children[0];
        return curr.keys[0];
    }

    // Fill children[index] with <m keys
    public void fill(int index) {

        // If the previous child node has multiple order-1 keys, borrow from them
        if (index != 0 && children[index - 1].count >= order) borrowFromPrev(index);
            // The latter sub node has multiple order-1 keys, from which to borrow
        else if (index != count && children[index + 1].count >= order) borrowFromNext(index);
        else {
            // Merge children[index] and its brothers
            // If children[index] is the last child node
            // Then merge it with the previous child node or merge it with its next sibling
            if (index != count) merge(index);
            else merge(index - 1);
        }
    }

    // Borrow a key from children[index-1] and insert it into children[index]
    public void borrowFromPrev(int index) {

        Node child = children[index];
        Node sibling = children[index - 1];

        // The last key from children[index-1] overflows to the parent node
        // The key[index-1] underflow from the parent node is inserted as the first key in children[index]
        // Therefore, sibling decreases by one and children increases by one
        for (int i = child.count - 1; i >= 0; --i) // children[index] move forward
            child.keys[i + 1] = child.keys[i];

        if (!child.isLeaf) { // Move children[index] forward when they are not leaf nodes
            for (int i = child.count; i >= 0; --i) child.children[i + 1] = child.children[i];
        }

        // Set the first key of the child node to the keys of the current node [index-1]
        child.keys[0] = keys[index - 1];
        if (!child.isLeaf) // Take the last child of sibling as the first child of children[index]
            child.children[0] = sibling.children[sibling.count];

        // Move the last key of sibling up to the last key of the current node
        keys[index - 1] = sibling.keys[sibling.count - 1];
        child.count++;
        sibling.count--;
    }

    // Symmetric with borowfromprev
    public void borrowFromNext(int index) {

        Node child = children[index];
        Node sibling = children[index + 1];

        child.keys[child.count] = keys[index];

        if (!child.isLeaf) child.children[child.count + 1] = sibling.children[0];

        keys[index] = sibling.keys[0];

        for (int i = 1; i < sibling.count; ++i) sibling.keys[i - 1] = sibling.keys[i];

        if (!sibling.isLeaf) {
            for (int i = 1; i <= sibling.count; ++i) sibling.children[i - 1] = sibling.children[i];
        }
        child.count += 1;
        sibling.count -= 1;
    }

    // Merge childre[index+1] into childre[index]
    public void merge(int index) {

        Node child = children[index];
        Node sibling = children[index + 1];

        // Insert the last key of the current node into the order-1 position of the child node
        child.keys[order - 1] = keys[index];

        // keys: children[index+1] copy to children[index]
        for (int i = 0; i < sibling.count; ++i) child.keys[i + order] = sibling.keys[i];

        // children: children[index+1] copy to children[index]
        if (!child.isLeaf) {
            for (int i = 0; i <= sibling.count; ++i) child.children[i + order] = sibling.children[i];
        }

        // Move keys forward, not gap caused by moving keys[index] to children[index]
        for (int i = index + 1; i < count; ++i) keys[i - 1] = keys[i];
        // Move the corresponding child node forward
        for (int i = index + 2; i <= count; ++i) children[i - 1] = children[i];

        child.count += sibling.count + 1;
        count--;
    }


    public void insertNotFull(int key) {

        int i = count - 1; // Initialize i as the rightmost index

        if (isLeaf) { // When it is a leaf node
            // Find the location where the new key should be inserted
            while (i >= 0 && keys[i] > key) {
                keys[i + 1] = keys[i]; // keys backward shift
                i--;
            }
            keys[i + 1] = key;
            count++;
        } else {
            // Find the child node location that should be inserted
            while (i >= 0 && keys[i] > key) i--;
            if (children[i + 1].count == 2 * order - 1) { // When the child node is full
                splitChild(i + 1, children[i + 1]);
                // After splitting, the key in the middle of the child node moves up, and the child node splits into two
                if (keys[i + 1] < key) i++;
            }
            children[i + 1].insertNotFull(key);
        }
    }


    public void splitChild(int i, Node y) {

        // First, create a node to hold the keys of order-1 of y
        Node z = new Node(y.order, y.isLeaf);
        z.count = order - 1;

        // Pass the properties of y to z
        for (int j = 0; j < order - 1; j++) z.keys[j] = y.keys[j + order];
        if (!y.isLeaf) {
            for (int j = 0; j < order; j++) z.children[j] = y.children[j + order];
        }
        y.count = order - 1;

        // Insert a new child into the child
        for (int j = count; j >= i + 1; j--) children[j + 1] = children[j];
        children[i + 1] = z;

        // Move a key in y to this node
        for (int j = count - 1; j >= i; j--) keys[j + 1] = keys[j];
        keys[i] = y.keys[order - 1];

        count++;
    }


    public void traverse() {
        int i;
        for (i = 0; i < count; i++) {
            if (!isLeaf) children[i].traverse();
            System.out.printf(" %d", keys[i]);
        }

        if (!isLeaf) children[i].traverse();
    }


    public Node search(int key) {
        int i = 0;
        while (i < count && key > keys[i])
            i++;

        if (keys[i] == key) return this;
        if (isLeaf) return null;
        return children[i].search(key);
    }
}
//------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class BTree {
    Node root;
    int order;

    public BTree(int order) {
        this.root = null;
        this.order = order;
    }

    public void traverse() {
        if (root != null) root.traverse();
    }

    // Function to find key
    public Node search(int key) {
        return root == null ? null : root.search(key);
    }

    public void insert(int key) {
        if (root == null) {
            root = new Node(order, true);
            root.keys[0] = key;
            root.count = 1;
        } else {
            // When the root node is full, the tree will grow high
            if (root.count == 2 * order - 1) {
                Node s = new Node(order, false);
                // The old root node becomes a child of the new root node
                s.children[0] = root;
                // Separate the old root node and give a key to the new node
                s.splitChild(0, root);
                // The new root node has 2 child nodes. Move the old one over there
                int i = 0;
                if (s.keys[0] < key) i++;
                s.children[i].insertNotFull(key);

                root = s;
            } else root.insertNotFull(key);
        }
    }

    public void remove(int key) {
        if (root == null) {
            System.out.println("The tree is empty");
            return;
        }
        root.remove(key);

        if (root.count == 0) { // If the root node has 0 keys
            // If it has a child, its first child is taken as the new root,
            // Otherwise, set the root node to null
            if (root.isLeaf) root = null;
            else root = root.children[0];
        }
    }
}

public static void main(String[] args) {
        BTree t = new BTree(5); // A B-Tree with order 5
        t.insert(50);
        t.insert(80);
        t.insert(10);
        t.insert(20);
        t.insert(4);
        t.insert(5);
        t.insert(6);
        t.insert(15);
        t.insert(14);
        t.insert(16);
        t.insert(23);
        t.insert(27);
        t.insert(60);
        t.insert(70);
        t.insert(75);
        t.insert(51);
        t.insert(52);
        t.insert(64);
        t.insert(65);
        t.insert(68);
        t.insert(72);
        t.insert(73);
        t.insert(77);
        t.insert(78);
        t.insert(79);
        t.insert(90);
        t.insert(95);
        t.insert(81);
        t.insert(82);
        t.insert(89);
        t.insert(92);
        t.insert(93);
        t.insert(100);
        t.insert(110);
        t.insert(111);

        System.out.println("Traversal of tree constructed is");
        t.traverse();
        System.out.println();

        t.remove(64);
        t.remove(23);
        t.remove(72);
        t.remove(65);
        t.remove(20);
        t.remove(70);
        t.remove(95);
        t.remove(77);
        t.remove(80);
        t.remove(100);
        t.remove(6);
        t.remove(27);
        t.remove(60);
        t.remove(16);
        t.remove(50);
        t.traverse();
        System.out.println();

    }
}

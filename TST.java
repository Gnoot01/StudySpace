import java.util.ArrayList;

class Node {
    char data;
    boolean isWord;
    Node L, M, R;

    public Node(char data) {
        this.data = data;
        this.isWord = false;
        this.L = null;
        this.M = null;
        this.R = null;
    }
}

class TST {
    private Node root;
    private ArrayList<String> list;

    public TST() {
        root = null;
    }

    public void makeEmpty() {
        root = null;
    }

    public boolean search(String word) {
        if (word == null || word.isEmpty()) return false;
        return search(root, word.toCharArray(), 0);
    }

    private boolean search(Node node, char[] word, int i) {
        if (node == null) return false;
        // If word[i]<curr node.data, traverse to L child
        if (word[i] < node.data) return search(node.L, word, i);
            // else if word[i]>curr node.data, traverse to R child
        else if (word[i] > node.data) return search(node.R, word, i);
            // Equal
        else {
            // if wordNode & word[i] is last letter of word
            if (node.isWord && i == word.length - 1) return true;
                // else traverse to M child & search next letter of word
            else return search(node.M, word, i + 1);
        }
    }

    public void insert(String word) {
        if (word != null && !word.isEmpty()) root = insert(root, word.toCharArray(), 0);
    }

    private Node insert(Node node, char[] word, int i) {
        if (node == null) node = new Node(word[i]);

        if (word[i] < node.data) node.L = insert(node.L, word, i);
        else if (word[i] > node.data) node.R = insert(node.R, word, i);
            // Equal
        else if (i + 1 < word.length) node.M = insert(node.M, word, i + 1);
        else node.isWord = true;
        return node;
    }

    public void delete(String word) {
        if (word != null && !word.isEmpty()) delete(root, word.toCharArray(), 0);
    }

    private void delete(Node node, char[] word, int i) {
        // 1) Key doesn't exist -> Do nothing
        if (node == null) return;
        // 2) Key exists as unique (NOT 3/4)->Delete all the nodes. [Delete BUG]
        // 3) Key exists as prefix of a longer key->Unmark the word node [Delete CAT from CATS, T|T->T|F]
        // 4) Key exists as part of it being prefix of a shorter key->Delete all extra nodes [Delete CATALOGUE from CATS, ALOGUE char nodes]
        if (word[i] < node.data) delete(node.L, word, i);
        else if (word[i] > node.data) delete(node.R, word, i);
        else {
            if (node.isWord && i == word.length - 1) {
                node.isWord = false;
            } else if (i + 1 < word.length) {
                delete(node.M, word, i + 1);
            }
        }
    }

    // Eg trie function (prefix)
    public boolean startsWith(String prefix) {
        if (prefix == null || prefix.isEmpty()) return false;
        return startsWith(root, prefix.toCharArray(), 0);
    }

    private boolean startsWith(Node node, char[] prefix, int i) {
        if (node == null) return false;
        if (prefix[i] < node.data) return startsWith(node.L, prefix, i);
        else if (prefix[i] > node.data) return startsWith(node.R, prefix, i);
        else if (i + 1 == prefix.length) return true;
        return startsWith(node.M, prefix, i + 1);
    }

    // Traverse Tree
    private void traverse(Node node, String str) {
        if (node != null) {
            traverse(node.L, str);
            str += node.data;
            if (node.isWord) list.add(str);
            traverse(node.M, str);
            str = str.substring(0, str.length() - 1);
            traverse(node.R, str);
        }
    }

    // Print Tree
    @Override
    public String toString() {
        list = new ArrayList<String>();
        traverse(root, "");
        return "\nTernary Search Tree : " + list;
    }
}

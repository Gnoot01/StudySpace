// Tutorial: https://www.youtube.com/watch?v=jND_WJ8r7FE&list=PLDV1Zeh2NRsB6SWUrDFW2RmDotAfPbeHu&index=52

public class MinIndexedBinaryHeap<T extends Comparable<T>> extends MinIndexedDHeap<T> {
  public MinIndexedBinaryHeap(int maxSize) {
    super(2, maxSize);
  }
}

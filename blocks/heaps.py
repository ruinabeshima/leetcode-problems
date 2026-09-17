import heapq
from collections import Counter


r"""
HEAPS

A container that always hands you the SMALLEST item first, in O(log n).

NOT a sorted list. You cannot index into it, and iterating it gives you
garbage order. The only things it does cheaply are "give me the minimum"
and "take another item". That restriction is what makes it fast.

You have already used one: the heap in dijkstra() in graphs.py. That is
why you could always pop the closest unvisited node without re-sorting.

  heapify(list)   O(n)       rearrange a list into a heap, IN PLACE
  heappush(h, x)  O(log n)
  heappop(h)      O(log n)   removes AND returns the smallest
  h[0]            O(1)       peek at the smallest without removing

Key point: heapq is MIN-heap only. For a max-heap, negate on the way in
and negate again on the way out. That trick is the most common heap
gotcha and it shows up in half the problems.
"""
def heap_basics():
    nums = [5, 1, 8, 3]

    heapq.heapify(nums)                 # in place -- returns None, don't assign it
    heapq.heappush(nums, 2)
    smallest = heapq.heappop(nums)      # 1
    peek = nums[0]                      # smallest remaining, NOT removed

    # MAX-heap: negate going in, negate coming out
    max_heap = []
    for n in [5, 1, 8, 3]:
        heapq.heappush(max_heap, -n)
    largest = -heapq.heappop(max_heap)  # 8

    # Tuples compare element by element, so the FIRST item is the sort key.
    # This is exactly dijkstra's (distance, node).
    tasks = []
    heapq.heappush(tasks, (2, "later"))
    heapq.heappush(tasks, (1, "sooner"))
    priority, name = heapq.heappop(tasks)     # (1, "sooner")

    return smallest, peek, largest, name


r"""
THE ONE BLOCK: TOP-K with a size-k heap

Key point: to find the k LARGEST, use a MIN-heap of size k.

That feels backwards, and it is the whole insight. The heap holds your
current champions, and its root is the WEAKEST of them -- exactly the one
to throw away when a better candidate shows up.

O(n log k) instead of O(n log n) for sorting. It also works on a stream,
where sorting cannot: you never need to hold all n items at once.
"""
def k_largest(nums, k):
    heap = []

    for n in nums:
        heapq.heappush(heap, n)
        if len(heap) > k:
            heapq.heappop(heap)     # evict the smallest -> the k biggest survive

    return heap                     # k largest, in NO particular order


def kth_largest(nums, k):
    # The kth largest IS the smallest of the k largest -- i.e. the root.
    heap = []

    for n in nums:
        heapq.heappush(heap, n)
        if len(heap) > k:
            heapq.heappop(heap)

    return heap[0]


def k_smallest(nums, k):
    # Mirror image: to keep the k SMALLEST you must evict the largest,
    # which needs a max-heap -> negate.
    heap = []

    for n in nums:
        heapq.heappush(heap, -n)
        if len(heap) > k:
            heapq.heappop(heap)     # pops the most negative = the largest

    return [-x for x in heap]


def top_k_frequent(nums, k):
    counts = Counter(nums)          # value -> how many times it appears

    heap = []
    for value, freq in counts.items():
        heapq.heappush(heap, (freq, value))     # freq FIRST: it is the sort key
        if len(heap) > k:
            heapq.heappop(heap)                 # evict the least frequent

    return [value for freq, value in heap]


r"""
TWO HEAPS -- Find Median from Data Stream

The only genuinely clever heap problem you are likely to meet.

Split the numbers in half, one heap per half, arranged so the two
candidates for the median sit at the two roots:

    low  = MAX-heap of the smaller half   (negated)
    high = MIN-heap of the larger half

        ... 1 2 3 | 4 5 6 ...
                ^   ^
            low[0]  high[0]      both O(1) to read

Key point: always push into `low` first, move its largest across to
`high`, then rebalance if `high` grew bigger. Pushing straight into
whichever heap looks shorter lets a too-large number sit in `low`, and
the roots stop being the median.
"""
class MedianFinder:
    def __init__(self):
        self.low = []       # max-heap (negated): the smaller half
        self.high = []      # min-heap: the larger half

    def add(self, num):
        # 1. everything enters through low
        heapq.heappush(self.low, -num)

        # 2. hand low's largest to high, so low[0] <= high[0] always holds
        heapq.heappush(self.high, -heapq.heappop(self.low))

        # 3. keep low the same size as high, or exactly one bigger
        if len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def median(self):
        if len(self.low) > len(self.high):
            return -self.low[0]                     # odd count: low holds the extra
        return (-self.low[0] + self.high[0]) / 2     # even: average the two roots

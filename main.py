import heapq

""" 
Practising heaps 
1. Find minimum number 
2. Find maximum 
3. Find minimum of tuple

"""

def heap(): 
    nums = [5, 1, 8, 3]
    heapq.heapify(nums)
    heapq.heappush(nums, 2)
    smallest = heapq.heappop(nums)
    print(smallest)

    max_heap = []
    for num in nums: 
        heapq.heappush(max_heap, -num)
    largest = -heapq.heappop(max_heap)
    print(largest)

def k_largest(nums, k): 
    heap = []
    for n in nums:
        heapq.heappush(heap, n)
        if len(heap) > k: 
            heapq.heappop(heap)

    return heap 

def k_largest_2(nums, k):
    heapq.heapify(nums)

    while len(nums) > k: 
        heapq.heappop(nums)
        
    return nums
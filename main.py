import heapq

def heap(): 
    nums = [5, 1, 8, 3]

    heapq.heapify(nums)
    heapq.heappush(nums, 2)
    smallest = heapq.heappop(nums)
    peek = nums[0]

    max_heap = []
    for n in nums: 
        heapq.heappush(max_heap, -n)
    largest = -heapq.heappop(max_heap)

    tasks = []
    heapq.heappush(tasks, (2, "later"))
    heapq.heappush(tasks, (1, "sooner"))


    print(smallest, peek, largest)

heap()

def kthlargest(nums, k):
    heap = []

    for n in nums: 
        heapq.heappush(nums, n)
        if len(heap) > k: 
            heapq.heappop(heap)

        return heap 


def ksmallest(nums, k):
    heap = []

    for n in nums: 
        heapq.heappush(heap, -n)
        if len(nums) > k: 
            heapq.heappush(heap)

    return [-x for x in heap]



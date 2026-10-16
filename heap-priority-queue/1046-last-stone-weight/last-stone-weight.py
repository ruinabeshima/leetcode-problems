class Solution:
    def lastStoneWeight(self, stones: list[int]) -> int:
        heap = [-stone for stone in stones]
        heapq.heapify(heap)

        while len(heap) > 1: 
            y = -heapq.heappop(heap)
            x = -heapq.heappop(heap)

            if x < y: 
                heapq.heappush(heap, -(y - x))
        
        return -heap[0] if len(heap) == 1 else 0 


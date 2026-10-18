class Solution:
    def kClosest(self, points: list[list[int]], k: int) -> list[list[int]]:
        heap = []

        for x, y in points: 
            heapq.heappush(heap, (-(x*x + y*y), x, y))

            if len(heap) > k: 
                heapq.heappop(heap)

        res = []
        for _, x, y in heap:
            res.append([x, y])
        return res
            
        


class Solution:
    def leastInterval(self, tasks: list[str], n: int) -> int:
        heap = [-c for c in Counter(tasks).values()]
        heapq.heapify(heap) # O(n) 
        time = 0 
        q = deque()

        while q or heap:
            time += 1 

            if heap: 
                val = heapq.heappop(heap) + 1
                if val < 0: 
                    q.append((val, time + n))

            if q and q[0][1] == time: 
                heapq.heappush(heap, q.popleft()[0])

        return time

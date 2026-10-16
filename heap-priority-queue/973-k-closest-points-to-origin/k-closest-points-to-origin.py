class Solution:
    def kClosest(self, points: list[list[int]], k: int) -> list[list[int]]:
        mapping = defaultdict(list)

        # Create distance array
        distances = [] 
        for x, y in points: # O(n)
            distance = math.sqrt(x ** 2 + y ** 2)
            mapping[distance].append([x, y])
            distances.append(distance)

        # Heap 
        res = []
        heapq.heapify(distances) # O(log n)
        for i in range(k): 
            dist = heapq.heappop(distances)
            res.append(mapping[dist][0])
            mapping[dist].pop(0)

        return res


class Solution:
    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        # curr, prereq

        indegree = [0] * numCourses 
        graph = defaultdict(list)

        for curr, prereq in prerequisites: 
            indegree[curr] += 1 
            graph[prereq].append(curr)

        queue = deque([i for i in range(numCourses) if indegree[i] == 0])
        order = []
       
        while queue: 
            node = queue.popleft() 
            order.append(node)

            for neighbor in graph[node]: 
                indegree[neighbor] -= 1 
                if indegree[neighbor] == 0: 
                    queue.append(neighbor)

        return len(order) == numCourses
            

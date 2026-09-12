class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        graph = defaultdict(list)
        indegree = [0] * numCourses

        for course, prereq in prerequisites: 
            graph[prereq].append(course)
            indegree[course] += 1 

        order = []
        queue = deque(i for i in range(len(indegree)) if indegree[i] == 0)

        while queue: 
            node = queue.popleft()
            order.append(node)

            for neighbor in graph[node]: 
                indegree[neighbor] -= 1 
                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        return len(order) == numCourses


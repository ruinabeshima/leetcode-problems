from collections import deque

def level_order(root): 
    if not root: 
        return []

    queue = deque([root])
    out = []

    while queue: 
        level = []

        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)

            if node.left: 
                queue.append(node.left)
            if node.right: 
                queue.append(node.right)

        out.append(level)

    return out
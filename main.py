def diameter(root): 
    best = 0 

    def depth(node): 
        nonlocal best 

        if not node: 
            return 0 

        left = depth(node.left)
        right = depth(node.right)

        best = max(left + right, best)
        return 1 + max(left, right)

    depth(root)
    return best 

def max_path_sum(root): 
    best = float("-inf")

    def gain(node): 
        nonlocal best 

        if not node: 
            return 0 

        left_sum = max(gain(node.left), 0)
        right_sum = max(gain(node.right), 0)

        best = max(best, node.val + left_sum + right_sum)
        return node.val + max(left_sum, right_sum)

def has_path_sum(node, target): 
    if not node: 
        return False 

    if not node.left and not node.right: 
        return target == node.val

    rest = target - node.val 
    return has_path_sum(node.left, rest) or has_path_sum(node.right, rest)


def all_root_to_leaf_paths(root): 
    out, path = [], []

    def dfs(node): 
        if not node: 
            return 

        path.append(node.val)

        if not node.left and not node.right: 
            out.append(path[:])
            path.pop() 
            return 

        dfs(node.left)
        dfs(node.right)
        path.pop() 
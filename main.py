
# Binary tree initialisation
class TreeNode: 
    def __init__(self, val, left=None, right=None): 
        self.val = val
        self.left = left
        self.right = right 


#       1
#     2     3
#   4   5     10

A = TreeNode(1)
B = TreeNode(2)
C = TreeNode(3)
D = TreeNode(4) 
E = TreeNode(5) 
F = TreeNode(10)

A.left = B 
A.right = C 
B.left = D 
B.right = E 
C.right = F 

# Recursive pre-order traversal, DFS, root -> left -> right, O(n) space and time 
def pre_order(node): 
    if not node: 
        return 

    print(node.val)
    pre_order(node.left)
    pre_order(node.right)
print("Recursive pre-order traversal")
pre_order(A)

# Recursive in-order traveral, DFS, left -> root -> right, O(n) space and time 
def in_order(node): 
    if not node: 
        return 
    
    in_order(node.left)
    print(node.val)
    in_order(node.right)
print("Recursive in order traversal")
in_order(A) 


# Recursive post-order traversal, DFS, left -> right -> root, O(n) space and time 
def post_order(node): 
    if not node: 
        return 
    
    post_order(node.left)
    post_order(node.right)
    print(node.val)
print("Recursive post order traversal")
post_order(A)

# Iterative pre-order traversal, LIFO, O(n) space and time
def pre_order_iterative(node): 
    stack = [node]
    while stack:
        node = stack.pop() 
        print(node.val)
        if node.right: stack.append(node.right)
        if node.left: stack.append(node.left)
print("Iterative pre-order traversal")
pre_order_iterative(A) 


# Level order traversal, BFS, O(n) time and space 
from collections import deque
def level_order(node): 
    queue = deque()
    queue.append(node)

    while queue: 
        node = queue.popleft() 
        print(node.val)
        if node.left: queue.append(node.left)
        if node.right: queue.append(node.right)
print("Level order traversal")
level_order(A) 


# Check value exists with DFS, O(n) space and time
def search(node, target): 
    if not node: 
        return False 
     
    if node.val == target: 
        return True 
    return search(node.left, target) or search(node.right, target)


# Binary Search Trees (BSTs)

#         5
#     1       8
#  -1  3   7    9

class BTreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"BTreeNode({self.val})"

A2 = BTreeNode(5)
B2 = BTreeNode(1)
C2 = BTreeNode(8)
D2 = BTreeNode(-1)
E2 = BTreeNode(3)
F2 = BTreeNode(7)
G2 = BTreeNode(9)

A2.left, A2.right = B2, C2
B2.left, B2.right = D2, E2
C2.left, C2.right = F2, G2


in_order(A2)


# Searching, O(log n) time, O(log n) space 
def search_bst(node, target):
    if not node: 
        return False 
    
    if node.val == target: 
        return True 
    elif target > node.val: 
        return search_bst(node.right, target)
    elif target < node.val: 
        return search_bst(node.left, target)

    

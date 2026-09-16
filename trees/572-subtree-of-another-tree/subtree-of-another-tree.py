# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSubtree(self, root: TreeNode | None, subRoot: TreeNode | None) -> bool:
        def check(p, q): 
            if not p and not q: 
                return True 
            if not p or not q: 
                return False 

            return p.val == q.val and check(p.left, q.left) and check(p.right, q.right)


        def walk(node): 
            if not node: 
                return False

            checked = check(node, subRoot) 

            if checked: 
                return True  
            
            return walk(node.left) or walk(node.right)

        return walk(root)

            

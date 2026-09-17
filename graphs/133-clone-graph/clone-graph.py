"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""

from typing import Optional
class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        mapping = {}
        
        def clone(node): 
            if node in mapping: 
                return mapping[node]

            mapping[node] = Node(node.val)
            for neighbor in node.neighbors: 
                mapping[node].neighbors.append(clone(neighbor))
            return mapping[node]

        return clone(node) if node else None

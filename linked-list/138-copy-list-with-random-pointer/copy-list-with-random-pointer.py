"""
# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random
"""

class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        hashmap = {None: None} 
        new_curr = dummy = Node(0)

        curr = head
        while curr: 
            hashmap[curr] = Node(curr.val)
            curr = curr.next 
        
        curr = head 
        while curr: 
            new_node = hashmap[curr]
            new_node.next = hashmap[curr.next]
            new_node.random = hashmap[curr.random]
            new_curr.next = new_node
            new_curr = new_curr.next
            curr = curr.next 
        return dummy.next

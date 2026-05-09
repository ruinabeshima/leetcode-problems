# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:
        dummy = ListNode()  
        tail = dummy 
        pointer = head 

        while pointer: 
            if pointer.val != val: 
                tail.next = pointer 
                tail = tail.next 
            pointer = pointer.next

        tail.next = None

        return dummy.next  

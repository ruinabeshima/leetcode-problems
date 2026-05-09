# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head: 
            return head 

        tail = head 
        pointer = head.next

        while pointer: 
            if tail.val != pointer.val: 
                tail.next = pointer 
                tail = tail.next 
            pointer = pointer.next 

        tail.next = None 
        return head
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        """
        Do not return anything, modify head in-place instead.
        """

        # Find the middle of the list 
        slow, fast = head, head.next
        while fast and fast.next: 
            fast = fast.next.next 
            slow = slow.next

        # Reverse right side
        second = slow.next
        slow.next = None # Split into two different lists
        
        prev = None
        while second: 
            temp = second.next 
            second.next = prev
            prev = second
            second = temp 

        # Merge two halves
        second = prev
        first = head
        while first and second:
            tmp1, tmp2 = first.next, second.next 
            first.next = second 
            second.next = tmp1
            first = tmp1 
            second = tmp2 
        




        
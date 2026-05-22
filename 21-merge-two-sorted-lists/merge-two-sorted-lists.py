# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0) 
        curr = dummy 

        pointer_1 = list1 
        pointer_2 = list2 

        while pointer_1 and pointer_2: 
            if pointer_1.val > pointer_2.val: 
                curr.next = pointer_2 
                pointer_2 = pointer_2.next 
            else: 
                curr.next = pointer_1 
                pointer_1 = pointer_1.next 
            curr = curr.next 

        if pointer_1: 
            curr.next = pointer_1 
        elif pointer_2: 
            curr.next = pointer_2 

        return dummy.next 

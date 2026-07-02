# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        curr = dummy = ListNode(0)
        carry = 0 

        while l1 or l2: 
            if l1 and l2: 
                l1val, l2val = l1.val, l2.val
                l1 = l1.next
                l2 = l2.next
            elif not l1: 
                l1val = 0 
                l2val = l2.val 
                l2 = l2.next
            else: 
                l1val = l1.val 
                l2val = 0 
                l1 = l1.next
            
            sum = l1val + l2val + carry
            if sum < 10: 
                curr.next = ListNode(sum)
                carry = 0 
            else: 
                curr.next = ListNode(int(str(sum)[1]))
                carry = int(str(sum)[0])
            curr = curr.next

        if carry > 0: 
            curr.next = ListNode(carry)

        return dummy.next
            
            

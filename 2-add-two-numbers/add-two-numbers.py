# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        def reverse(prev, curr): 
            if curr is None: 
                return prev 
            temp = curr.next 
            curr.next = prev 
            return reverse(curr, temp)
        
        reverse_1 = reverse(None, l1)
        reverse_2 = reverse(None, l2)
        num1, num2 = "", "" 

        while reverse_1: 
            num1 += str(reverse_1.val)
            reverse_1 = reverse_1.next
        while reverse_2: 
            num2 += str(reverse_2.val)
            reverse_2 = reverse_2.next
        result = int(num1) + int(num2)

        dummy = ListNode(0)
        curr = dummy
        for i in range(len(str(result)) - 1, -1, -1): 
            curr.next = ListNode(int(str(result)[i]))
            curr = curr.next
        return dummy.next

        
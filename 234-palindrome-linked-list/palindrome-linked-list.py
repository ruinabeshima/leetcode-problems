# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:

        # Find the middle of the linked list
        left = head 
        right = head 
        while right and right.next: 
            right = right.next.next
            left = left.next

        # Reverse the right half of the linked list in-place
        curr = left
        prev = None 
        while curr: 
            temp = curr.next 
            curr.next = prev 
            prev = curr 
            curr = temp 

        # Compare 
        pointer_1 = head 
        pointer_2 = prev 

        while pointer_1 != prev and pointer_2: 
            if pointer_1.val != pointer_2.val: 
                return False 
            pointer_1 = pointer_1.next 
            pointer_2 = pointer_2.next 
        return True 





    
                

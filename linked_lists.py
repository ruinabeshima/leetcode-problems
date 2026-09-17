class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


r"""
LINKED LISTS

There is no algorithm here in the way there is for graphs. Linked list
problems are POINTER CHOREOGRAPHY: the difficulty is never "which
algorithm", it is "did I lose the rest of the list".

Two habits prevent most bugs:
  1. Before overwriting a .next, save what it pointed at.
  2. Draw three nodes on paper and move the arrows by hand.

Five blocks:
  1. Dummy head        (any problem that might change the head)
  2. Reverse           (three pointers)
  3. Fast & slow       (middle, cycle, nth-from-end)
  4. Merge two sorted  (dummy + two pointers)
  5. Split-reverse-merge (the combo)
"""


r"""
1. DUMMY HEAD

The problem: deleting or inserting at the HEAD is a special case, because
there is no previous node to update. That special case is where the bugs
live.

The fix: invent a node in front of the real head. Now every node has a
predecessor, the special case disappears, and you return dummy.next at
the end (NOT head -- head might be the thing you deleted).

Key point: if the head can change, use a dummy.
"""
def remove_elements(head, val):
    dummy = ListNode(0, head)
    curr = dummy

    # Look at curr.next, so we always hold the PREVIOUS node
    while curr.next:
        if curr.next.val == val:
            curr.next = curr.next.next      # unlink
        else:
            curr = curr.next                # only advance when we didn't delete

    return dummy.next


# Note: the advance is inside the else. After deleting, curr.next is a
# NEW node that also needs checking -- advancing would skip it. That is
# the classic bug on input like [1, 1, 1] with val = 1.


r"""
2. REVERSE A LINKED LIST

The one everybody has to be able to write cold.

You walk the list flipping each .next to point backwards. Three pointers:

    prev  = the part already reversed (starts as None: nothing behind head)
    curr  = the node being flipped
    nxt   = a saved handle on the rest, BEFORE we destroy curr.next

    None <- 1 <- 2   3 -> 4 -> 5
            prev^  curr^

Key point: the moment you write curr.next = prev you have destroyed your
only reference to the rest of the list. Save it first. That single line
is the whole reason `nxt` exists.

At the end curr is None and prev is the last node visited = the new head.
"""
def reverse_list(head):
    prev = None
    curr = head

    while curr:
        nxt = curr.next     # SAVE before destroying
        curr.next = prev    # flip the arrow
        prev = curr         # advance prev
        curr = nxt          # advance curr

    return prev             # prev, not curr -- curr is None


def reverse_between(head, left, right):
    # Reverse only positions left..right (1-indexed).
    # Head can change when left == 1 -> dummy.
    dummy = ListNode(0, head)
    before = dummy

    for _ in range(left - 1):
        before = before.next

    # Standard reverse, but stopped after (right - left + 1) nodes
    prev = None
    curr = before.next
    tail = curr                 # this becomes the TAIL of the reversed chunk

    for _ in range(right - left + 1):
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt

    # Stitch the reversed chunk back in
    before.next = prev          # prev = new head of the chunk
    tail.next = curr            # curr = first node after the chunk

    return dummy.next


r"""
3. FAST AND SLOW POINTERS

Two pointers moving at different speeds. Their GAP is what does the work.

  - fast moves 2, slow moves 1   -> slow lands on the middle
  - in a cycle, fast gains 1 step per tick on slow, so it must catch up
  - fast starts n ahead          -> when fast hits the end, slow is n from it

Key point: `while fast and fast.next` is the guard. You need both,
because fast.next.next must be legal. Getting this wrong is an
AttributeError on even-length lists.
"""
def middle_node(head):
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow     # even length -> returns the SECOND middle


def has_cycle(head):
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        # Compare identity, not value -- two nodes can share a value
        if slow is fast:
            return True

    return False    # fast reached the end, so there was no cycle


r"""
FINDING WHERE THE CYCLE STARTS (Floyd, phase 2)

Once slow and fast meet, reset ONE pointer to the head and move both
one step at a time. They meet at the cycle entrance.

Why: let L = distance head -> entrance, and C = cycle length. When they
meet, slow has gone L + k and fast has gone twice that, and the extra
distance fast covered is a whole number of laps. The algebra falls out
to: the meeting point is exactly L steps from the entrance, going
forward. So head and meeting-point are equidistant from it.

You do not need to re-derive this in an interview. Just remember:
MEET, RESET ONE TO HEAD, WALK BOTH AT SPEED 1.
"""
def cycle_start(head):
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow is fast:
            slow = head                 # reset one pointer

            while slow is not fast:     # now both move at speed 1
                slow = slow.next
                fast = fast.next

            return slow                 # the entrance

    return None


def remove_nth_from_end(head, n):
    # Head can change (removing the 1st node) -> dummy
    dummy = ListNode(0, head)
    slow = fast = dummy

    # Open a gap of exactly n
    for _ in range(n):
        fast = fast.next

    # Walk both until fast is at the last node.
    # slow is then the node BEFORE the one to remove.
    while fast.next:
        slow = slow.next
        fast = fast.next

    slow.next = slow.next.next
    return dummy.next


r"""
4. MERGE TWO SORTED LISTS

Dummy head plus a `tail` pointer you keep appending to.

Key point: `tail.next = a or b` at the end. One list is exhausted, the
other still has nodes, and they are already sorted -- so attach the whole
remainder in one line instead of looping.

(`a or b` is Python's "first truthy one", i.e. whichever is not None.)
"""
def merge_two_lists(a, b):
    dummy = ListNode()
    tail = dummy

    while a and b:
        if a.val <= b.val:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next

        tail = tail.next

    tail.next = a or b      # attach whatever is left
    return dummy.next


r"""
5. SPLIT -> REVERSE -> MERGE (the combo)

Hard-looking list problems are usually two or three of the blocks above,
chained. Once you spot that, they stop being hard.

Palindrome:  find the middle, reverse the second half, compare.
Reorder:     find the middle, reverse the second half, weave them.
"""
def is_palindrome(head):
    # 1. middle
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # 2. reverse the second half
    second = reverse_list(slow)

    # 3. compare. The first half is still longer or equal, so stopping
    #    when `second` runs out is correct.
    first = head
    while second:
        if first.val != second.val:
            return False
        first = first.next
        second = second.next

    return True


def reorder_list(head):
    # 1 -> 2 -> 3 -> 4 -> 5   becomes   1 -> 5 -> 2 -> 4 -> 3
    if not head or not head.next:
        return head

    # 1. find the middle (first middle, so the halves split cleanly)
    slow, fast = head, head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    # 2. reverse the second half and cut the link between the halves
    second = reverse_list(slow.next)
    slow.next = None

    # 3. weave
    first = head
    while second:
        first_nxt, second_nxt = first.next, second.next
        first.next = second
        second.next = first_nxt
        first, second = first_nxt, second_nxt

    return head


r"""
HELPERS for testing in the REPL
"""
def build(values):
    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out

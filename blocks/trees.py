from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


r"""
TREES VS GRAPHS

A tree is a graph with the hard parts removed:
  - No cycles             -> no visited set, EVER
  - Connected, n-1 edges  -> no outer loop over components
  - One parent each       -> no "did I come from there?" check
  - None is the base case -> the recursion terminates by itself

So nearly every tree problem is plain recursion.
The visited-set reflex from graphs is actively wrong here.

Three core blocks:
  1. Bottom-up DFS   (answer comes from my children)
  2. Top-down DFS    (answer depends on my ancestors)
  3. Level-order BFS (same code as bfs_with_levels in graphs.py)

Two specialisations:
  4. BST   (exploit the ordering)
  5. LCA   (common enough to memorise)
"""


r"""
1. BOTTOM-UP DFS -- the workhorse, roughly 60% of tree problems

Solve both children first, then combine into this node's answer.

Key point: ASSUME THE RECURSIVE CALLS ALREADY WORK.
Don't trace into them. Only ask:
"given the left answer and the right answer, what is the answer here?"

Every problem of this shape is two decisions:
    base case -> what is the answer for an empty tree?
    combine   -> how do left + right + node.val make my answer?
"""
r"""
MAX DEPTH -- how many nodes lie on the longest root-to-leaf chain.
An empty tree is 0, a single node is 1.
"""
def max_depth(node):
    # Base case: an empty tree has depth 0
    if not node:
        return 0

    left = max_depth(node.left)
    right = max_depth(node.right)

    # Combine: 1 (me) + the deeper of my two children
    return 1 + max(left, right)


r"""
COUNT NODES -- how many nodes the tree holds.
Identical shape to max_depth; only the combine line differs.
"""
def count_nodes(node):
    if not node:
        return 0
    # Same shape, different combine
    return 1 + count_nodes(node.left) + count_nodes(node.right)


r"""
IS SAME TREE -- do two trees have the same structure AND the same values?
Walks both in lockstep. Matching values in a different shape is False,
which is what the "exactly one is None" check catches.
"""
def is_same_tree(p, q):
    # Both empty -> same
    if not p and not q:
        return True
    # Exactly one empty -> different
    if not p or not q:
        return False

    return (p.val == q.val
            and is_same_tree(p.left, q.left)
            and is_same_tree(p.right, q.right))


r"""
INVERT TREE -- mirror the tree, swapping every node's two children.
Mutates in place and returns the same root.

Key point: the tuple assignment evaluates BOTH recursive calls before it
assigns either one. Split into two separate lines it reads node.left
after having just overwritten it, and a whole subtree is lost.
"""
def invert_tree(node):
    if not node:
        return None

    node.left, node.right = invert_tree(node.right), invert_tree(node.left)
    return node


r"""
THE SUB-PATTERN THAT TRIPS EVERYONE

Sometimes the value you RETURN is not the answer you WANT.

Your parent needs a depth. But the longest path might BEND at this node
and never reach the parent at all, so that candidate has to be recorded
somewhere on the side.

    best   = the answer      (path that bends here: left + right)
    return = what my parent needs (depth: 1 + max(left, right))

Once you see this split, Diameter / Max Path Sum / Longest Univalue Path
are all the same problem.
"""


r"""
DIAMETER -- the longest path between any two nodes, counted in EDGES.

The path does not have to pass through the root, and neither endpoint
has to be a leaf. A node whose left subtree is 3 deep and right subtree
1 deep has a path of 3 + 1 = 4 edges bending through it.
"""
def diameter(root):
    best = 0

    def depth(node):
        nonlocal best
        if not node:
            return 0

        left = depth(node.left)
        right = depth(node.right)

        # The ANSWER: longest path passing THROUGH this node
        best = max(best, left + right)

        # The RETURN: a depth, because that is what my parent needs
        return 1 + max(left, right)

    depth(root)
    return best


r"""
MAX PATH SUM -- the largest total of node values along any path.

Same shape as diameter, but summing values instead of counting edges.
A path is any chain of connected nodes: it need not touch the root, need
not reach a leaf, and may be a single node on its own. Values can be
negative, which is what the clamp below exists for.
"""
def max_path_sum(root):
    best = float('-inf')

    def gain(node):
        nonlocal best
        if not node:
            return 0

        # A negative branch is worse than not using it at all -> clamp to 0
        left = max(gain(node.left), 0)
        right = max(gain(node.right), 0)

        # ANSWER: the path that bends here uses BOTH branches
        best = max(best, node.val + left + right)

        # RETURN: my parent can only continue down ONE branch
        return node.val + max(left, right)

    gain(root)
    return best


r"""
2. TOP-DOWN DFS -- carry state DOWN as a parameter

Use this when a node's answer depends on what is ABOVE it rather than
below it. The information flows down through the arguments.
"""
r"""
HAS PATH SUM -- is there a root-to-LEAF path whose values add up to target?
Must reach a leaf; stopping partway does not count, which is why the base
case tests for a leaf rather than for None.
"""
def has_path_sum(node, target):
    if not node:
        return False

    # A leaf is where a root-to-leaf path ends
    if not node.left and not node.right:
        return node.val == target

    rest = target - node.val
    return has_path_sum(node.left, rest) or has_path_sum(node.right, rest)


r"""
TOP-DOWN WITH BACKTRACKING

When you need the actual paths, not just a yes/no.

Two bugs live here:
  - appending `path` instead of `path[:]`  (every entry ends up the same list)
  - forgetting a pop() on some return branch
"""
r"""
ALL ROOT-TO-LEAF PATHS -- every complete path from root to leaf, as a
list of value lists.
"""
def all_root_to_leaf_paths(root):
    out, path = [], []

    def dfs(node):
        if not node:
            return

        path.append(node.val)

        if not node.left and not node.right:
            out.append(path[:])     # COPY, or all entries alias one list
            path.pop()              # undo before returning
            return

        dfs(node.left)
        dfs(node.right)
        path.pop()                  # undo

    dfs(root)
    return out


r"""
3. LEVEL-ORDER BFS -- identical to bfs_with_levels in graphs.py

node.left / node.right are the neighbours.
No visited set: a tree cannot revisit. The `if node.left:` guards
replace it.

Reach for BFS over DFS when the question mentions levels, rows, or
"shallowest". Min Depth is the giveaway: DFS explores a whole deep
branch first, BFS stops at the first leaf it meets.
"""
r"""
LEVEL ORDER -- the values grouped by depth, one inner list per level.
"""
def level_order(root):
    if not root:
        return []

    queue = deque([root])
    out = []

    while queue:
        level = []

        # Same snapshot trick: drain exactly one level
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        out.append(level)

    return out


# Twists on level_order:
#   Right Side View -> append level[-1]
#   Level Averages  -> append sum(level) / len(level)
#   Zigzag          -> reverse level on odd rows
#   Max Width       -> track indices instead of nodes
r"""
RIGHT SIDE VIEW -- what you would see standing to the right of the tree:
the LAST node of every level.
"""
def right_side_view(root):
    return [level[-1] for level in level_order(root)]


r"""
MIN DEPTH -- nodes on the SHORTEST root-to-leaf chain.

BFS rather than DFS on purpose: it stops at the first leaf it meets,
where DFS would explore an entire deep branch before finding a shallow one.
"""
def min_depth(root):
    if not root:
        return 0

    queue = deque([root])
    depth = 1

    while queue:
        for _ in range(len(queue)):
            node = queue.popleft()

            # First leaf we meet is the shallowest one
            if not node.left and not node.right:
                return depth

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        depth += 1

    return depth


r"""
4. BST -- exploit the ordering

Two facts carry every BST problem:

  (a) Inorder traversal yields SORTED order.
  (b) A comparison tells you which way to go, so you skip half the tree.

If a problem says "BST" and your solution visits every node,
you are probably missing the point.
"""
r"""
INORDER -- left, then node, then right. On a BST that is SORTED order.
Appends into `out` and returns it.
"""
def inorder(node, out):
    if not node:
        return

    inorder(node.left, out)
    out.append(node.val)        # the work happens BETWEEN the two calls
    inorder(node.right, out)

    return out


r"""
SEARCH BST -- the node holding target, or None.
O(height) rather than O(n): each comparison throws away half the tree.
"""
def search_bst(node, target):
    # O(height), not O(n) -- each comparison discards half the tree
    if not node or node.val == target:
        return node

    if target < node.val:
        return search_bst(node.left, target)
    return search_bst(node.right, target)


r"""
VALIDATE BST -- the classic trap

Checking only `left.val < node.val < right.val` locally is WRONG.
A node deep in the left subtree can still exceed an ancestor:

        5
       / \
      1   6
         / \
        4   7      <- 4 < 6 locally, but 4 < 5 breaks the BST

The valid range NARROWS as you descend. That is what lo/hi carry.
"""
def is_valid_bst(node, lo=float('-inf'), hi=float('inf')):
    if not node:
        return True

    if not (lo < node.val < hi):
        return False

    return (is_valid_bst(node.left, lo, node.val)
            and is_valid_bst(node.right, node.val, hi))


r"""
KTH SMALLEST -- the kth smallest value in a BST, 1-indexed.

Iterative inorder with an explicit stack so it can stop at the kth visit
instead of walking the whole tree.
"""
def kth_smallest(root, k):
    # Inorder = sorted, so just stop at the kth visit
    stack, node = [], root

    while stack or node:
        while node:                 # go as far left as possible
            stack.append(node)
            node = node.left

        node = stack.pop()
        k -= 1
        if k == 0:
            return node.val

        node = node.right

    return None


r"""
5. LOWEST COMMON ANCESTOR

The deepest node with both p and q somewhere below it. A node counts as
its own ancestor, so lca(p, p, q) is p.

The logic:
  - found something in BOTH subtrees -> the targets diverge HERE, so I am
    the LCA
  - only one side returned something -> the answer is down that side,
    pass it up unchanged
"""
def lca(root, p, q):
    if not root or root is p or root is q:
        return root

    left = lca(root.left, p, q)
    right = lca(root.right, p, q)

    if left and right:
        return root         # p and q split here

    return left or right    # both on one side, bubble it up


r"""
LCA IN A BST -- the same question, but the ordering removes the recursion.
Walk down while both targets sit on the same side; the moment they split
(or one of them IS the current node) you are standing on the answer.
"""
def lca_bst(root, p, q):
    # In a BST you do not need recursion: just walk while both
    # targets are on the same side
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root     # they split here (or one IS root)

    return None


r"""
WHEN A TREE IS SECRETLY A GRAPH

Some "tree" problems need to move UPWARD, which tree recursion cannot do.
Fix: build parent pointers, and now every node has three neighbours
(left, right, parent). It is a plain undirected graph and all the
graphs.py tools apply.

All Nodes Distance K in Binary Tree is exactly this: wire parents, then
BFS with levels -- and now you DO need a visited set, because you can
walk back up.
"""
r"""
WIRE PARENTS -- build a {node: parent} map so you can walk UPWARD.
The root maps to None.
"""
def wire_parents(root):
    parent = {}

    def walk(node, par=None):
        if not node:
            return
        parent[node] = par
        walk(node.left, node)
        walk(node.right, node)

    walk(root)
    return parent


r"""
DISTANCE K -- every value exactly k edges from target, in any direction
(down into subtrees, or up through the parent and back down).
"""
def distance_k(root, target, k):
    parent = wire_parents(root)

    queue = deque([target])
    visited = {target}          # needed now: the graph has cycles
    dist = 0

    while queue:
        if dist == k:
            return [node.val for node in queue]

        for _ in range(len(queue)):
            node = queue.popleft()

            for nb in (node.left, node.right, parent[node]):
                if nb and nb not in visited:
                    visited.add(nb)
                    queue.append(nb)

        dist += 1

    return []

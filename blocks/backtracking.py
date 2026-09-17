r"""
BACKTRACKING

Explore a choice, and if it does not work out, UNDO it and try the next
one. It is how you enumerate every possibility without building them all
in memory at once.

You have written this already -- all_root_to_leaf_paths in trees.py:

    path.append(node.val)     # choose
    dfs(node.left)            # explore
    path.pop()                # UNDO

Backtracking is DFS that cleans up after itself on the way back out.

THE TEMPLATE -- three beats, every time:

    def backtrack(start):
        if <goal reached>:
            result.append(path[:])      # COPY
            return
        for choice in <options>:
            path.append(choice)         # choose
            backtrack(...)              # explore
            path.pop()                  # undo

Two things to burn in:

  - path[:] not path. Append `path` and every entry in `result` is the
    SAME list object -- they all mutate together and end up identical
    (usually all empty, since path is empty when you finish).

  - The pop must run on EVERY return path. One missing undo and later
    branches inherit stale state from a branch that already finished.

Key point: every backtracking problem is this template. The only things
that change are "what counts as a choice" and "when am I done".
"""


r"""
SUBSETS -- the simplest instance

Every node of the recursion tree is a valid answer, not just the leaves,
so you record on the way IN and there is no goal test at all.

start stops you from reusing earlier elements, which is what makes
[1,2] and [2,1] the same subset rather than two.
"""
def subsets(nums):
    result = []
    path = []

    def backtrack(start):
        result.append(path[:])          # every partial path IS a subset

        for i in range(start, len(nums)):
            path.append(nums[i])        # choose
            backtrack(i + 1)            # explore -- i+1 forbids reusing nums[i]
            path.pop()                  # undo

    backtrack(0)
    return result


r"""
PERMUTATIONS -- order matters, so `start` disappears

In a subset, [1,2] and [2,1] are the same. In a permutation they are
different answers, so every unused element is a candidate at every
position -- you cannot restrict yourself to "later" elements.

Key point: `start` is replaced by a `used` list. Two pieces of state to
change means two pieces of state to undo.
"""
def permutations(nums):
    result = []
    path = []
    used = [False] * len(nums)

    def backtrack():
        if len(path) == len(nums):      # goal: a full-length arrangement
            result.append(path[:])
            return

        for i in range(len(nums)):
            if used[i]:
                continue                # already in the current path

            used[i] = True              # choose
            path.append(nums[i])

            backtrack()                 # explore

            path.pop()                  # undo BOTH changes
            used[i] = False

    backtrack()
    return result


r"""
COMBINATION SUM -- reuse allowed, and the first taste of pruning

Key point: recurse with `i`, not `i + 1`. That single character is the
difference between "each number once" and "each number as often as you
like".

The `remaining < 0` check is pruning: once you have overshot the target
there is no way back, so stop instead of exploring a doomed branch.
"""
def combination_sum(candidates, target):
    result = []
    path = []

    def backtrack(start, remaining):
        if remaining == 0:              # hit it exactly
            result.append(path[:])
            return
        if remaining < 0:               # overshot -- PRUNE
            return

        for i in range(start, len(candidates)):
            path.append(candidates[i])
            backtrack(i, remaining - candidates[i])     # i, NOT i+1: reuse allowed
            path.pop()

    backtrack(0, target)
    return result


r"""
BACKTRACKING ON A GRID -- Word Search

Compare this with dfs_on_grid in graphs.py. That one marks a cell and
leaves it marked forever, because it only ever asks "have I been here".

Here a cell is off-limits only FOR THE CURRENT PATH. A different route
through the grid is completely entitled to use it, so the mark has to be
lifted on the way out.

Key point: mark, recurse, UNMARK. That one extra line is the entire
difference between flood fill and backtracking on a grid.
"""
def word_search(board, word):
    rows, cols = len(board), len(board[0])

    def backtrack(r, c, i):
        if i == len(word):              # matched every letter
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False                # bounds BEFORE indexing
        if board[r][c] != word[i]:
            return False                # wrong letter

        board[r][c] = "#"               # choose: block this cell for this path

        found = (backtrack(r + 1, c, i + 1)
                 or backtrack(r - 1, c, i + 1)
                 or backtrack(r, c + 1, i + 1)
                 or backtrack(r, c - 1, i + 1))

        board[r][c] = word[i]           # UNDO: restore it for other paths
        return found

    return any(backtrack(r, c, 0) for r in range(rows) for c in range(cols))


r"""
PRUNING -- N-Queens

Everything above explores an option and rejects it afterwards. Pruning
refuses the option UP FRONT, so entire branches are never entered.

A queen attacks along its column and both diagonals. Track all three in
sets, and a square is legal only if it misses all three:

    col        the column index
    r - c      constant along a "\" diagonal
    r + c      constant along a "/" diagonal

Key point: place exactly one queen per ROW. Rows then cannot conflict by
construction, and the only question at depth r is which column.
"""
def n_queens(n):
    result = []
    placed = []                         # placed[r] = column used in row r
    cols, diag, anti = set(), set(), set()

    def backtrack(r):
        if r == n:                      # all n rows filled
            result.append(["." * c + "Q" + "." * (n - c - 1) for c in placed])
            return

        for c in range(n):
            if c in cols or (r - c) in diag or (r + c) in anti:
                continue                # PRUNE: attacked, do not even recurse

            cols.add(c)                 # choose
            diag.add(r - c)
            anti.add(r + c)
            placed.append(c)

            backtrack(r + 1)            # explore

            cols.remove(c)              # undo all four
            diag.remove(r - c)
            anti.remove(r + c)
            placed.pop()

    backtrack(0)
    return result

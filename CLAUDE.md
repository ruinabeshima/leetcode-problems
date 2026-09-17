# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A personal study repo for LeetCode / DSA interview prep in Python. It is **not** an
application — there is no build, no dependencies, no test suite, and no git history.

The `.py` files are **reference implementations written to be learned from**. The
explanatory docstrings and inline comments are the point of the files, not decoration
around it. Preserve that character when editing: an implementation here is only useful
if the reasoning next to it is intact.

## Layout

| File | Contents |
|---|---|
| `graphs.py` | The 5 graph blocks + plain BFS/DFS |
| `trees.py` | 3 core tree blocks + BST and LCA, with a `TreeNode` class |
| `linked_lists.py` | 5 linked-list blocks, with `ListNode` and `build`/`to_list` helpers |
| `heaps.py` | The top-K block, `heapq` basics, and the two-heap median |
| `backtracking.py` | The choose/explore/undo template + subsets, permutations, grid search, pruning |
| `tries.py` | `TrieNode`/`Trie` + wildcard search |
| `sliding_window.py` | Fixed + variable window blocks, and opposite-end two pointers |
| `main.py` | Scratch pad for whatever LeetCode problem is being solved right now. Overwritten per problem — do not treat its contents as durable. |
| `leetcode_sync.py` | Reads the solutions repo (directories + git history) and writes the two generated files. Stdlib only, offline, no credentials. Not study material — do not apply the file-style rules below to it. |
| `LEETCODE.md` | **Generated** by `leetcode_sync.py`. What the user has actually solved, mapped onto the blocks below. Read it before recommending practice problems. Never hand-edit. |
| `leetcode_data.json` | **Generated.** The derived record behind `LEETCODE.md` — one entry per problem plus its solve dates. |
| `neetcode_lists.json` | **Generated**, then committed. NeetCode's own problem table (450 problems, `blind75`/`neetcode150` flags). The only thing ever fetched from the network; cached so runs work offline. Refresh with `--refresh-lists`. |

## The solutions repo

Accepted solutions live in a **separate git repo**, `../leetcode-problems`, one directory
per problem named `<id>-<slug>/` containing the LeetCode `README.md` and a `<slug>.py`.
It is written by **LeetSync**, a browser extension that commits on every accepted
submission — so it is machine-managed. Never hand-edit or reorganise it; a rename breaks
the mapping back to LeetCode, and the extension will fight you.

That auto-committing is what makes the review system work: **commit dates in that repo
are real solve dates**, and a re-solve is a new commit, so solve counts and recency are
computed rather than logged. The study files in this repo are being migrated into that
one; `leetcode_sync.py` auto-detects the solutions repo either alongside (`../`) or as
its own directory, so it keeps working before and after the move.

## Knowing what the user has solved

`LEETCODE.md` is the source of truth for what has actually been practised. Regenerate it
with `python3 leetcode_sync.py` — it reads the solutions repo and nothing else, so it
needs no cookie, no API and no network, and it cannot go stale in a way a re-run will not
fix. Just re-run it rather than reasoning about whether it is current.

**It knows only what LeetSync committed.** A problem solved while the extension was not
running does not exist as far as this repo is concerned, and will be reported as unsolved.
That is a deliberate trade — no credential to keep alive — and the fix is to re-solve it,
which writes the commit. Do not try to patch around it by hand.

Three sections matter, and they answer different questions:

- **Curriculum progress** — where they are in the study lists. Answers *what next*.
- **Due for review** — solved problems that have gone cold. Answers *what to redo*.
- **Coverage by block** — a canonical problem for every block and twist named below,
  marked solved or not, so a block flagged **never done** is a real gap. Answers *which
  technique is missing*.

Recommend from the gaps, not from a generic list.

## Practice order

The user works a fixed curriculum, and recommendations must follow it. Always say which
list a suggestion comes from:

1. **Blind 75**
2. **NeetCode 150**
3. **NeetCode All (450)**
4. Free choice

The tiers in `LEETCODE.md` are disjoint — each problem is counted only in the earliest
list containing it — so the first tier with anything remaining is the one to recommend
from. Off-list problems are welcome when there is a real reason, but name the reason and
say it is off-list rather than quietly substituting one.

Where a list's ordering fights this repo's block/twist framework, **flag it and let them
decide** — do not silently reorder. The standing example: Blind 75 includes Word Search
but not Subsets, which is the base template Word Search is a twist on.

Note there is no published `neetcode250` flag in NeetCode's data, so tier 3 is their full
450 set rather than the 250. Say "NeetCode All (450)", not "NeetCode 250".

## Active recall

Re-solving is scheduled by a fixed ladder keyed to rep count: the 1st solve comes back in
3 days, then 7, 21, 60, 180. Reps and recency come from git history in the solutions repo,
so there is nothing to log.

The protocol is **recall, not reading**:

1. Open the problem's `README.md` in its directory — the statement only.
2. The user retypes the solution from memory into a scratch file.
3. Only then `diff` against the committed solution.

Reading the old solution and agreeing with it is not recall and does not count as a rep.
When running a review session, do not show them the committed file until step 3 — this is
the same calibrated-help rule as below, and it matters more here, because the whole point
is that retrieval failed or succeeded on its own.

A problem only leaves the queue by being **accepted on LeetCode again**, which is what
creates the new commit. Retyping it locally does not advance the ladder.

## Running things

No test runner. Verify by importing the module and calling it, from the directory
holding this file:

```bash
python3 -c "from graphs import DSU; d = DSU(6); d.union(0,1); print(d.parent, d.count)"
```

From a script elsewhere, put that directory on the import path:

```bash
PYTHONPATH=/path/to/this/repo python3 /path/to/scratch_test.py
```

Paths here are deliberately relative — these files are moving into the solutions repo,
so anything that hardcodes their current location will rot.

`trees.py` and `linked_lists.py` ship constructors for test data — `build([1,2,3])` /
`to_list(head)` for lists, and `TreeNode(val, left, right)` for trees.

## The organising framework

The three files share one idea, and it is the thing to understand before changing
anything: there is a small set of **memorised code blocks**, and everything else is a
named **twist** on one of them. This is deliberate — the user asked for the material to
be reduced to a minimum memorisation load.

**Graphs — 5 blocks:** BFS with levels · DFS on a grid · DSU · Kahn's · Dijkstra.
Connected components, multi-source BFS, boundary-in flood fill, bipartite colouring,
cycle detection, MST, 0-1 BFS and the `max(d,w)` Dijkstra variant are all presented as
one-line changes to those five, never as separate algorithms.

**Trees — 3 core + 2:** bottom-up DFS · top-down DFS · level-order BFS, plus BST
ordering and LCA. Level-order BFS is explicitly the same code as `bfs_with_levels` in
`graphs.py`.

**Linked lists — 5 blocks:** dummy head · reverse · fast & slow · merge two sorted ·
split-reverse-merge.

**Heaps — 1 block:** top-K with a size-k heap. `heapq` is the library, so there is
nothing to implement; the only tricks are that k *largest* needs a *min*-heap, and that
max-heaps come from negating. The Dijkstra priority queue is the same structure.

**Backtracking — 1 template:** choose · explore · undo. Subsets, permutations,
combination sum, grid word search and N-Queens are that template with a different notion
of "choice" — plus, for N-Queens, up-front pruning. `all_root_to_leaf_paths` in
`trees.py` is the same idea and is cross-referenced from there.

**Tries — 1 block:** `children` dict + `is_word` flag. Wildcard search is the same walk
turned recursive.

**Sliding window — 1 template, 2 flavours:** `right` always advances, `left` catches up.
Longest shrinks *while invalid* and records after the `while`; shortest shrinks *while
valid* and records inside it. Where the recording goes is the whole distinction, and
putting it in the wrong place gives plausible off-by-one answers rather than a crash.
Fixed-size windows need no `left` at all. Opposite-end two pointers live in the same file
but are a separate technique.

When adding material, extend an existing block with its twist rather than introducing a
sixth algorithm. If something genuinely does not fit, say so explicitly rather than
quietly growing the set.

## File style

Match the existing convention when adding to these files:

- A module-level `r"""..."""` block **before** the function (not a docstring inside it),
  containing a title, the problem it solves, and a `Key point:` line naming the one idea
  that makes it work.
- Use `r"""` whenever the block contains ASCII diagrams — a bare `"""` with `\   /` in it
  raises a `SyntaxWarning`.
- Inline `#` comments on the non-obvious lines only, explaining *why* (`# SAVE before
  destroying`, `# prev, not curr -- curr is None`).
- Known bugs and traps are called out in the comments next to the code that causes them.
  Keep those; they are the highest-value lines in the files.

## Working with the user on problems

The user is actively learning this material, so the default here is **not** to produce
solutions.

- When they are mid-problem, they ask for calibrated help and mean it literally:
  "yes or no only", "no hints", "slight hints". Honour the level asked for and stop
  there. Escalate only when asked.
- When they submit working code, review it — run it rather than eyeballing it, construct
  counterexamples for logic gaps, and cite issues as `file.py:line`. Several real bugs in
  this repo were found by running a counterexample, not by reading.
- Explanations land best as **slow traces with concrete state**: index-labelled array
  tables after every step, ASCII tree/graph pictures, and an explicit walk through each
  sub-call. Abstract description of an invariant does not work on its own; show the
  invariant holding at each step.
- Correct terminology errors when they appear, since the vocabulary is being built from
  scratch (e.g. "union-find", not "union join"; a recursive function with no queue is
  DFS, not BFS).
- Prefer recommending fewer things. When asked to simplify, actually cut the set rather
  than reorganising it.

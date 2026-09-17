r"""
TRIES (prefix trees)

A tree where each EDGE is a letter, so a path down from the root spells
out a word.

Storing "car", "cat", "dog":

        root
        /   \
       c     d
       |     |
       a     o
      / \    |
     r   t   g
     *   *   *        (* = a word ENDS here)

"car" and "cat" share the c -> a path. That sharing is the point: asking
whether ANY stored word starts with "ca" takes two steps, no matter
whether you stored three words or thirty thousand.

It is trees.py with a different child structure -- instead of .left and
.right, a dict from character to child.

Key point: is_word is the whole design. Without it, inserting "cat"
would make search("ca") return True -- but "ca" was never a word, it is
just a node you passed through. The flag is how a node says "a word
genuinely ends here", and it is the ONLY difference between search()
and starts_with().
"""
class TrieNode:
    def __init__(self):
        self.children = {}      # char -> TrieNode
        self.is_word = False    # does a word END here?


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root

        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()      # create the branch
            node = node.children[ch]                # walk down

        node.is_word = True                         # mark the LAST node only

    def _walk(self, s):
        # Follow s from the root. Returns the node it lands on, or None
        # if the path runs out partway.
        node = self.root

        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]

        return node

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.is_word    # must be a REAL word

    def starts_with(self, prefix):
        return self._walk(prefix) is not None       # merely reaching it is enough


# Note there is no recursion anywhere above. Insert and lookup are plain
# loops over the characters -- O(len(word)) each, independent of how many
# words are stored.


r"""
WILDCARDS -- Design Add and Search Words

search(".ad") must match "bad", "dad" and "mad". A "." matches any one
letter.

Key point: the loop version dies here. A "." means you cannot know which
child to step into, so you must try ALL of them -- and trying several
options and giving up on the failures is recursion. This is the same
choose/explore/undo idea as backtracking.py, with the undo being free
because nothing was mutated.
"""
class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def add(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_word = True

    def search(self, word):
        def dfs(node, i):
            if i == len(word):
                return node.is_word         # ran out of letters: is this a word?

            ch = word[i]

            if ch == ".":
                # any child that works is enough
                return any(dfs(child, i + 1) for child in node.children.values())

            if ch not in node.children:
                return False                # dead end
            return dfs(node.children[ch], i + 1)

        return dfs(self.root, 0)


r"""
WORD SEARCH II -- where tries earn their keep

The payoff problem, and honestly the reason to learn tries at all.

Naive approach: run word_search (backtracking.py) once per word. With
thousands of words that is hopeless.

With a trie: insert every word, then walk the grid ONCE, carrying a trie
node alongside your (r, c) position. At each step, if the current letter
is not a child of the current node, then NO word in the entire list
continues this way -- abandon the branch immediately.

Key point: the trie turns "is this a prefix of any of my 30000 words?"
into a single dict lookup. That is the pruning that makes the problem
tractable, and it is exactly the pruning idea from n_queens applied to a
different kind of state.

It combines all three ideas: grid backtracking + mark/unmark + trie.
Save it until each piece is comfortable on its own.
"""

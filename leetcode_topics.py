r"""
Where a problem lives: slug -> topic directory
==============================================

One question, asked in one place: given a problem, which topic folder does its
directory belong under? Both `leetcode_pull.py` (writing new solves) and
`leetcode_sync.py` (reading old ones) import this, so a problem cannot be filed
in one place and looked for in another.

Classification runs in three steps, first hit wins:

    1. OVERRIDES        hand-set, for anything the other two get wrong
    2. NeetCode pattern  from neetcode_lists.json -- covers all 450 on-list
    3. LeetCode topicTags  fetched once into leetcode_tags.json, then cached

Key point: topic directory names must never match "<digits>-<rest>", because
that is exactly the pattern for a problem directory. "1-D Dynamic Programming"
would slugify to "1-d-dynamic-programming" and be parsed as problem #1 -- which
is why the DP folders here are "dp-1d" and "dp-2d" rather than the literal
NeetCode names.

Usage
-----
    python3 leetcode_topics.py            # print the classification of every problem
    python3 leetcode_topics.py --plan     # show the git mv plan, change nothing
    python3 leetcode_topics.py --migrate  # move the directories into topic folders
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

PROBLEM_DIR_RE = re.compile(r"^(\d+)-(.+)$")
TAGS_FILE = "leetcode_tags.json"
LISTS_FILE = "neetcode_lists.json"
GRAPHQL_URL = "https://leetcode.com/graphql/"

# NeetCode's own pattern names -> the folder each becomes. The two DP entries
# are deliberately not literal translations; see the Key point above.
PATTERN_DIRS = {
    "Arrays & Hashing": "arrays-hashing",
    "Two Pointers": "two-pointers",
    "Sliding Window": "sliding-window",
    "Stack": "stack",
    "Binary Search": "binary-search",
    "Linked List": "linked-list",
    "Trees": "trees",
    "Tries": "tries",
    "Heap / Priority Queue": "heap-priority-queue",
    "Backtracking": "backtracking",
    "Graphs": "graphs",
    "Advanced Graphs": "advanced-graphs",
    "1-D Dynamic Programming": "dp-1d",
    "2-D Dynamic Programming": "dp-2d",
    "Greedy": "greedy",
    "Intervals": "intervals",
    "Math & Geometry": "math-geometry",
    "Bit Manipulation": "bit-manipulation",
    # NeetCode files the JS-runtime problems under "JavaScript", which is a
    # language and not a pattern. Drop to the tag fallback instead.
    "JavaScript": None,
}

# LeetCode's own topic tags, for the ~15% of problems NeetCode never listed.
# ORDER IS THE ALGORITHM: a problem carries many tags and the first match wins,
# so this runs specific -> generic. "Array" and "Hash Table" sit at the bottom
# because nearly everything carries them.
TAG_DIRS = [
    # These strings are LeetCode's exact tag names, checked against the API --
    # they are not guessable. It is "Union-Find" and not "Union Find", and
    # "Graph Theory" and not "Graph"; getting either wrong silently sends the
    # problem to misc/ instead of failing loudly.
    ("Trie", "tries"),
    # Weighted/structured graph work outranks plain connectivity, so a problem
    # tagged both Union-Find and Dijkstra lands in advanced-graphs.
    ("Shortest Path", "advanced-graphs"),
    ("Dijkstra's Algorithm", "advanced-graphs"),
    ("Minimum Spanning Tree", "advanced-graphs"),
    ("Prim's Algorithm", "advanced-graphs"),
    ("Kruskal's Algorithm", "advanced-graphs"),
    ("Strongly Connected Component", "advanced-graphs"),
    # NeetCode files every union-find problem it lists under plain Graphs
    # (Redundant Connection, Accounts Merge, Number of Connected Components),
    # so match that rather than promoting them to advanced.
    ("Union-Find", "graphs"),
    ("Topological Sort", "graphs"),
    ("Binary Search Tree", "trees"),
    ("Binary Tree", "trees"),
    ("Tree", "trees"),
    ("Graph Theory", "graphs"),
    ("Backtracking", "backtracking"),
    ("Heap (Priority Queue)", "heap-priority-queue"),
    ("Linked List", "linked-list"),
    ("Monotonic Stack", "stack"),
    ("Stack", "stack"),
    ("Sliding Window", "sliding-window"),
    ("Two Pointers", "two-pointers"),
    # Before Binary Search on purpose: Longest Increasing Subsequence carries
    # both, and it is a DP problem that happens to have a binary-search speedup.
    ("Dynamic Programming", "dp-1d"),
    ("Binary Search", "binary-search"),
    ("Greedy", "greedy"),
    ("Bit Manipulation", "bit-manipulation"),
    ("Geometry", "math-geometry"),
    ("Math", "math-geometry"),
    ("Prefix Sum", "arrays-hashing"),
    ("Sorting", "arrays-hashing"),
    ("Counting", "arrays-hashing"),
    ("Hash Table", "arrays-hashing"),
    ("String", "arrays-hashing"),
    ("Array", "arrays-hashing"),
]

# Anything the two automatic steps get wrong. Edit freely -- this always wins.
# "Dynamic Programming" cannot tell 1-D from 2-D, so multi-dimensional DP
# problems that NeetCode never listed have to be named here.
OVERRIDES = {}

FALLBACK_DIR = "misc"
TOPIC_DIRS = sorted(set(v for v in PATTERN_DIRS.values() if v)
                    | set(v for _, v in TAG_DIRS) | {FALLBACK_DIR})


def graphql(query, variables, timeout=20):
    """POST a query to LeetCode's public GraphQL endpoint. No auth needed here."""
    body = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(GRAPHQL_URL, data=body, headers={
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (leetcode-topics)",
        "Referer": "https://leetcode.com",
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


TAGS_QUERY = """
query questionTags($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionFrontendId
    title
    difficulty
    topicTags { name slug }
  }
}
"""


def load_json(path, default):
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return default


def load_patterns(repo):
    """{slug: NeetCode pattern} from the committed list file."""
    entries = load_json(Path(repo) / LISTS_FILE, [])
    return {e["slug"]: e.get("pattern", "") for e in entries}


def load_tags(repo):
    """{slug: [tag, ...]} from the local cache. Missing file just means empty."""
    return load_json(Path(repo) / TAGS_FILE, {})


def save_tags(repo, tags):
    path = Path(repo) / TAGS_FILE
    path.write_text(json.dumps(tags, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def fetch_tags(slug):
    """Topic tags for one problem, or None if LeetCode will not say."""
    try:
        data = graphql(TAGS_QUERY, {"titleSlug": slug})
    except (urllib.error.URLError, OSError, ValueError, TimeoutError):
        return None
    question = (data.get("data") or {}).get("question")
    if not question:
        return None
    return [t["name"] for t in question.get("topicTags") or []]


def topic_for(slug, patterns=None, tags=None):
    """The topic folder for one problem slug. Always returns something."""
    if slug in OVERRIDES:
        return OVERRIDES[slug]
    pattern = (patterns or {}).get(slug)
    if pattern:
        mapped = PATTERN_DIRS.get(pattern)
        if mapped:
            return mapped
    have = set((tags or {}).get(slug) or [])
    for tag, folder in TAG_DIRS:
        if tag in have:
            return folder
    return FALLBACK_DIR


def classify_all(repo, slugs, fetch_missing=True, log=None):
    """{slug: folder} for many problems, filling the tag cache as needed.

    Only slugs that NeetCode never listed cost a request, and the answer is
    cached, so a second run over the same repo touches the network zero times.
    """
    patterns, tags = load_patterns(repo), load_tags(repo)
    unknown = [s for s in slugs
               if s not in OVERRIDES
               and not PATTERN_DIRS.get(patterns.get(s) or "")
               and s not in tags]
    if unknown and fetch_missing:
        for slug in unknown:
            if log:
                log(f"  fetching tags for off-list problem: {slug}")
            fetched = fetch_tags(slug)
            if fetched is not None:
                tags[slug] = fetched
        if tags:
            save_tags(repo, tags)
    return {s: topic_for(s, patterns, tags) for s in slugs}


def find_problem_dirs(repo):
    """{slug: path-relative-to-repo} for every problem directory, nested or not.

    Walks rather than lists, so it finds problems both before the migration
    (flat at the root) and after it (one level down, under a topic folder).
    """
    repo = Path(repo)
    found = {}
    skip = {".git", "__pycache__", ".venv", "node_modules"}
    for dirpath, dirnames, _ in os.walk(repo):
        dirnames[:] = [d for d in dirnames if d not in skip]
        for name in list(dirnames):
            if PROBLEM_DIR_RE.match(name):
                rel = Path(dirpath, name).relative_to(repo)
                found[PROBLEM_DIR_RE.match(name).group(2)] = rel.as_posix()
                dirnames.remove(name)  # a problem dir holds no other problems
    return found


def plan_migration(repo):
    """[(old_rel, new_rel), ...] for every problem not already in its folder."""
    current = find_problem_dirs(repo)
    topics = classify_all(repo, sorted(current), log=lambda m: print(m, file=sys.stderr))
    moves = []
    for slug, old in sorted(current.items()):
        new = f"{topics[slug]}/{Path(old).name}"
        if old != new:
            moves.append((old, new))
    return moves, topics


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--repo", default=".", help="the solutions repo")
    parser.add_argument("--plan", action="store_true", help="show moves, change nothing")
    parser.add_argument("--migrate", action="store_true", help="perform the moves")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    moves, topics = plan_migration(repo)

    if not args.plan and not args.migrate:
        for slug, folder in sorted(topics.items(), key=lambda kv: (kv[1], kv[0])):
            print(f"{folder:22} {slug}")
        return 0

    if not moves:
        print("Nothing to move -- every problem is already in its topic folder.")
        return 0

    print(f"{len(moves)} directories to move:\n")
    for old, new in moves:
        print(f"  {old}  ->  {new}")

    if args.plan:
        print("\n(--plan: nothing changed)")
        return 0

    for old, new in moves:
        (repo / new).parent.mkdir(parents=True, exist_ok=True)
        # git mv, so the move is recorded as a rename and the file keeps its
        # history. leetcode_sync.py filters renames out of the solve log.
        result = subprocess.run(["git", "mv", old, new], cwd=str(repo),
                                capture_output=True, text=True)
        if result.returncode != 0:
            print(f"FAILED {old}: {result.stderr.strip()}", file=sys.stderr)
            return 1
    print(f"\nMoved {len(moves)} directories. Nothing is committed yet -- review with "
          "`git status`, then commit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

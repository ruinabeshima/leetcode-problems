r"""
LeetCode progress, read out of the solutions repo
=================================================

Reads the LeetSync solutions repo -- one directory per problem, named
"<id>-<slug>", holding the LeetCode README and the accepted solution -- and
writes two files:

    leetcode_data.json   the derived record (structured, diffable between runs)
    LEETCODE.md          a Claude-facing summary: what to solve next, what has
                         gone cold, and which memorised block is still missing

Key point: LeetSync commits on every accepted submission, so the git history IS
the study log. Commit dates are solve dates and a re-solve is another commit,
which is what lets the review schedule be computed rather than logged. Nothing
here talks to LeetCode -- no session cookie, no API, no expiry.

The one thing git cannot see is a problem solved while the extension was not
running; it simply looks unsolved. That is the accepted trade for having no
credential to keep alive. Re-solve it and it reappears.

The only network call left is the NeetCode study lists, fetched once into
neetcode_lists.json and then read from disk. Commit that file and this script
never needs the network again.

Usage
-----
    python3 leetcode_sync.py                       # auto-detect the repo
    python3 leetcode_sync.py --problems-dir ~/foo  # point it elsewhere
    python3 leetcode_sync.py --refresh-lists       # re-download the lists
"""

import argparse
import json
import re
import subprocess
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

import leetcode_topics as topics

# LeetSync's directory naming. The id and slug are the whole mapping back to
# LeetCode, which is why the repo must never be hand-reorganised.
PROBLEM_DIR_RE = re.compile(r"^(\d+)-(.+)$")
TITLE_RE = re.compile(r'<h2><a href="[^"]*">([^<]+)</a></h2>')
DIFFICULTY_RE = re.compile(r"Difficulty-(Easy|Medium|Hard)")

# NeetCode publishes its own problem table with a flag per curated list. Using
# it beats hand-typing hundreds of slugs: the lists stay whatever NeetCode says.
# It ships blind75 and neetcode150 flags only -- there is no neetcode250 flag in
# that data, so the third tier below is NeetCode's full set, not the 250.
NEETCODE_URL = ("https://raw.githubusercontent.com/neetcode-gh/leetcode/"
                "main/.problemSiteData.json")
LISTS_FILE = "neetcode_lists.json"

# The order the user works through them. Each tier is (label, flag); a flag of
# None means "everything in NeetCode's set not already claimed by an earlier
# tier", so the tiers are disjoint and the first unfinished one is what is next.
CURRICULUM = [
    ("Blind 75", "blind75"),
    ("NeetCode 150", "neetcode150"),
    ("NeetCode All (450)", None),
]

# Spaced repetition: the number of times a problem has been solved picks the
# interval before it is due again. Solve it once and it returns in 3 days; get
# it right five times and it goes quiet for half a year.
REVIEW_LADDER = [3, 7, 21, 60, 180]
REVIEW_SHOWN = 15  # rows in the markdown table; the rest are counted, not listed

# How many problems to review in a day. THE BACKLOG IS NOT THE WORKLOAD: once a
# few dozen problems have gone cold, printing all of them is a wall rather than
# a plan, and the queue stops being something anyone acts on. So the queue names
# today's problem and counts the rest.
#
# Whether today's is already done is computed, like everything else here: a
# commit dated today on a problem that had been solved before is a review. A
# first-ever solve is new work and does not spend the day's quota.
REVIEWS_PER_DAY = 1

# The canonical problem for each block and each named twist in CLAUDE.md. This
# is what turns "you solved 40 graph problems" into "you have never done
# Kahn's". Edit freely -- it is a study list, not data from anywhere.
CANON = {
    "blocks/graphs.py": {
        "BFS with levels": ["binary-tree-level-order-traversal", "word-ladder"],
        "multi-source BFS (twist)": ["rotting-oranges", "01-matrix"],
        "DFS on a grid": ["number-of-islands", "max-area-of-island"],
        "boundary-in flood fill (twist)": ["surrounded-regions", "pacific-atlantic-water-flow"],
        "DSU": ["redundant-connection", "number-of-provinces", "accounts-merge"],
        "Kahn's": ["course-schedule", "course-schedule-ii"],
        "Dijkstra": ["network-delay-time", "path-with-maximum-probability"],
        "max(d,w) Dijkstra (twist)": ["swim-in-rising-water", "path-with-minimum-effort"],
        "bipartite colouring (twist)": ["is-graph-bipartite"],
        "0-1 BFS (twist)": ["minimum-obstacle-removal-to-reach-corner"],
    },
    "blocks/trees.py": {
        "bottom-up DFS": ["maximum-depth-of-binary-tree", "diameter-of-binary-tree",
                          "balanced-binary-tree", "binary-tree-maximum-path-sum"],
        "top-down DFS": ["path-sum", "path-sum-ii", "sum-root-to-leaf-numbers"],
        "level-order BFS": ["binary-tree-level-order-traversal", "binary-tree-right-side-view"],
        "BST ordering": ["validate-binary-search-tree", "kth-smallest-element-in-a-bst"],
        "LCA": ["lowest-common-ancestor-of-a-binary-tree",
                "lowest-common-ancestor-of-a-binary-search-tree"],
    },
    "blocks/linked_lists.py": {
        "dummy head": ["remove-linked-list-elements", "remove-nth-node-from-end-of-list"],
        "reverse": ["reverse-linked-list", "reverse-linked-list-ii"],
        "fast & slow": ["linked-list-cycle", "linked-list-cycle-ii", "middle-of-the-linked-list"],
        "merge two sorted": ["merge-two-sorted-lists"],
        "split-reverse-merge": ["reorder-list", "palindrome-linked-list"],
    },
    "blocks/heaps.py": {
        "top-K with a size-k heap": ["kth-largest-element-in-an-array", "top-k-frequent-elements",
                                     "k-closest-points-to-origin", "merge-k-sorted-lists"],
        "two-heap median": ["find-median-from-data-stream"],
    },
    "blocks/backtracking.py": {
        "choose/explore/undo": ["subsets", "permutations", "combination-sum",
                                "letter-combinations-of-a-phone-number"],
        "dedup on a sorted array (twist)": ["subsets-ii", "combination-sum-ii", "permutations-ii"],
        "grid search (twist)": ["word-search"],
        "up-front pruning (twist)": ["n-queens"],
        "partition (twist)": ["palindrome-partitioning"],
    },
    "blocks/tries.py": {
        "children dict + is_word": ["implement-trie-prefix-tree"],
        "wildcard search (twist)": ["design-add-and-search-words-data-structure"],
        "trie + grid backtracking (twist)": ["word-search-ii"],
    },
    "blocks/sliding_window.py": {
        "longest (shrink while invalid)": ["longest-substring-without-repeating-characters",
                                           "longest-repeating-character-replacement",
                                           "max-consecutive-ones-iii"],
        "shortest (shrink while valid)": ["minimum-size-subarray-sum", "minimum-window-substring"],
        "fixed-size window": ["maximum-average-subarray-i", "permutation-in-string"],
        "opposite-end two pointers": ["two-sum-ii-input-array-is-sorted", "3sum",
                                      "container-with-most-water", "trapping-rain-water",
                                      "valid-palindrome"],
    },
}


# ---------------------------------------------------------------------------
# Reading the solutions repo
# ---------------------------------------------------------------------------
def find_problems_dir(start, explicit=None):
    """Locate the solutions repo: given, here, or next door.

    After the study files move into the solutions repo these are the same
    directory, so check that first and the script keeps working across the move.
    """
    if explicit:
        path = Path(explicit).expanduser()
        return path if path.is_dir() else None
    here = Path(start).resolve()
    for cand in (here, here.parent / "leetcode-problems"):
        # Not a listdir: after the topic migration the problem directories sit
        # one level down, under graphs/, trees/ and so on.
        if cand.is_dir() and topics.find_problem_dirs(cand):
            return cand
    return None


def scan_problems(problems_dir):
    """One record per problem directory, title and difficulty out of its README."""
    found = []
    for slug, rel in sorted(topics.find_problem_dirs(problems_dir).items()):
        name = Path(rel).name
        pid = int(PROBLEM_DIR_RE.match(name).group(1))
        parent = Path(rel).parent
        topic = "" if parent == Path(".") else parent.as_posix()
        title, difficulty = slug, ""
        readme = Path(problems_dir) / rel / "README.md"
        if readme.exists():
            text = readme.read_text(encoding="utf-8", errors="replace")
            found_title = TITLE_RE.search(text)
            found_diff = DIFFICULTY_RE.search(text)
            if found_title:
                title = found_title.group(1).strip()
            if found_diff:
                difficulty = found_diff.group(1)
        found.append({"id": pid, "slug": slug, "title": title,
                      "difficulty": difficulty, "dir": rel, "topic": topic})
    return sorted(found, key=lambda p: p["id"])


def slug_from_path(path):
    """The problem slug out of a repo-relative path, flat or nested.

    Paths read "207-course-schedule/x.py" before the topic migration and
    "graphs/207-course-schedule/x.py" after it -- and commits made before the
    move keep their old paths forever, so scan the segments for the one that
    looks like a problem rather than assuming which position it is in.
    """
    for segment in path.split("/"):
        match = PROBLEM_DIR_RE.match(segment)
        if match:
            return match.group(2)
    return None


def solve_history(problems_dir):
    """{slug: [date, ...]} -- the distinct days each problem was accepted.

    One `git log` for the whole repo, not one per directory. LeetSync commits
    the solution and its README separately, so dedupe by date rather than
    counting commits, or every solve looks like two.
    """
    try:
        proc = subprocess.run(
            # --diff-filter=AM is load-bearing: moving the problem directories
            # into topic folders is a rename, and without this filter every
            # moved problem would read as having been re-solved on the day of
            # the move, resetting 75 review schedules at once.
            ["git", "log", "--format=@%at", "--name-only", "--no-merges",
             "--diff-filter=AM"],
            cwd=str(problems_dir), capture_output=True, text=True, timeout=120,
        )
    except (OSError, subprocess.SubprocessError):
        return {}
    if proc.returncode != 0:
        return {}

    history, when = {}, None
    for line in proc.stdout.splitlines():
        if line.startswith("@"):
            when = datetime.fromtimestamp(int(line[1:]), timezone.utc).date()
        elif line.strip() and when is not None:
            # Only the solution file marks a solve; the README commit is noise.
            if line.endswith(".md"):
                continue
            slug = slug_from_path(line)
            if slug:
                history.setdefault(slug, set()).add(when)
    return {slug: sorted(dates, reverse=True) for slug, dates in history.items()}


def reviews_done_today(history, today=None):
    """Problems re-solved today, newest first.

    Distinguishes a review from new work by rep count: a problem whose only
    solve date is today is a first solve, not a review, and must not count
    against the day's quota.
    """
    today = today or datetime.now(timezone.utc).date()
    return [slug for slug, dates in history.items()
            if dates and dates[0] == today and len(dates) > 1]


def due_for_review(history, today=None):
    """Problems past their interval, most overdue first."""
    today = today or datetime.now(timezone.utc).date()
    due = []
    for slug, dates in history.items():
        reps = len(dates)
        interval = REVIEW_LADDER[min(reps, len(REVIEW_LADDER)) - 1]
        age = (today - dates[0]).days
        if age >= interval:
            due.append({"slug": slug, "age": age, "interval": interval, "reps": reps,
                        "last": dates[0].isoformat(), "overdue": age - interval})
    return sorted(due, key=lambda d: -d["overdue"])


# ---------------------------------------------------------------------------
# Curriculum lists
# ---------------------------------------------------------------------------
def fetch_lists():
    """Download NeetCode's problem table, trimmed to the fields used here."""
    req = urllib.request.Request(NEETCODE_URL, headers={"User-Agent": "leetcode-sync"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = json.loads(resp.read().decode("utf-8"))
    out = []
    for entry in raw:
        # "contains-duplicate/" -> "contains-duplicate"; matches LeetCode slugs.
        slug = (entry.get("link") or "").strip("/")
        if slug:
            out.append({"slug": slug, "title": entry.get("problem", slug),
                        "difficulty": entry.get("difficulty", ""),
                        "pattern": entry.get("pattern", ""),
                        "blind75": entry.get("blind75") is True,
                        "neetcode150": entry.get("neetcode150") is True})
    return out


def load_lists(out_dir, refresh=False):
    """Vendored copy of the lists, downloaded once so later runs work offline."""
    path = Path(out_dir) / LISTS_FILE
    if path.exists() and not refresh:
        try:
            return json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            pass  # a corrupt cache is not worth dying over -- refetch
    try:
        lists = fetch_lists()
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
        print(f"  could not fetch the NeetCode lists ({exc}); skipping curriculum")
        return None
    path.write_text(json.dumps(lists, indent=2, ensure_ascii=False) + "\n")
    print(f"  wrote {path.name} ({len(lists)} problems)")
    return lists


def tier_of(entry):
    """Which tier a problem belongs to -- the earliest list that claims it."""
    for label, flag in CURRICULUM:
        if flag is None or entry[flag]:
            return label
    return CURRICULUM[-1][0]


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------
def render_curriculum(lists, solved_slugs):
    """The ordered study lists, and what is left in the tier being worked on."""
    lines, add = [], None
    add = lines.append
    order = [label for label, _ in CURRICULUM]
    tiers = {label: [] for label in order}
    for entry in lists:
        tiers[tier_of(entry)].append(entry)

    add("## Curriculum progress")
    add("")
    add("Work these in order — " + " → ".join(order) + " → anything else.")
    add("Tiers are disjoint: a problem is counted only in the earliest list that")
    add("contains it, so the first row with anything remaining is what comes next.")
    add("")
    add("| Tier | Solved | Total | Remaining |")
    add("|---|---|---|---|")
    current = None
    for label in order:
        done = sum(1 for e in tiers[label] if e["slug"] in solved_slugs)
        left = len(tiers[label]) - done
        if left and current is None:
            current = label
        add(f"| {label} | {done} | {len(tiers[label])} | {left} |")
    add("")

    if current is None:
        add("All tiers complete — pick freely.")
        add("")
        return lines

    remaining = [e for e in tiers[current] if e["slug"] not in solved_slugs]
    add(f"### Next up: {current} — {len(remaining)} left")
    add("")
    add("In NeetCode's own order, grouped by pattern. Recommend from here first.")
    add("")
    by_pattern = {}
    for entry in remaining:
        by_pattern.setdefault(entry["pattern"], []).append(entry)
    for pattern, entries in by_pattern.items():
        add(f"- **{pattern}** ({len(entries)})")
        for e in entries:
            add(f"  - [ ] [{e['title']}](https://leetcode.com/problems/{e['slug']}/)"
                f" · {e['difficulty']}")
    add("")
    return lines


def render_review(history, titles, lists=None, per_day=REVIEWS_PER_DAY):
    """The active-recall queue: what has gone cold, most valuable first.

    Ordered by curriculum tier before staleness. Sorting on overdue days alone
    buries Blind 75 problems under every Easy warm-up ever solved, which is the
    opposite of what limited review time should buy.
    """
    lines = []
    add = lines.append
    rank = {}
    if lists:
        order = [label for label, _ in CURRICULUM]
        for entry in lists:
            rank[entry["slug"]] = order.index(tier_of(entry))
    off_list = len(CURRICULUM)  # never on a NeetCode list -> review last
    tier_name = {i: label for i, (label, _) in enumerate(CURRICULUM)}

    add("## Due for review")
    add("")
    add("Commit dates in the solutions repo are the solve dates, so this is")
    add("computed, not logged. Interval by rep count: "
        + " · ".join(f"{i + 1}→{d}d" for i, d in enumerate(REVIEW_LADDER)) + ".")
    add("")
    add("**Protocol — recall, do not read.** Open the problem's `README.md`, retype")
    add("the solution from memory into a scratch file, and only then `diff` it against")
    add("the committed one. Reading the old solution and nodding is not recall.")
    add("A problem leaves this queue by being accepted on LeetCode again, which is")
    add("what writes the new commit — retyping it locally does not advance the ladder.")
    add("")
    due = due_for_review(history)
    if not due:
        add(f"Nothing due — all {len(history)} solved problems are inside their interval.")
        add("")
        return lines

    due.sort(key=lambda d: (rank.get(d["slug"], off_list), -d["overdue"]))
    done = reviews_done_today(history)
    remaining = max(0, per_day - len(done))
    days_to_clear = -(-len(due) // per_day) if per_day else 0

    plural = "" if per_day == 1 else "s"
    add(f"**Limit: {per_day} review{plural} per day.** {len(due)} of {len(history)} "
        f"solved problems are cold, but that is the backlog, not today's work — "
        f"at {per_day}/day it is ~{days_to_clear} days of review.")
    add("")

    if not remaining:
        names = ", ".join(f"**{titles.get(s, s)}**" for s in done)
        add(f"### Done for today")
        add("")
        add(f"Already re-solved {names} today. Nothing further is due — "
            f"do new problems instead, or stop.")
        add("")
        add(f"Next in line tomorrow:")
    else:
        add(f"### Today — {remaining} to do")
    add("")
    add("| Problem | List | Last solved | Age | Interval | Reps |")
    add("|---|---|---|---|---|---|")
    shown = due[:max(remaining, per_day)]
    for item in shown:
        tier = tier_name.get(rank.get(item["slug"], off_list), "—")
        add(f"| [{titles.get(item['slug'], item['slug'])}]"
            f"(https://leetcode.com/problems/{item['slug']}/) | {tier} "
            f"| {item['last']} | {item['age']}d | {item['interval']}d | {item['reps']} |")
    add("")
    if len(due) > len(shown):
        add(f"<details><summary>The other {len(due) - len(shown)} queued, "
            f"highest-value first</summary>")
        add("")
        for item in due[len(shown):len(shown) + REVIEW_SHOWN]:
            tier = tier_name.get(rank.get(item["slug"], off_list), "—")
            add(f"- [{titles.get(item['slug'], item['slug'])}]"
                f"(https://leetcode.com/problems/{item['slug']}/) — {tier}, "
                f"{item['age']}d since last solve, {item['reps']} rep"
                f"{'' if item['reps'] == 1 else 's'}")
        if len(due) > len(shown) + REVIEW_SHOWN:
            add(f"- … and {len(due) - len(shown) - REVIEW_SHOWN} more")
        add("")
        add("</details>")
        add("")
    return lines


def render_markdown(record, lists=None, per_day=REVIEWS_PER_DAY):
    problems = record["problems"]
    solved_slugs = {p["slug"] for p in problems}
    titles = {p["slug"]: p["title"] for p in problems}
    history = {s: [date.fromisoformat(d) for d in v]
               for s, v in record.get("history", {}).items()}

    lines = []
    add = lines.append
    add("# LeetCode progress")
    add("")
    add(f"Generated {record['generated_at']} by `leetcode_sync.py` from "
        f"`{record['problems_dir']}`.")
    add("")
    add("Regenerate with `python3 leetcode_sync.py`. Do not hand-edit — it is overwritten.")
    add("")

    add("## Totals")
    add("")
    counts = {"Easy": 0, "Medium": 0, "Hard": 0}
    for prob in problems:
        if prob["difficulty"] in counts:
            counts[prob["difficulty"]] += 1
    add("| Difficulty | Solved |")
    add("|---|---|")
    for key in ("Easy", "Medium", "Hard"):
        add(f"| {key} | {counts[key]} |")
    add(f"| All | {len(problems)} |")
    add("")

    if lists:
        lines.extend(render_curriculum(lists, solved_slugs))
    if history:
        lines.extend(render_review(history, titles, lists, per_day))

    add("## Coverage by block")
    add("")
    add("Each block is the memorised code in that file; each twist is a one-line")
    add("change to it. A missing canonical problem is a gap worth filling.")
    add("")
    for fname, blocks in CANON.items():
        total = sum(len(v) for v in blocks.values())
        hit = sum(1 for v in blocks.values() for s in v if s in solved_slugs)
        add(f"### `{fname}` — {hit}/{total} canonical")
        add("")
        for block, slugs in blocks.items():
            done = sum(1 for s in slugs if s in solved_slugs)
            flag = "" if done else "  ← **never done**"
            add(f"- **{block}** ({done}/{len(slugs)}){flag}")
            for slug in slugs:
                mark = "x" if slug in solved_slugs else " "
                add(f"  - [{mark}] [{slug}](https://leetcode.com/problems/{slug}/)")
        add("")

    add("## All solved problems")
    add("")
    pattern_of = {e["slug"]: e["pattern"] for e in (lists or [])}
    per_pattern = {}
    for prob in problems:
        per_pattern.setdefault(pattern_of.get(prob["slug"], "Not on a NeetCode list"),
                               []).append(prob)
    for pattern in sorted(per_pattern, key=lambda p: (-len(per_pattern[p]), p)):
        probs = sorted(per_pattern[pattern], key=lambda p: p["id"])
        add(f"<details><summary><b>{pattern}</b> ({len(probs)})</summary>")
        add("")
        for prob in probs:
            reps = len(record.get("history", {}).get(prob["slug"], []))
            add(f"- {prob['id']}. [{prob['title']}]"
                f"(https://leetcode.com/problems/{prob['slug']}/) "
                f"· {prob['difficulty'] or '?'} · {reps} solve{'s' if reps != 1 else ''}")
        add("")
        add("</details>")
        add("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(
        description="Summarise LeetCode progress from the local solutions repo.")
    ap.add_argument("--problems-dir", help="the solutions repo (default: auto-detect)")
    ap.add_argument("--out-dir", default=str(Path(__file__).parent),
                    help="where to write output")
    ap.add_argument("--refresh-lists", action="store_true",
                    help=f"re-download the NeetCode study lists into {LISTS_FILE}")
    ap.add_argument("--reviews-per-day", type=int, default=REVIEWS_PER_DAY,
                    metavar="N", help="how many review problems a day the queue asks "
                    f"for (default: {REVIEWS_PER_DAY}); edit REVIEWS_PER_DAY to change "
                    "it for good")
    args = ap.parse_args()

    out = Path(args.out_dir)
    problems_dir = find_problems_dir(out, args.problems_dir)
    if not problems_dir:
        ap.error("no solutions repo found — pass --problems-dir")

    print(f"Reading {problems_dir} ...")
    problems = scan_problems(problems_dir)
    print(f"  {len(problems)} problems")

    history = solve_history(problems_dir)
    if history:
        done = len(reviews_done_today(history))
        print(f"  {len(history)} with git history, {len(due_for_review(history))} due; "
              f"{done}/{args.reviews_per_day} of today's reviews done")
    else:
        print("  no git history found — review queue skipped")

    print("Loading study lists ...")
    lists = load_lists(out, refresh=args.refresh_lists)

    record = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "problems_dir": str(problems_dir),
        "problems": problems,
        "history": {s: [d.isoformat() for d in v] for s, v in history.items()},
    }

    json_path, md_path = out / "leetcode_data.json", out / "LEETCODE.md"
    json_path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
    md_path.write_text(render_markdown(record, lists, args.reviews_per_day) + "\n")
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()

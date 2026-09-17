r"""
Accepted submissions -> commits, without a browser extension
============================================================

Replaces LeetSync. Asks LeetCode for your accepted submissions, writes each one
into the repo in the layout this repo already uses, and commits it. Run it on
demand, or leave `--watch` running while you practise.

Why this is steadier than the extension it replaces: it is *idempotent and
stateless*. The repo is the only record of what has been pulled, so a run that
fails, or a laptop that was asleep, costs nothing -- the next run notices what
is missing and writes it. Nothing has to be listening at the moment you submit.

Key point: the commit's author date is set to the *submission* timestamp, never
to "now". `leetcode_sync.py` reads commit dates as solve dates, so backfilling a
month-old submission has to land on the day it was actually solved or the whole
review schedule shifts.

Layout written, matching what is already here:

    <topic>/<id>-<slug>/README.md         the problem statement, LeetCode's HTML
    <topic>/<id>-<slug>/<slug>.<ext>      the accepted code
    <topic>/<id>-<slug>/submissions.json  every accepted submission, appended

That last file is not decoration. Re-solving a problem with byte-identical code
produces no diff, so git would have nothing to commit and the review ladder
would never advance. submissions.json always changes, so every acceptance is a
real commit.

Credentials
-----------
Needs your logged-in session cookie -- this is the one thing the extension did
not need, and the trade for not depending on a browser. Take LEETCODE_SESSION
(and csrftoken) from DevTools > Application > Cookies on leetcode.com, then:

    echo 'LEETCODE_SESSION=...' >> .leetcode_session
    echo 'csrftoken=...'        >> .leetcode_session

.leetcode_session is gitignored. The env vars of the same names also work and
take precedence. The cookie expires every few weeks; the script says so plainly
when it does, and re-pasting it is the whole fix.

Usage
-----
    python3 leetcode_pull.py                  # pull recent accepted, commit each
    python3 leetcode_pull.py --dry-run        # show what it would do, write nothing
    python3 leetcode_pull.py --watch 120      # poll every 120s until interrupted
    python3 leetcode_pull.py --backfill 500   # walk further back through history
    python3 leetcode_pull.py --push           # git push once the commits are in
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import leetcode_topics as topics

GRAPHQL_URL = "https://leetcode.com/graphql/"
SUBMISSIONS_API = "https://leetcode.com/api/submissions/"
CRED_FILE = ".leetcode_session"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 leetcode-pull"

# LeetCode's language ids -> the extension the file gets.
LANG_EXT = {
    "python": "py", "python3": "py", "pythondata": "py", "java": "java",
    "c": "c", "cpp": "cpp", "csharp": "cs", "javascript": "js", "typescript": "ts",
    "golang": "go", "go": "go", "rust": "rs", "kotlin": "kt", "swift": "swift",
    "ruby": "rb", "scala": "scala", "php": "php", "racket": "rkt",
    "erlang": "erl", "elixir": "ex", "dart": "dart", "bash": "sh",
    "mysql": "sql", "mssql": "sql", "oraclesql": "sql", "postgresql": "sql",
}
DIFFICULTY_COLOR = {"Easy": "brightgreen", "Medium": "orange", "Hard": "red"}

Q_WHOAMI = "query globalData { userStatus { userId username isSignedIn } }"

Q_RECENT = """
query recentAcSubmissions($username: String!, $limit: Int!) {
  recentAcSubmissionList(username: $username, limit: $limit) {
    id title titleSlug timestamp
  }
}
"""

Q_DETAIL = """
query submissionDetails($submissionId: Int!) {
  submissionDetails(submissionId: $submissionId) {
    code
    timestamp
    runtimeDisplay
    runtimePercentile
    memoryDisplay
    memoryPercentile
    lang { name verboseName }
  }
}
"""

Q_QUESTION = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId questionFrontendId title titleSlug difficulty content
    topicTags { name slug }
  }
}
"""


class LeetCodeError(RuntimeError):
    """Anything that means "stop and tell the user something actionable"."""


# ---------------------------------------------------------------------------
# Credentials and transport
# ---------------------------------------------------------------------------
def load_credentials(repo):
    """(session, csrf). Env wins over the file; either may supply either half."""
    session = os.environ.get("LEETCODE_SESSION", "").strip()
    csrf = os.environ.get("LEETCODE_CSRF") or os.environ.get("csrftoken") or ""
    csrf = csrf.strip()

    path = Path(repo) / CRED_FILE
    if path.exists():
        raw = path.read_text(encoding="utf-8")
        # Tolerant on purpose: people paste a whole Cookie header, a KEY=VALUE
        # pair per line, or just the bare token. Accept all three.
        for chunk in re.split(r"[\r\n;]+", raw):
            chunk = chunk.strip()
            if not chunk:
                continue
            if "=" in chunk:
                key, _, value = chunk.partition("=")
                key, value = key.strip().lower(), value.strip().strip('"')
                if key == "leetcode_session" and not session:
                    session = value
                elif key == "csrftoken" and not csrf:
                    csrf = value
            elif not session:
                session = chunk
    if not session:
        raise LeetCodeError(
            f"No session cookie. Copy LEETCODE_SESSION from your browser into "
            f"{path}, or export LEETCODE_SESSION. See the module docstring.")
    return session, csrf


def request_json(url, session, csrf, payload=None, timeout=30):
    cookie = f"LEETCODE_SESSION={session}"
    if csrf:
        cookie += f"; csrftoken={csrf}"
    headers = {
        "User-Agent": UA,
        "Referer": "https://leetcode.com",
        "Cookie": cookie,
        "Content-Type": "application/json",
    }
    if csrf:
        headers["x-csrftoken"] = csrf
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        if err.code in (401, 403):
            raise LeetCodeError(
                "LeetCode rejected the session cookie (HTTP %d). It has most "
                "likely expired -- paste a fresh LEETCODE_SESSION into %s."
                % (err.code, CRED_FILE)) from err
        if err.code == 429:
            raise LeetCodeError("Rate limited by LeetCode. Wait and re-run; "
                                "nothing was lost.") from err
        raise LeetCodeError(f"LeetCode returned HTTP {err.code} for {url}") from err
    except (urllib.error.URLError, TimeoutError, OSError) as err:
        raise LeetCodeError(f"Could not reach LeetCode: {err}") from err


def graphql(query, variables, session, csrf):
    body = request_json(GRAPHQL_URL, session, csrf,
                        {"query": query, "variables": variables})
    if body.get("errors"):
        message = "; ".join(e.get("message", "?") for e in body["errors"])
        raise LeetCodeError(f"GraphQL error: {message}")
    return body.get("data") or {}


# ---------------------------------------------------------------------------
# Reading LeetCode
# ---------------------------------------------------------------------------
def whoami(session, csrf):
    status = (graphql(Q_WHOAMI, {}, session, csrf).get("userStatus") or {})
    if not status.get("isSignedIn"):
        raise LeetCodeError(
            f"The cookie is not signed in. Re-copy LEETCODE_SESSION into {CRED_FILE}.")
    return status["username"]


def recent_accepted(session, csrf, username, limit):
    """The most recent accepted submissions. LeetCode caps this list around 20."""
    data = graphql(Q_RECENT, {"username": username, "limit": limit}, session, csrf)
    return data.get("recentAcSubmissionList") or []


def backfill_accepted(session, csrf, want):
    """Walk the paginated REST history for older accepted submissions.

    recentAcSubmissionList only reaches back about 20, which is plenty for
    polling but not for a first import. This older endpoint pages properly.
    """
    out, offset, seen = [], 0, set()
    while len(out) < want:
        url = f"{SUBMISSIONS_API}?offset={offset}&limit=20"
        body = request_json(url, session, csrf)
        dump = body.get("submissions_dump") or []
        if not dump:
            break
        for item in dump:
            if item.get("status_display") != "Accepted":
                continue
            sid = str(item.get("id"))
            if sid in seen:
                continue
            seen.add(sid)
            out.append({"id": sid, "title": item.get("title", ""),
                        "titleSlug": item.get("title_slug", ""),
                        "timestamp": int(item.get("timestamp") or 0)})
        if not body.get("has_next"):
            break
        offset += 20
        time.sleep(0.4)  # be a polite client; this endpoint rate-limits hard
    return out[:want]


def submission_detail(session, csrf, submission_id):
    data = graphql(Q_DETAIL, {"submissionId": int(submission_id)}, session, csrf)
    detail = data.get("submissionDetails")
    if not detail or not detail.get("code"):
        raise LeetCodeError(
            f"No code returned for submission {submission_id}. This is what an "
            f"expired cookie looks like -- refresh LEETCODE_SESSION in {CRED_FILE}.")
    return detail


def question_data(session, csrf, slug, cache):
    if slug not in cache:
        data = graphql(Q_QUESTION, {"titleSlug": slug}, session, csrf)
        question = data.get("question")
        if not question:
            raise LeetCodeError(f"LeetCode has no question called {slug!r}.")
        cache[slug] = question
    return cache[slug]


# ---------------------------------------------------------------------------
# Writing the repo
# ---------------------------------------------------------------------------
def render_readme(question):
    """Byte-compatible with the READMEs LeetSync already wrote here."""
    difficulty = question.get("difficulty") or "Easy"
    colour = DIFFICULTY_COLOR.get(difficulty, "lightgrey")
    slug, title = question["titleSlug"], question["title"]
    return (
        f'<h2><a href="https://leetcode.com/problems/{slug}">{title}</a></h2>'
        f" <img src='https://img.shields.io/badge/Difficulty-{difficulty}-{colour}'"
        f" alt='Difficulty: {difficulty}' /><hr>"
        f"{question.get('content') or ''}"
    )


def problem_dir(repo, question, patterns, tags):
    """<topic>/<frontend id>-<slug>, reusing the existing directory if it moved."""
    slug = question["titleSlug"]
    pid = question.get("questionFrontendId") or question.get("questionId")
    name = f"{pid}-{slug}"
    existing = topics.find_problem_dirs(repo).get(slug)
    if existing and Path(existing).name == name:
        return Path(repo) / existing       # already filed; do not fight the user

    # The question payload already carries topicTags, so a problem NeetCode
    # never listed can still be classified -- with no extra request. Without
    # this, topic_for() sees no pattern and no cached tags and quietly returns
    # misc/, which is how Number of Provinces ended up filed there.
    if slug not in tags:
        fetched = [t["name"] for t in question.get("topicTags") or []]
        if fetched:
            tags[slug] = fetched
            topics.save_tags(repo, tags)

    folder = topics.topic_for(slug, patterns, tags)
    return Path(repo) / folder / name


def record_submission(path, sub, detail):
    """Append this acceptance to submissions.json. Returns False if already there."""
    entries = []
    if path.exists():
        try:
            entries = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            entries = []
    if any(str(e.get("id")) == str(sub["id"]) for e in entries):
        return False
    entries.append({
        "id": str(sub["id"]),
        "date": datetime.fromtimestamp(int(sub["timestamp"]), timezone.utc)
                        .date().isoformat(),
        "timestamp": int(sub["timestamp"]),
        "lang": (detail.get("lang") or {}).get("name", ""),
        "runtime": detail.get("runtimeDisplay") or "",
        "runtime_percentile": round(detail.get("runtimePercentile") or 0, 2),
        "memory": detail.get("memoryDisplay") or "",
        "memory_percentile": round(detail.get("memoryPercentile") or 0, 2),
    })
    entries.sort(key=lambda e: e["timestamp"])
    path.write_text(json.dumps(entries, indent=1) + "\n", encoding="utf-8")
    return True


def git(repo, *args, env=None):
    full = dict(os.environ)
    full.update(env or {})
    return subprocess.run(["git", *args], cwd=str(repo), capture_output=True,
                          text=True, env=full)


def commit(repo, paths, message, when):
    """One commit, authored on the day of the submission rather than today."""
    rels = [str(Path(p).relative_to(repo)) for p in paths]
    added = git(repo, "add", "--", *rels)
    if added.returncode != 0:
        raise LeetCodeError(f"git add failed: {added.stderr.strip()}")
    staged = git(repo, "diff", "--cached", "--quiet", "--", *rels)
    if staged.returncode == 0:
        return False                       # nothing actually changed
    stamp = datetime.fromtimestamp(when, timezone.utc).isoformat()
    done = git(repo, "commit", "-m", message, "--", *rels,
               env={"GIT_AUTHOR_DATE": stamp, "GIT_COMMITTER_DATE": stamp})
    if done.returncode != 0:
        raise LeetCodeError(f"git commit failed: {done.stderr.strip()}")
    return True


def pull_one(repo, sub, session, csrf, cache, patterns, tags, dry_run=False,
             refresh_readme=False):
    """Fetch, write and commit a single accepted submission. Returns a status word."""
    slug = sub["titleSlug"]
    question = question_data(session, csrf, slug, cache)
    target = problem_dir(repo, question, patterns, tags)

    # Cheap skip: if this exact submission id is already recorded, it is done.
    record = target / "submissions.json"
    if record.exists():
        try:
            known = json.loads(record.read_text(encoding="utf-8"))
            if any(str(e.get("id")) == str(sub["id"]) for e in known):
                return "known", target
        except ValueError:
            pass

    detail = submission_detail(session, csrf, sub["id"])
    lang = (detail.get("lang") or {}).get("name", "python3")
    ext = LANG_EXT.get(lang, "txt")
    code = detail["code"].replace("\r\n", "\n")
    if not code.endswith("\n"):
        code += "\n"

    if dry_run:
        return ("would-add" if not target.exists() else "would-update"), target

    target.mkdir(parents=True, exist_ok=True)
    touched = []

    readme = target / "README.md"
    if refresh_readme or not readme.exists():
        readme.write_text(render_readme(question), encoding="utf-8")
        touched.append(readme)

    solution = target / f"{slug}.{ext}"
    if not solution.exists() or solution.read_text(encoding="utf-8") != code:
        solution.write_text(code, encoding="utf-8")
    touched.append(solution)

    record_submission(record, sub, detail)
    touched.append(record)

    runtime = detail.get("runtimeDisplay") or "?"
    memory = detail.get("memoryDisplay") or "?"
    message = (f"Time: {runtime} ({detail.get('runtimePercentile') or 0:.2f}%) | "
               f"Memory: {memory} ({detail.get('memoryPercentile') or 0:.2f}%) - "
               f"{question['title']}")
    wrote = commit(repo, touched, message, int(sub["timestamp"]))
    return ("committed" if wrote else "unchanged"), target


def run_once(repo, args, session, csrf, username):
    patterns = topics.load_patterns(repo)
    tags = topics.load_tags(repo)
    cache = {}

    if args.backfill:
        subs = backfill_accepted(session, csrf, args.backfill)
        print(f"  {len(subs)} accepted submissions in history")
    else:
        subs = recent_accepted(session, csrf, username, args.limit)

    if args.since:
        cutoff = datetime.strptime(args.since, "%Y-%m-%d").replace(
            tzinfo=timezone.utc).timestamp()
        subs = [s for s in subs if int(s["timestamp"]) >= cutoff]

    # Oldest first, so a problem solved twice commits in chronological order.
    subs.sort(key=lambda s: int(s["timestamp"]))

    counts = {}
    for sub in subs:
        try:
            status, target = pull_one(repo, sub, session, csrf, cache, patterns,
                                      tags, args.dry_run, args.refresh_readme)
        except LeetCodeError as err:
            print(f"  !! {sub['titleSlug']}: {err}", file=sys.stderr)
            counts["failed"] = counts.get("failed", 0) + 1
            continue
        counts[status] = counts.get(status, 0) + 1
        if status != "known":
            rel = Path(target).relative_to(repo)
            when = datetime.fromtimestamp(int(sub["timestamp"]), timezone.utc).date()
            print(f"  {status:12} {rel}  ({when})")

    summary = ", ".join(f"{v} {k}" for k, v in sorted(counts.items())) or "nothing new"
    print(f"  -> {summary}")
    return counts


def main():
    parser = argparse.ArgumentParser(
        description="Pull accepted LeetCode submissions into this repo and commit them.")
    parser.add_argument("--repo", default=".", help="the solutions repo (default: .)")
    parser.add_argument("--limit", type=int, default=20,
                        help="how many recent accepted submissions to ask for")
    parser.add_argument("--backfill", type=int, metavar="N",
                        help="walk N submissions back through full history instead")
    parser.add_argument("--since", metavar="YYYY-MM-DD", help="ignore anything older")
    parser.add_argument("--watch", type=int, metavar="SECONDS",
                        help="keep polling every SECONDS until interrupted")
    parser.add_argument("--dry-run", action="store_true",
                        help="report what would happen; write and commit nothing")
    parser.add_argument("--refresh-readme", action="store_true",
                        help="rewrite README.md even when it already exists")
    parser.add_argument("--push", action="store_true", help="git push after committing")
    parser.add_argument("--sync", action="store_true",
                        help="run leetcode_sync.py afterwards to refresh LEETCODE.md")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    try:
        session, csrf = load_credentials(repo)
        username = whoami(session, csrf)
    except LeetCodeError as err:
        print(f"error: {err}", file=sys.stderr)
        return 2

    print(f"signed in as {username}")
    if args.dry_run:
        print("(--dry-run: nothing will be written or committed)")

    while True:
        stamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{stamp}] checking...")
        try:
            counts = run_once(repo, args, session, csrf, username)
        except LeetCodeError as err:
            print(f"error: {err}", file=sys.stderr)
            if not args.watch:
                return 2
            counts = {}

        if counts.get("committed") and args.push and not args.dry_run:
            pushed = git(repo, "push")
            print("  pushed" if pushed.returncode == 0
                  else f"  push failed: {pushed.stderr.strip()}")
        if counts.get("committed") and args.sync and not args.dry_run:
            subprocess.run([sys.executable, "leetcode_sync.py"], cwd=str(repo))

        if not args.watch:
            return 0
        try:
            time.sleep(args.watch)
        except KeyboardInterrupt:
            print("\nstopped")
            return 0


if __name__ == "__main__":
    raise SystemExit(main())

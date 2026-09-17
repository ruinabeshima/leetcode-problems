from collections import Counter, defaultdict


r"""
SLIDING WINDOW

The brute force for "find the best subarray/substring" tries every start
against every end: O(n^2). A sliding window keeps two pointers, left and
right, and moves each one FORWARD ONLY. Every element enters the window
once and leaves once, so the whole thing is O(n) even though there is a
nested while loop.

Key point: forward-only is the entire reason it is fast. If you ever find
yourself needing to move `left` backwards, this is not a sliding window
problem.

Two blocks:
  1. Fixed size    -- the window is always exactly k wide
  2. Variable size -- right always advances, left catches up when it must

WHEN IT DOES NOT WORK

The condition has to be monotonic: shrinking from the left must move you
TOWARD validity. "Subarray sum >= target" qualifies only while the
numbers are positive, because dropping an element always lowers the sum.
Allow negatives and shrinking can RAISE the sum, left would need to go
backwards, and you need prefix sums plus a hash map instead.

So read the constraints. Negative numbers on a subarray-sum problem mean
it is not a sliding window.
"""


r"""
1. FIXED SIZE -- the window never changes width

Adding one element means removing one, so there is no `left` pointer to
track: it is always right - k.
"""
def max_sum_k(nums, k):
    window = sum(nums[:k])          # build the first window outright
    best = window

    for right in range(k, len(nums)):
        window += nums[right] - nums[right - k]      # add the new, drop the old
        best = max(best, window)

    return best


r"""
FIND ALL ANAGRAMS -- fixed window plus a counter

Every start index in s where a permutation of p begins.

Key point: two Counters compare equal when they hold the same characters
with the same multiplicities, so `window == need` IS the anagram test.
That is also why zero entries must be deleted -- {a:1, b:0} and {a:1} are
not equal, and a stale zero would break every later comparison.
"""
def find_anagrams(s, p):
    need = Counter(p)
    window = Counter()
    out = []

    for right in range(len(s)):
        window[s[right]] += 1

        if right >= len(p):                 # too wide now: drop the leftmost
            left = right - len(p)
            window[s[left]] -= 1
            if window[s[left]] == 0:
                del window[s[left]]         # keep the Counter comparable

        if window == need:
            out.append(right - len(p) + 1)

    return out


r"""
2. VARIABLE SIZE -- the block that matters

    left = 0
    for right in range(len(s)):
        <add s[right] to the window state>

        while <condition>:
            <remove s[left] from the window state>
            left += 1

        <record the answer>

Everything below is that shape. Only two things ever change: what goes in
the while, and WHERE you record.

    LONGEST  -- shrink while the window is INVALID, record AFTER the while
                (the while exits having restored validity, so measure then)

    SHORTEST -- shrink while the window is VALID, record INSIDE the while
                (measure before you destroy the valid window)

Key point: putting the record in the wrong place is the number one
sliding window bug, and it produces plausible off-by-one answers rather
than a crash.
"""


r"""
LONGEST SUBSTRING WITHOUT REPEATING CHARACTERS

The cleanest instance of the LONGEST flavour, and the one to learn first.

The window is invalid exactly when the character just added appears
twice -- no other character can have become a duplicate, since the window
was valid a moment ago.
"""
def longest_unique_substring(s):
    count = defaultdict(int)
    left = 0
    best = 0

    for right in range(len(s)):
        count[s[right]] += 1

        while count[s[right]] > 1:          # INVALID: the new char duplicates
            count[s[left]] -= 1
            left += 1

        best = max(best, right - left + 1)  # AFTER the while: valid again

    return best


r"""
MAX CONSECUTIVE ONES III

Longest run of 1s if you may flip at most k zeros.

Key point: do not think about which zeros to flip. The window is valid
whenever it contains at most k zeros, so all you track is a count.
"""
def max_consecutive_ones(nums, k):
    left = 0
    zeros = 0
    best = 0

    for right in range(len(nums)):
        if nums[right] == 0:
            zeros += 1

        while zeros > k:                    # INVALID: more flips than allowed
            if nums[left] == 0:
                zeros -= 1
            left += 1

        best = max(best, right - left + 1)

    return best


r"""
LONGEST REPEATING CHARACTER REPLACEMENT

Longest substring that can become all one letter using at most k changes.

The window is valid when (width - count of the most common letter) <= k,
i.e. everything that is not the majority letter can be replaced.

Key point: max_freq is never decreased, which looks like a bug and is
not. A stale-high max_freq can only make the window look MORE valid, so
the window never shrinks when it should have -- but `best` only grows
when a genuinely larger max_freq appears. The answer stays correct and
you save re-scanning the counter on every shrink.
"""
def character_replacement(s, k):
    count = defaultdict(int)
    left = 0
    max_freq = 0
    best = 0

    for right in range(len(s)):
        count[s[right]] += 1
        max_freq = max(max_freq, count[s[right]])

        while (right - left + 1) - max_freq > k:    # INVALID: too many to replace
            count[s[left]] -= 1
            left += 1

        best = max(best, right - left + 1)

    return best


r"""
MINIMUM SIZE SUBARRAY SUM -- the SHORTEST flavour

Shortest subarray whose sum is at least target. Returns 0 if none exists.

Note where the recording moved: INSIDE the while. The window is valid at
that moment, so you measure it before shrinking it away.

Requires positive numbers -- see the monotonicity note at the top.
"""
def min_subarray_len(nums, target):
    left = 0
    total = 0
    best = float('inf')

    for right in range(len(nums)):
        total += nums[right]

        while total >= target:              # VALID: record, then try smaller
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1

    return best if best != float('inf') else 0


r"""
MINIMUM WINDOW SUBSTRING -- the hard one, same template

Shortest window of s containing every character of t, multiplicities
included. Returns "" if there is none.

Key point: `missing` counts characters still unmatched, WITH
multiplicity, so the validity test is a single integer comparison rather
than a per-character scan of the counter.

The need[c] > 0 guard is what makes that work. Counts go negative for
surplus copies, and only a need that was still positive represents a
character that genuinely had to be found.
"""
def min_window(s, t):
    if not t or len(t) > len(s):
        return ""

    need = Counter(t)
    missing = len(t)                        # unmatched chars, with multiplicity
    left = 0
    best = (float('inf'), 0, 0)             # (width, start, end)

    for right in range(len(s)):
        if need[s[right]] > 0:              # this one was genuinely still needed
            missing -= 1
        need[s[right]] -= 1                 # surplus copies go negative

        while missing == 0:                 # VALID: record, then shrink
            if right - left + 1 < best[0]:
                best = (right - left + 1, left, right)

            need[s[left]] += 1
            if need[s[left]] > 0:           # back above zero = we now need it again
                missing += 1
            left += 1

    return "" if best[0] == float('inf') else s[best[1]:best[2] + 1]


r"""
ADJACENT TECHNIQUE: TWO POINTERS FROM OPPOSITE ENDS

Grouped with sliding window on most problem lists, but a different
motion: the pointers start at the two ends and move TOWARD each other.
The array is usually sorted, or sortedness is irrelevant and the geometry
does the work.

Key point: the skill is knowing which pointer to move. There is always an
argument that moving the other one cannot possibly help.
"""
def two_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1

    while left < right:
        total = nums[left] + nums[right]

        if total == target:
            return [left, right]
        if total < target:
            left += 1               # only a bigger left can raise the sum
        else:
            right -= 1              # only a smaller right can lower it

    return []


def max_area(heights):
    left, right = 0, len(heights) - 1
    best = 0

    while left < right:
        width = right - left
        best = max(best, width * min(heights[left], heights[right]))

        # Move the SHORTER wall. Width only ever shrinks, and the short
        # wall caps the height, so keeping it can never beat what we just
        # measured -- there is nothing to gain from moving the taller one.
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1

    return best

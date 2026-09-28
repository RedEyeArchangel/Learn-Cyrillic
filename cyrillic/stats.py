# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# Copyright (c) 2026 RedEyeArchangel
"""Learning data: history, confusions, error proneness and study plan."""
from collections import Counter

from cyrillic.i18n import LANG, _
from cyrillic.questions import CARDS


# History + confusions per letter (uppercase letter as key)
HIST_MAX = 200
PLAN_UNLOCK = 3  # how often Easy must have been fully learned
SOUND_KEY = {c.answer: c.key for c in CARDS["Easy"]}


def record_letter(stats, right, chosen):
    h = stats["hist"].setdefault(right, [])
    h.append(int(right == chosen))
    del h[:-HIST_MAX]
    if right != chosen:
        c = stats["conf"].setdefault(right, {})
        c[chosen] = c.get(chosen, 0) + 1


def partners(stats, k):
    """Letters confused with k (both directions), most frequent first."""
    cnt = Counter(stats["conf"].get(k, {}))
    for o, c in stats["conf"].items():
        cnt[o] += c.get(k, 0)
    return [x for x, n in cnt.most_common() if n and x != k]


# Components of error proneness (name, weight per event). A wrongly pressed letter counts double
# (like a mistake + a confusion for the letter that was asked). Every right answer in the current run
# lowers the score; a mistake ends the run, and after RELAPSE right in a row it counts as "forgot again".
# ponytail: counts never age; count only the last N events if that becomes a problem
PARTS = [(_("Error rate (last 10)"), None), (_("Confused"), .1), (_("Wrongly pressed"), .2), (_("Looked up"), .1),
         (_("Forgot again"), .3), (_("Right in a row"), -.1)]
RELAPSE = 4


def run(h):
    """Right answers in a row at the end of the history."""
    return h[::-1].index(0) if 0 in h else len(h)


def weakness_parts(stats):
    """letter -> [error rate, confused, wrongly pressed, looked up, forgot again, right in a row], weighted."""
    parts = {}

    def add(k, i, v):
        parts.setdefault(k, [0.0] * len(PARTS))[i] += v
    for k, h in stats["hist"].items():
        if h:
            add(k, 0, h[-10:].count(0) / len(h[-10:]))
            add(k, 4, PARTS[4][1] * sum(not h[i] and all(h[i - RELAPSE:i]) for i in range(RELAPSE, len(h))))
            add(k, 5, PARTS[5][1] * run(h))
    for k, c in stats["conf"].items():
        for o, n in c.items():
            add(k, 1, n * PARTS[1][1])
            add(o, 2, n * PARTS[2][1])
    for k, n in stats["lookup"].items():
        add(k, 3, n * PARTS[3][1])
    return parts


def weakness(stats):
    return Counter({k: sum(v) for k, v in weakness_parts(stats).items()})


def explain(k, v):
    """Breakdown of a weakness score as text."""
    txt = [_("error rate {:.0%} ({:.2f})").format(v[0], v[0])]
    case = str if LANG == "de" else str.lower  # German nouns stay capitalized
    txt += [f"{round(x / w)}× {case(name)} ({x:.2f})" for (name, w), x in zip(PARTS[1:], v[1:])]
    return f"{k}:  " + "  +  ".join(txt) + f"  =  {sum(v):.2f}"


def make_plan(stats, n=8):
    """Weakest letters, each with its two most frequent mix-ups."""
    plan = []
    for k, score in weakness(stats).most_common():
        if score <= 0 or len(plan) >= n:
            break
        plan += [x for x in [k] + partners(stats, k)[:2] if x not in plan]
    return plan


def plan_cards(plan, lv):
    """Easy: only plan letters; words/sentences: those containing a plan letter."""
    low = {k.lower() for k in plan}
    sel = [c for c in CARDS[lv] if (c.key in plan if lv == "Easy" else low & set(c.key.lower()))]
    return sel or CARDS[lv]


def moving(h, k=5):
    return [sum(h[max(0, i - k + 1):i + 1]) / len(h[max(0, i - k + 1):i + 1]) for i in range(len(h))]

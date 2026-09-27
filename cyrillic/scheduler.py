# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# Copyright (c) 2026 RedEyeArchangel
"""Learning algorithm like driving-school theory apps: streak, status, next card."""
import random


# Every card has to be answered correctly MASTER times in a row -> "learned" (green).
# A mistake resets the streak to 0 (red). New cards are added by difficulty,
# at most BATCH in progress at the same time. Learned cards come back now and then for review.
MASTER = 3
BATCH = 5
REVIEW_CHANCE = 0.15
EXAM_QUESTIONS, EXAM_MAX_WRONG = 20, 2
WEIGHT = {"red": 3, "yellow": 2, "new": 2, "green": 1}


def status(p):
    if not p:
        return "new"
    if p["streak"] >= MASTER:
        return "green"
    return "red" if p["streak"] == 0 else "yellow"


def record(progress, key, correct):
    p = progress.setdefault(key, {"streak": 0, "wrong": 0})
    p["streak"] = p["streak"] + 1 if correct else 0
    p["wrong"] += not correct


def pick(progress, cards, last=None, rng=random):
    st = {c.key: status(progress.get(c.key)) for c in cards}
    active = [c for c in cards if st[c.key] in ("red", "yellow")]
    new = [c for c in sorted(cards, key=lambda c: c.group) if st[c.key] == "new"]
    pool = active + new[:max(0, BATCH - len(active))]
    if not pool or rng.random() < REVIEW_CHANCE:
        pool += [c for c in cards if st[c.key] == "green"]
    pool = [c for c in pool if c.key != last] or pool
    return rng.choices(pool, [WEIGHT[st[c.key]] for c in pool])[0]


def learned(progress, cards):
    return sum(status(progress.get(c.key)) == "green" for c in cards)

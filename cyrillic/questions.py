# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# Copyright (c) 2026 RedEyeArchangel
"""Transliteration, flash cards per level and quiz questions with distractors."""
import random
import re
from collections import namedtuple

from cyrillic.data import CYR_SWAP, LETTERS, MISREAD, SENTENCES, SIMILAR, SOUND, TR, VOWELS, WORDS


def translit(text, rng=None, p=0.0):
    """Transliterate; with rng/p every confusable letter is misread with probability p."""
    out, prev = [], " "
    for ch in text:
        low = ch.lower()
        t = TR.get(low, ch)
        if low == "е" and (prev in VOWELS or not prev.isalpha()):
            t = "ye"
        if rng and low in MISREAD and rng.random() < p:
            t = MISREAD[low]
        out.append(t.capitalize() if ch.isupper() else t)
        prev = low
    return "".join(out)


Card = namedtuple("Card", "key show say answer info group word meaning")
LETTER_GROUP = {l[1]: l[6] for l in LETTERS}


def text_card(ru, meaning):
    # difficulty = hardest letter group in the text -> easy words come first
    return Card(ru, ru, ru, translit(ru), meaning, max(LETTER_GROUP.get(c, 1) for c in ru.lower()), ru, meaning)


CARDS = {
    "Easy": [Card(l[0], f"{l[0]} {l[1]}", l[2], SOUND[l[0]], l[3], l[6], l[4], l[5])
             for l in LETTERS],
    "Medium": [text_card(*w) for w in WORDS],
    "Hard": [text_card(*s) for s in SENTENCES],
}
LEVEL_TXT = {"Easy": "Letters", "Medium": "Words", "Hard": "Sentences"}

# Question types per level: (type, question). Listening only from Medium on.
QTYPES = {
    "Easy": [("sound", "Which sound?"), ("letter", "Which letter makes this sound?")],
    "Medium": [("read", "How do you read this?"), ("write", "How do you write this?"),
               ("meaning", "What does this mean?"), ("reverse", "How do you say this in Russian?"),
               ("spell", "Which letter is missing?"), ("listen", "What do you hear?")],
    "Hard": [("read", "How do you read this?"), ("write", "How do you write this?"),
             ("meaning", "What does this mean?"), ("reverse", "How do you say this in Russian?"),
             ("wordgap", "Which word is missing?"), ("listen", "What do you hear?")],
}
RU_WORD = r"[А-Яа-яЁё-]+"
SENT_WORDS = sorted({t.lower() for s, _ in SENTENCES for t in re.findall(RU_WORD, s)})
ALPHABET = "".join(l[1] for l in LETTERS)


def similar(ch):
    """Lowercase letters that get confused with ch (without ch itself)."""
    return {x.lower() for g in SIMILAR if ch.upper() in g for x in g} - {ch.lower()}


def misspell(text, rng, p):
    return "".join((CYR_SWAP[ch.lower()].upper() if ch.isupper() else CYR_SWAP[ch.lower()])
                   if ch.lower() in CYR_SWAP and rng.random() < p else ch for ch in text)


def question(card, level, qtype, rng=random, n=4, confused=()):
    """-> (prompt, options, right answer). confused: your own mix-ups come first as distractors."""
    others = rng.sample(CARDS[level], len(CARDS[level]))
    if level == "Easy":
        pool = ([c for c in others if c.key in confused] +
                [c for c in others if c.show[-1] in similar(card.key)] + others)
        if qtype == "sound":
            prompt, right, cand = card.show, card.answer, [c.answer for c in pool]
        else:  # letter
            prompt, right, cand = card.answer, card.show, [c.show for c in pool]
    else:
        typos = [misspell(card.key, rng, p) for p in (.5, .4, .4, .3, .3, .2)]
        if qtype == "read":
            prompt, right = card.show, card.answer
            cand = [translit(card.key, rng, p) for p in (1, .5, .5, .4, .4, .3)] + [c.answer for c in others]
        elif qtype == "write":
            prompt, right, cand = card.answer, card.show, typos + [c.show for c in others]
        elif qtype == "meaning":
            prompt, right, cand = card.show, card.meaning, [c.meaning for c in others]
        elif qtype == "reverse":
            prompt, right, cand = card.meaning, card.show, typos[:1] + [c.show for c in others]
        elif qtype == "spell":
            i = rng.choice([i for i, ch in enumerate(card.key) if ch.isalpha()])
            right = card.key[i].lower()
            prompt = f"{card.key[:i]}_{card.key[i + 1:]}\n({card.meaning})"
            cand = sorted(similar(right)) + [CYR_SWAP.get(right, "")] + rng.sample(ALPHABET, len(ALPHABET))
            cand = [c for c in cand if c]
        elif qtype == "wordgap":
            w = rng.choice(re.findall(RU_WORD, card.key))
            gapped = re.sub(rf"(?<![А-Яа-яЁё-]){re.escape(w)}(?![А-Яа-яЁё-])", "___", card.key, count=1)
            prompt, right = f"{gapped}\n({card.meaning})", w.lower()
            words = rng.sample(SENT_WORDS, len(SENT_WORDS))
            cand = [misspell(right, rng, .5)] + sorted(words, key=lambda x: abs(len(x) - len(right)))
        else:  # listen
            prompt, right, cand = "?", card.show, typos + [c.show for c in others]
    opts = list(dict.fromkeys(x for x in cand if x != right))[:n - 1] + [right]
    rng.shuffle(opts)
    return prompt, opts, right

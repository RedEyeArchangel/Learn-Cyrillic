# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# Copyright (c) 2026 RedEyeArchangel
"""Transliteration, flash cards per level and quiz questions with distractors."""
import random
import re
from collections import namedtuple

from cyrillic.data import (COGNATES, CYR_SWAP, EXAMPLES, LETTERS, MISREAD, SENTENCES, SIMILAR, SOUND, TR, VOWELS,
                           WORDS)
from cyrillic.i18n import _


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
    # difficulty = hardest letter group in the text -> easy words come first; cognates before everything else
    group = max(LETTER_GROUP.get(c, 1) for c in ru.lower()) - 10 * (ru in COGNATES)
    return Card(ru, ru, ru, translit(ru), meaning, group, ru, meaning)


CARDS = {
    "Easy": [Card(l[0], f"{l[0]} {l[1]}", l[2], SOUND[l[0]], l[3], l[6], l[4], l[5])
             for l in LETTERS],
    "Medium": [text_card(*w) for w in WORDS],
    "Hard": [text_card(*s) for s in SENTENCES],
}
LEVEL_TXT = {"Easy": _("Letters"), "Medium": _("Words"), "Hard": _("Sentences")}

# Question types per level: (type, question). Listening only from Medium on.
QTYPES = {
    "Easy": [("sound", _("Which sound?")), ("letter", _("Which letter makes this sound?"))],
    "Medium": [("read", _("How do you read this?")), ("write", _("How do you write this?")),
               ("meaning", _("What does this mean?")), ("reverse", _("How do you say this in Russian?")),
               ("spell", _("Which letter is missing?")), ("hearmeaning", _("What does the word you hear mean?")),
               ("listen", _("What do you hear?"))],
    "Hard": [("read", _("How do you read this?")), ("write", _("How do you write this?")),
             ("meaning", _("What does this mean?")), ("reverse", _("How do you say this in Russian?")),
             ("wordgap", _("Which word is missing?")), ("listen", _("What do you hear?"))],
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
        elif qtype == "hearmeaning":
            prompt, right, cand = "?", card.meaning, [c.meaning for c in others]
        else:  # listen
            prompt, right, cand = "?", card.show, typos + [c.show for c in others]
    opts = list(dict.fromkeys(x for x in cand if x != right))[:n - 1] + [right]
    rng.shuffle(opts)
    return prompt, opts, right


# --- hint (free practice): how a card is written and why ---
LETTER = {l[1]: l for l in LETTERS}
NOTES = {
    "е": _("е: at the start of a word or after a vowel “ye”, after a consonant “e” and it softens the consonant"),
    "ё": _("ё: “yo”, always stressed – the two dots are often left out in normal texts"),
    "й": _("й: short “y”, glides after a vowel (like the y in “boy”)"),
    "ь": _("ь (soft sign): no sound of its own, softens the consonant before it"),
    "ъ": _("ъ (hard sign): no sound of its own, separates the consonant from the next vowel"),
    "ы": _("ы: dull i, tongue pulled back – not the same as и"),
}


def letter_notes(letters, n=6):
    """Why-notes for the special letters, at most n: rules (signs, е/ё/й/ы) first, then false friends, then new
    sounds; each group in order of first appearance."""
    notes = []
    for ch in dict.fromkeys(letters):
        if ch in NOTES:
            notes.append((0, NOTES[ch]))
        elif ch in LETTER and LETTER[ch][6] == 2 and ch in MISREAD:  # false friend
            notes.append((1, _("{}: looks like Latin “{}”, but is “{}”").format(ch, MISREAD[ch], TR[ch])))
        elif ch in LETTER and LETTER[ch][6] == 4:  # new sound
            notes.append((2, f"{ch}: {SOUND[ch.upper()]}"))
    return [t for _p, t in sorted(notes, key=lambda x: x[0])][:n]


def hint(card, level):
    """Explanation for a card: word, transliteration, letter by letter (or word by word) and the rules behind it."""
    if level == "Easy":
        up, low, name, pron, ex, tr, _g = LETTER[card.key.lower()]
        lines = [f"{up} {low}  ·  " + _("name “{}”").format(name) + f"  ·  {pron}",
                 _("Example: {} = {} ({})").format(ex, translit(ex), tr)]
        return "\n".join(lines + letter_notes(low))
    text = card.key
    lines = [f"{card.show}  =  {card.answer}  ·  {card.meaning}"]
    if level == "Medium":  # letter by letter, e.g. д = d · о = o · м = m
        parts = [translit(text[:i + 1])[len(translit(text[:i])):] or "–" for i in range(len(text))]
        lines.append("  ·  ".join(f"{ch} = {t}" for ch, t in zip(text, parts) if ch.isalpha()))
        if text in EXAMPLES:
            lines.append(_("Example: {} – {}").format(*EXAMPLES[text]))
        if text in COGNATES:
            lines.append(_("Cognate: once you can read it, you know what it means"))
    else:  # word by word
        lines.append("  ·  ".join(f"{w} = {translit(w)}" for w in re.findall(RU_WORD, text)))
    # at most 6 lines in total, so the answer buttons stay visible
    return "\n".join(lines + letter_notes((c for c in text.lower() if c.isalpha()), 6 - len(lines)))

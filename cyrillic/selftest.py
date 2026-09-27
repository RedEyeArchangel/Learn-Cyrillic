# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# Copyright (c) 2026 RedEyeArchangel
"""Self-test: python learn_cyrillic.py --test"""
import json
import os
import random
import tempfile
import wave

from cyrillic.data import GROUPS, LETTERS, SOUND
from cyrillic.gui.theme import STYLES
from cyrillic.questions import CARDS, QTYPES, question, translit
from cyrillic.scheduler import BATCH, MASTER, learned, pick, record, status
from cyrillic.sound import fanfare
from cyrillic.stats import (HIST_MAX, SOUND_KEY, explain, make_plan, moving, partners, plan_cards, record_letter,
                            weakness, weakness_parts)
from cyrillic.storage import normalize


def selftest():
    assert len(LETTERS) == 33
    assert len({l[0] for l in LETTERS}) == 33
    assert len({l[3] for l in LETTERS}) == 33, "pronunciation hints must be unique (quiz)"
    assert {l[6] for l in LETTERS} == set(GROUPS)
    # transliteration
    assert translit("Это мой дом.") == "Eto moy dom."
    assert translit("объект") == "obyekt" and translit("Ёлка") == "Yolka" and translit("ель") == "yel"
    assert translit("Доброе утро!") == "Dobroye utro!" and translit("щука") == "shchuka"
    assert translit("рот", random.Random(0), 1) == "pot", "misreading: р -> p"
    # questions: always 4 different answers, exactly one right, no example word in the answers
    assert len({c.answer for c in CARDS["Easy"]}) == 33, "sounds must be unique"
    assert set(SOUND) == {l[0] for l in LETTERS} and all(" as in " not in c.answer for c in CARDS["Easy"])
    assert set(dict(QTYPES["Easy"])) == {"sound", "letter"}, "Easy: only alphabet + sounds"
    assert "___" in question(CARDS["Hard"][7], "Hard", "wordgap", random.Random(5))[0]
    rng = random.Random(1)
    for lv, cards in CARDS.items():
        assert len({c.key for c in cards}) == len(cards), f"duplicate card in {lv}"
        for c in cards * 3:
            for qtype, _ in QTYPES[lv]:
                prompt, opts, right = question(c, lv, qtype, rng)
                assert len(opts) == 4 and len(set(opts)) == 4 and opts.count(right) == 1, (lv, qtype, c.key)
    _, opts, _ = question(CARDS["Easy"][24], "Easy", "letter", rng)  # Ч
    assert set(opts) <= {"Ш ш", "Щ щ", "Ч ч", "Ц ц", "Ж ж"}, "similar letters as distractors"
    # learning algorithm
    letters, prog = CARDS["Easy"], {}
    assert pick(prog, letters, rng=rng).group == 1, "new letters come group by group, group 1 first"
    assert pick({}, CARDS["Medium"], rng=rng).group == 1, "easy words first"
    record(prog, "А", True)
    assert status(prog["А"]) == "yellow"
    for _ in range(MASTER - 1):
        record(prog, "А", True)
    assert status(prog["А"]) == "green"
    record(prog, "А", False)
    assert status(prog["А"]) == "red" and prog["А"]["wrong"] == 1
    busy = {c.key: {"streak": 0, "wrong": 1} for c in letters[:BATCH]}
    for _ in range(200):  # BATCH in progress -> no new cards
        assert pick(busy, letters, rng=rng).key in busy
    assert pick(prog, letters, last="А", rng=rng).key != "А"
    full = {c.key: {"streak": MASTER, "wrong": 0} for c in letters}
    assert status(full[pick(full, letters, rng=rng).key]) == "green", "everything learned -> review"
    assert learned(full, letters) == 33 and learned({}, letters) == 0
    # learning data + study plan
    st = {"hist": {}, "conf": {}, "done": 0, "plan": [], "lookup": {}}
    assert make_plan(st) == []
    st["lookup"]["Ю"] = 2
    assert make_plan(st) == ["Ю"], "looking up alone -> letter goes into the plan"
    st["lookup"].clear()
    for _ in range(3):
        record_letter(st, "Ш", "Щ")
    record_letter(st, "А", "А")
    record_letter(st, "Ы", "И")
    assert st["hist"]["Ш"] == [0, 0, 0] and st["conf"]["Ш"] == {"Щ": 3} and st["hist"]["А"] == [1]
    assert partners(st, "Щ") == ["Ш"]
    assert round(weakness(st)["Щ"], 6) == .6, "wrongly pressed letter is weighted"
    assert [round(x, 6) for x in weakness_parts(st)["Ш"]] == [1, .3, 0, 0]
    assert explain("Щ", weakness_parts(st)["Щ"]) == ("Щ:  error rate 0% (0.00)  +  0× confused (0.00)  +  "
                                                  "3× wrongly pressed (0.60)  +  0× looked up (0.00)  =  0.60")
    plan = make_plan(st)
    assert plan[:2] == ["Ш", "Щ"] and "Ы" in plan and "И" in plan and "А" not in plan, plan
    assert {c.key for c in plan_cards(plan, "Easy")} == set(plan)
    assert all(set(c.key.lower()) & set("шщыи") for c in plan_cards(plan, "Medium"))
    assert plan_cards(["Ъ"], "Hard") == CARDS["Hard"], "no match -> all cards"
    ch = next(c for c in CARDS["Easy"] if c.key == "Ш")
    assert "Щ щ" in question(ch, "Easy", "letter", rng, confused=["Щ"])[1]
    for _ in range(HIST_MAX + 5):
        record_letter(st, "А", "А")
    assert len(st["hist"]["А"]) == HIST_MAX
    assert moving([0, 1, 1]) == [0, .5, 2 / 3]
    assert SOUND_KEY[SOUND["Ш"]] == "Ш"
    # export/import: round trip, old formats are migrated, broken files are rejected
    full = normalize({"Easy": {"А": {"streak": 3, "wrong": 1}}, "stats": st})
    assert normalize(json.loads(json.dumps(full, ensure_ascii=False))) == full
    assert normalize({"А": {"streak": 1, "wrong": 0}})["Easy"]["А"]["streak"] == 1, "oldest format"
    old = normalize({"Leicht": {"А": {"streak": 2, "wrong": 0}}, "Schwer": {}, "stats": {"done": 2}})
    assert old["Easy"]["А"]["streak"] == 2 and "Leicht" not in old and old["stats"]["done"] == 2, "German levels"
    for bad in ([], {"Easy": {"А": 5}}, {"Easy": {}, "stats": {"done": "x"}},
                {"Easy": {}, "stats": {"hist": {"А": ["a"]}}}, {"foo": 1}, {"Easy": {}, "stats": 3},
                {"Easy": {}, "stats": {"plan": [1]}}, {"Leicht": {"А": 5}}):
        try:
            normalize(bad)
            raise AssertionError(bad)
        except ValueError:
            pass
    assert len(set(STYLES)) >= len(LETTERS), "enough curve styles for all letters"
    wav = fanfare(tempfile.mktemp(suffix=".wav"))
    with wave.open(wav) as w:
        assert 1 < w.getnframes() / w.getframerate() < 3, "fanfare ~1.6 s"
    os.remove(wav)
    print("ok")

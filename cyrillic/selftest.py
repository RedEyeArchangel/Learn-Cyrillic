# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# Copyright (c) 2026 RedEyeArchangel
"""Self-test: python learn_cyrillic.py --test"""
import ast
import json
import os
import random
import re
import tempfile
import wave
from pathlib import Path

from cyrillic.data import GROUPS, LETTERS, SENTENCES, SOUND, WORDS
from cyrillic.gui.theme import STYLES
from cyrillic.i18n import DE
from cyrillic.questions import CARDS, QTYPES, question, translit
from cyrillic.scheduler import (BATCH, KEEP_AFTER, MASTER, complete_level, learned, pick, record,
                                status)
from cyrillic.sound import fanfare
from cyrillic.stats import (HIST_MAX, SOUND_KEY, explain, make_plan, moving, partners, plan_cards, record_letter, run,
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
    rounds = {"Easy": 0}
    for i in range(1, KEEP_AFTER + 1):  # completed: counted, starts from zero until the last round
        prog = {c.key: {"streak": MASTER, "wrong": 0} for c in letters}
        assert complete_level(prog, rounds, "Easy", letters) and rounds["Easy"] == i
        assert (prog == {}) == (i < KEEP_AFTER)
    assert learned(prog, letters) == 33, "after the last round the level stays learned"
    assert not complete_level(prog, rounds, "Easy", letters) and rounds["Easy"] == KEEP_AFTER, "no more counting"
    assert not complete_level({}, {"Easy": 0}, "Easy", letters), "not full -> nothing happens"
    # learning data + study plan
    st = {"hist": {}, "conf": {}, "rounds": {}, "plan": [], "lookup": {}}
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
    assert round(weakness(st)["Щ"], 6) == .3, "wrongly pressed letter is weighted"
    assert [round(x, 6) for x in weakness_parts(st)["Ш"]] == [1, .3, 0, 0, 0, 0]
    assert explain("Щ", weakness_parts(st)["Щ"]) == ("Щ:  error rate 0% (0.00)  +  0× confused (0.00)  +  "
                                                  "3× wrongly pressed (0.30)  +  0× looked up (0.00)  +  "
                                                  "0× forgot again (0.00)  +  0× right answers (0.00)  =  0.30")
    plan = make_plan(st)
    assert plan == ["Ш", "Ы", "Щ", "И"], plan  # by score: 1.3, 1.1, 0.3, 0.1
    # right answers lower the score, a mistake halves that bonus; a mistake after RELAPSE right = "forgot again"
    h = {"hist": {"Ж": [0, 1, 1, 1, 1, 0, 1, 1]}, "conf": {}, "lookup": {}}
    assert run([1, 0, 1, 1]) == 2 and run([1, 1]) == 2 and run([0]) == 0 and run([1] * 10 + [0]) == 5
    assert [round(x, 6) for x in weakness_parts(h)["Ж"]] == [.25, 0, 0, 0, .2, -.4]
    h["hist"]["Ж"] += [1] * 5
    assert make_plan(h) == [], "enough right answers in a row -> out of the plan"
    mix = {"hist": {"Л": [0], "П": [0] + [1] * 10}, "conf": {"Л": {"П": 1}}, "lookup": {}}
    assert make_plan(mix) == ["Л"], "a learned mix-up partner (score <= 0) stays out of the plan"
    mix["hist"]["П"].append(0)
    assert make_plan(mix) == ["Л"], "one slip after 10 right answers is not enough to come back"
    mix["hist"]["П"].append(0)
    assert set(make_plan(mix)) == {"Л", "П"}, "a second mistake brings it back"
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
    assert old["Easy"]["А"]["streak"] == 2 and "Leicht" not in old and old["stats"]["rounds"]["Easy"] == 2, "German levels"
    assert normalize({"stats": {"done": 3}})["stats"]["rounds"] == {"Easy": 3, "Medium": 0, "Hard": 0}, \
        "old Easy counter"
    for bad in ([], {"Easy": {"А": 5}}, {"Easy": {}, "stats": {"done": "x"}},
                {"Easy": {}, "stats": {"hist": {"А": ["a"]}}}, {"foo": 1}, {"Easy": {}, "stats": 3},
                {"Easy": {}, "stats": {"plan": [1]}}, {"Leicht": {"А": 5}}, {"stats": {"rounds": {"Easy": "x"}}}):
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
    # German: every _("...") in the code is translated, placeholders match, quiz answers stay unique
    used = {n.args[0].value for f in Path(__file__).parent.rglob("*.py") for n in ast.walk(ast.parse(f.read_text()))
            if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "_" and n.args
            and isinstance(n.args[0], ast.Constant)}
    assert used <= set(DE), used - set(DE)
    content = [l[3] for l in LETTERS] + [l[5] for l in LETTERS] + list(SOUND.values()) + list(GROUPS.values())
    content += [m for _, m in WORDS + SENTENCES]
    assert not [t for t in content if t not in DE and len(t) > 2], "content without German text"
    assert all(re.findall(r"{[^}]*}", k) == re.findall(r"{[^}]*}", v) for k, v in DE.items()), "placeholders"
    for texts in ([l[3] for l in LETTERS], SOUND.values(), [m for _, m in WORDS], [m for _, m in SENTENCES]):
        assert len({DE.get(t, t) for t in texts}) == len(list(texts)), "German answers must be unique"
    print("ok")

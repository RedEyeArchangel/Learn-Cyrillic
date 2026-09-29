# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# Copyright (c) 2026 RedEyeArchangel
"""Load, validate and save progress."""
import json
from pathlib import Path

from cyrillic.questions import CARDS


SAVE_FILE = Path.home() / ".local/share/learn-cyrillic/progress.json"
OLD_SAVE_FILE = Path.home() / ".local/share/kyrillisch/progress.json"  # before the English version
OLD_LEVELS = {"Leicht": "Easy", "Mittel": "Medium", "Schwer": "Hard"}


def normalize(data):
    """Validate progress and fill in missing parts. ValueError for a broken or foreign file."""
    if not isinstance(data, dict):
        raise ValueError("not a progress file")
    for old, new in OLD_LEVELS.items():  # German level names from older versions
        if old in data and new not in data:
            data[new] = data.pop(old)
    if data and not (set(CARDS) | {"stats"}) & set(data):  # oldest format: letters only
        data = {"Easy": data}
    for lv in CARDS:
        data.setdefault(lv, {})
    st = data.setdefault("stats", {})
    if not isinstance(st, dict):
        raise ValueError("invalid learning data")
    done = st.pop("done", 0)  # older versions only counted Easy
    for k, v in (("hist", {}), ("conf", {}), ("rounds", {"Easy": done}), ("plan", []), ("lookup", {}), ("exams", {})):
        st.setdefault(k, v)
    ints = lambda xs: all(isinstance(x, int) for x in xs)
    dicts = lambda *xs: all(isinstance(x, dict) for x in xs)
    ok = (dicts(*(data[lv] for lv in CARDS), st["hist"], st["conf"], st["lookup"], st["rounds"], st["exams"])
          and all(dicts(p) and ints([p.get("streak"), p.get("wrong")]) for lv in CARDS for p in data[lv].values())
          and all(isinstance(h, list) and ints(h) for h in st["hist"].values())
          and all(dicts(c) and ints(c.values()) for c in st["conf"].values())
          and ints([done, *st["rounds"].values(), *st["lookup"].values(), *st["exams"].values()])
          and isinstance(st["plan"], list)
          and all(isinstance(k, str) for k in st["plan"]))
    if not ok:
        raise ValueError("invalid progress file")
    for lv in CARDS:
        st["rounds"].setdefault(lv, 0)
        st["exams"].setdefault(lv, 0)  # passed exams per level
    return data


def load_progress():
    for path in (SAVE_FILE, OLD_SAVE_FILE):  # old path only until the first save to the new one
        try:
            return normalize(json.loads(path.read_text()))
        except (OSError, ValueError):
            pass
    return normalize({})


def save_progress(progress):
    SAVE_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = SAVE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(progress))
    tmp.replace(SAVE_FILE)  # atomic, no half-written file on a crash

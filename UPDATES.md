# Updates

## 2026-09-29
- Changed: README screenshots retaken for the current version; added screenshots of the "How it works" view and the Settings tab.
- Changed: error-proneness chart redesigned as rows: mistakes to the right, right-answer bonus to the left, a dot at the real score, ★ for study-plan letters and ✓ for letters out of the plan.
- Fixed: German part names in the error-proneness breakdown keep their capital letters.
- Added: "How it works" view in Learning data explaining cards, weights, study plan and exam (numbers taken from the code).
- Changed: the study plan updates itself after every answer; the "Create study plan" button is gone.
- Added: right answers in a row lower a letter's weight (−0.1 each).
- Added: "forgot again" weight (+0.3) for a mistake after 4 right answers in a row.

## 2026-09-28
- Fixed: a level that was already fully learned when loaded now also counts as completed and starts again from zero.
- Added: `GIT-COMMANDS.md` with the common git commands (commit, push, tag, pull, undo, conflicts).
- Added: README "Run" section (activate the venv, start with `./learn_cyrillic.py`).
- Changed: README describes the Settings tab, German version and completed rounds.
- Fixed: English щ pronunciation is "sh" (long, soft), not "shch"; transliteration stays "shch".
- Fixed: README merge conflict (kept the full README).
- Added: completion counter per level in the status bar; a fully learned level counts +1 and starts again from zero.
- Fixed: German щ pronunciation is "sch" (long, soft), not "schtsch".
- Changed: export, import and reset buttons moved to the Settings tab; one reset button per level.
- Added: Settings tab with language and voice selection (saved between starts).
- Added: German version of the whole app.

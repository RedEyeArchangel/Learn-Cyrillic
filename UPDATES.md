# Updates

## 2026-09-30
- Changed: Medium introduces cognates (музей, метро, банк …) first, so reading a word already gives its meaning.
- Added: an example sentence for every Medium word, shown after answering and in the hint.
- Added: Medium question type "What does the word you hear mean?".
- Changed: "Listen again" sits next to the question; with the hint open the feedback shows only "Correct!"/"Wrong" and the hint has at most 6 lines, so the answer buttons always stay visible.
- Changed: in free practice a wrong answer waits for a "Next" button instead of moving on after 3.5 s, so the hint can be read; opening the hint also stops the timer.
- Added: "Hint" button behind the word in free practice – explains how the word is written and why (letter by letter or word by word, false friends, soft/hard sign, е/ё/й rules) with a 🔊 button to hear it.
- Changed: "How it works" explains the Learn buttons (levels, listen only, study plan, free practice, exam), the status bar and how to read the error-proneness chart.
- Removed: emojis from buttons and texts; only the congratulations (🎉) and the voice test in Settings (🔊) keep theirs.
- Changed: Learn tab top row redesigned – "Listen only", "Study plan" and "Free practice" are toggle buttons in the same style as the levels, shorter labels, the exam button is blue when it can be started; the exam line shows the allowed mistakes.
- Added: "Free practice" checkbox in Learn – quiz any level without recording progress, learning data or completed rounds.
- Added: passed exams are counted per level and shown in the status bar (also saved in export/import).

## 2026-09-29
- Fixed: "How it works" scrolls (scrollbar + mouse wheel) when the text is taller than the window; the exam section was cut off.
- Changed: README – repository links filled in, releases link, study-plan text and screenshots updated.
- Changed: an empty study plan (all letters at 0 or below) now says so instead of "No study plan yet".
- Changed: gentler scoring – a mistake halves the right-answer bonus instead of deleting it, "wrongly pressed" weighs 0.1 (was 0.2) and "forgot again" 0.2 (was 0.3); the part is now called "Right answers".
- Changed: the error-proneness chart shows all 33 letters (two columns when space is short; letters without data show "–"); the title wraps in narrow windows.
- Fixed: the four answer buttons keep the same size on every level and question type (full width, letter height).
- Changed: after a level was completed 3 times it stays learned instead of starting from zero again; only the reset button in Settings clears it.
- Changed: the exam of a level unlocks only after the level was completed 3 times and the study plan has at most 1 letter; the button shows what is still missing.
- Changed: the study plan holds exactly the letters with a score above 0 (no fixed size, no mix-up partners that are already learned); a new mistake brings a letter back.
- Added: GitHub Actions workflow that creates a release automatically when a `v*` tag is pushed (tag message = release notes).
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

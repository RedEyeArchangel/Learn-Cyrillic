# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# Copyright (c) 2026 RedEyeArchangel
"""UI language: the English text is the key, DE holds the German version.

The language is read once at start (the cards are built at import), switching restarts the app.
"""
from cyrillic.settings import SETTINGS


LANGUAGES = {"en": "English", "de": "Deutsch"}
LANG = SETTINGS.get("lang", "en")


def _(text):
    return DE.get(text, text) if LANG == "de" else text


DE = {
    # --- main window ---
    "Learn Cyrillic": "Kyrillisch lernen",
    "Alphabet": "Alphabet",
    "Learn": "Lernen",
    "Learning data": "Lerndaten",
    "Reference": "Nachschlagen",
    "Settings": "Einstellungen",
    "Reset": "Zurücksetzen",
    "Export": "Exportieren",
    "Import": "Importieren",
    "{} learned: {}/{}": "{} gelernt: {}/{}",
    "Completed: {}": "Geschafft: {}",
    "Export progress": "Fortschritt exportieren",
    "Exported: {}": "Exportiert: {}",
    "Import progress": "Fortschritt importieren",
    "Cannot read the file:\n{}": "Die Datei kann nicht gelesen werden:\n{}",
    "Replace your current progress and all learning data with this file?":
        "Aktuellen Fortschritt und alle Lerndaten durch diese Datei ersetzen?",
    "Imported: {}": "Importiert: {}",
    "Delete progress for “{} · {}”?": "Fortschritt für „{} · {}“ löschen?",
    "No speech output: 'spd-say' missing (sudo apt install speech-dispatcher espeak-ng)":
        "Keine Sprachausgabe: 'spd-say' fehlt (sudo apt install speech-dispatcher espeak-ng)",
    # --- settings ---
    "Language": "Sprache",
    "Voice": "Stimme",
    "Progress": "Fortschritt",
    "🔊 Test": "🔊 Testen",
    "Basic voice (espeak). Better voice: start with .venv/bin/python":
        "Einfache Stimme (espeak). Bessere Stimme: mit .venv/bin/python starten",
    "Restart now to switch the language?": "Jetzt neu starten, um die Sprache zu wechseln?",
    # --- levels, status ---
    "Easy": "Leicht", "Medium": "Mittel", "Hard": "Schwer",
    "Letters": "Buchstaben", "Words": "Wörter", "Sentences": "Sätze",
    "new": "neu", "wrong": "falsch", "in progress": "in Arbeit", "learned": "gelernt",
    # --- alphabet ---
    "🔊 Letter": "🔊 Buchstabe",
    "🔊 Word": "🔊 Wort",
    "Status: {}  ·  Streak {}/{}  ·  Total mistakes {}": "Status: {}  ·  Serie {}/{}  ·  Fehler gesamt {}",
    # --- learn ---
    "Listen only": "Nur hören",
    "🔊 Listen again": "🔊 Nochmal hören",
    "Cancel exam": "Prüfung abbrechen",
    "Exam ({} questions, max. {} mistakes)": "Prüfung ({} Fragen, max. {} Fehler)",
    "Study plan": "Lernplan",
    "Study plan (after {}× Easy, {}/{})": "Lernplan (nach {}× Leicht, {}/{})",
    "Study plan (no weak letters)": "Lernplan (keine schwachen Buchstaben)",
    "Exam · question {}/{} · mistakes {}": "Prüfung · Frage {}/{} · Fehler {}",
    "Correct!  ·  {}": "Richtig!  ·  {}",
    "Wrong — {}": "Falsch — {}",
    "Well done! 🎉": "Geschafft! 🎉",
    "Level {}: all {} {} learned": "Stufe {}: alle {} {} gelernt",
    "Exam": "Prüfung",
    "Passed! 🎉": "Bestanden! 🎉",
    "Not passed.": "Nicht bestanden.",
    "{} mistakes (allowed: {})": "{} Fehler (erlaubt: {})",
    "Which sound?": "Welcher Laut?",
    "Which letter makes this sound?": "Welcher Buchstabe klingt so?",
    "How do you read this?": "Wie liest man das?",
    "How do you write this?": "Wie schreibt man das?",
    "What does this mean?": "Was bedeutet das?",
    "How do you say this in Russian?": "Wie sagt man das auf Russisch?",
    "Which letter is missing?": "Welcher Buchstabe fehlt?",
    "Which word is missing?": "Welches Wort fehlt?",
    "What do you hear?": "Was hörst du?",
    # --- reference ---
    "Letter": "Buchstabe",
    "Pronunciation / function": "Aussprache / Funktion",
    "Example": "Beispiel",
    "Group {}": "Gruppe {}",
    "Click a row to hear the example word": "Zeile anklicken, um das Beispielwort zu hören",
    # --- learning data ---
    "Letters in the chart (click)": "Buchstaben im Diagramm (anklicken)",
    "Show all": "Alle zeigen",
    "Hide all": "Alle ausblenden",
    "Confusions": "Verwechslungen",
    "correct → chosen": "richtig → gewählt",
    "Count": "Anzahl",
    "Reset learning data": "Lerndaten zurücksetzen",
    "Learning curves": "Lernkurven",
    "Error proneness": "Fehleranfälligkeit",
    "Easy fully learned: {}× ({})": "Leicht komplett gelernt: {}× ({})",
    "study plan unlocked": "Lernplan freigeschaltet",
    "{}× needed": "{}× nötig",
    "Looked up: ": "Nachgeschlagen: ",
    "Your study plan: {}\n(Reasons: “Error proneness”, hover a bar)":
        "Dein Lernplan: {}\n(Gründe: „Fehleranfälligkeit“, Maus über einen Balken)",
    "No study plan yet.\n": "Noch kein Lernplan.\n",
    "Delete learning curves, confusions, lookups and the study plan?\n(“Easy fully learned” is kept.)":
        "Lernkurven, Verwechslungen, Nachschlagen und Lernplan löschen?\n(„Leicht komplett gelernt“ bleibt.)",
    "Error proneness · ● score  ★ in the study plan  ✓ out of the plan":
        "Fehleranfälligkeit · ● Wert  ★ im Lernplan  ✓ raus aus dem Lernplan",
    "Mistakes ▶": "Fehler ▶",
    "◀ Bonus": "◀ Bonus",
    "+{} more": "+{} weitere",
    "No data yet": "Noch keine Daten",
    "Learning curve · hit rate (average of the last 5 attempts)":
        "Lernkurve · Trefferquote (Mittel der letzten 5 Versuche)",
    "Attempt": "Versuch",
    "No data yet – pick letters or practice on “Easy”": "Noch keine Daten – Buchstaben wählen oder auf „Leicht“ üben",
    "Error rate (last 10)": "Fehlerquote (letzte 10)",
    "Confused": "Verwechselt",
    "Wrongly pressed": "Falsch gedrückt",
    "Looked up": "Nachgeschlagen",
    "Forgot again": "Wieder vergessen",
    "Right in a row": "Richtig in Folge",
    "How it works": "So funktioniert’s",
    "Learning a card": "Eine Karte lernen",
    "Answer a card right {} times in a row and it is learned (green); a mistake sets it back to 0 (red). "
    "At most {} cards are in progress at once, new ones come in order of difficulty. The next card is "
    "drawn at random, weighted: red {}, yellow/new {}, green {}. Learned cards come back for review "
    "with a {:.0%} chance. When a whole level is learned it counts +1 and starts again from zero.":
        "Beantworte eine Karte {}-mal in Folge richtig, dann ist sie gelernt (grün); ein Fehler setzt sie auf 0 "
        "zurück (rot). Höchstens {} Karten sind gleichzeitig in Arbeit, neue kommen nach Schwierigkeit dazu. Die "
        "nächste Karte wird zufällig gezogen, gewichtet: rot {}, gelb/neu {}, grün {}. Gelernte Karten kommen mit "
        "{:.0%} Wahrscheinlichkeit zur Wiederholung. Ist eine ganze Stufe gelernt, zählt sie +1 und beginnt "
        "wieder bei null.",
    "Only questions whose answer is a single letter count. Score per letter:\n• error rate of the "
    "last 10 answers (0–1)\n• +{} per confusion (asked, another letter chosen)\n• +{} per wrongly pressed "
    "(chosen, but another letter was right)\n• +{} per look-up in the Reference\n• +{} per “forgot again” "
    "(a mistake after {} right in a row)\n• {} per right answer in the current run\nA mistake ends the "
    "run and its bonus.":
        "Es zählen nur Fragen, deren Antwort ein einzelner Buchstabe ist. Wert pro Buchstabe:\n• Fehlerquote der "
        "letzten 10 Antworten (0–1)\n• +{} pro Verwechslung (gefragt, anderer Buchstabe gewählt)\n• +{} pro falsch "
        "gedrückt (gewählt, aber ein anderer war richtig)\n• +{} pro Nachschlagen im Tab „Nachschlagen“\n• +{} pro "
        "„wieder vergessen“ (ein Fehler nach {} richtigen in Folge)\n• {} pro richtiger Antwort in der aktuellen "
        "Serie\nEin Fehler beendet die Serie und ihren Bonus.",
    "Unlocked after completing Easy {} times, then rebuilt after every answer: the letters with a "
    "score above 0, weakest first, each with the two letters you mix it up with most, about 8 in "
    "total. With the plan on, Easy asks only these letters, Medium and Hard only words that contain "
    "one, and the wrong options are your own confusions.":
        "Freigeschaltet nach {}× Leicht komplett, danach nach jeder Antwort neu erstellt: die Buchstaben mit "
        "einem Wert über 0, die schwächsten zuerst, jeweils mit den zwei Buchstaben, die du am häufigsten damit "
        "verwechselst, etwa 8 insgesamt. Mit Lernplan fragt Leicht nur diese Buchstaben, Mittel und Schwer nur "
        "Wörter, die einen davon enthalten, und die falschen Antworten sind deine eigenen Verwechslungen.",
    "{} random questions of the level, passed with at most {} mistakes.":
        "{} zufällige Fragen der Stufe, bestanden mit höchstens {} Fehlern.",
    "error rate {:.0%} ({:.2f})": "Fehlerquote {:.0%} ({:.2f})",
    # --- letter groups ---
    "Same look, same sound": "Gleiches Aussehen, gleicher Laut",
    "“False friends” (familiar look, different sound) – ⚠ most common source of mistakes":
        "„Falsche Freunde“ (bekanntes Aussehen, anderer Laut) – ⚠ häufigste Fehlerquelle",
    "New look, familiar sound": "Neues Aussehen, bekannter Laut",
    "New sounds and letter combinations (zh, sh, ch, ts, ya …)": "Neue Laute und Lautverbindungen (sch, tsch, z, ja …)",
    "The two signs without a sound of their own": "Die zwei Zeichen ohne eigenen Laut",
    # --- pronunciation (Alphabet/Reference, must stay unique) ---
    "v": "w wie in „Wasser“",
    "g as in 'go'": "g wie in „gut“",
    "ye (after consonants: e with softening)": "je (nach Konsonanten: e mit Erweichung)",
    "yo (always stressed)": "jo (immer betont)",
    "voiced zh as in 'measure'": "stimmhaftes sch wie in „Journal“",
    "z as in 'zoo'": "stimmhaftes s wie in „Sonne“",
    "ee as in 'see'": "i wie in „Igel“",
    "short y as in 'boy'": "kurzes j wie in „Mai“",
    "l (mostly dark, at the back of the mouth)": "l (meist dunkel, hinten im Mund)",
    "o (stressed)": "o (betont)",
    "rolled r (tip of the tongue)": "gerolltes r (Zungenspitze)",
    "s as in 'sun'": "stimmloses s wie in „Haus“",
    "oo as in 'boot'": "u wie in „Hut“",
    "kh as in Scottish 'loch'": "ch wie in „Bach“",
    "ts as in 'cats'": "z wie in „Zahn“",
    "ch as in 'church'": "tsch wie in „Matsch“",
    "sh (hard)": "sch (hart)",
    "long, soft sh": "langes, weiches sch",
    "hard sign: separates a consonant from the following vowel; rare":
        "Hartes Zeichen: trennt einen Konsonanten vom folgenden Vokal; selten",
    "dull i, with the tongue pulled back": "dumpfes i, Zunge zurückgezogen",
    "soft sign: softens (palatalizes) the preceding consonant":
        "Weiches Zeichen: erweicht (palatalisiert) den vorigen Konsonanten",
    "open e as in 'bet'": "offenes e wie in „Bett“",
    "yu as in 'you'": "ju wie in „Jugend“",
    "ya as in 'yard'": "ja wie in „Jacke“",
    # --- sounds in the quiz (must stay unique) ---
    "e – open": "e – offen",
    "i – dull (y)": "i – dumpf (y)",
    "i – bright, softening": "i – hell, erweichend",
    "ya": "ja", "ye": "je", "yo – always stressed": "jo – immer betont", "yu": "ju", "y – short": "j – kurz",
    "b – voiced": "b – stimmhaft", "p – voiceless": "p – stimmlos",
    "v – voiced": "w – stimmhaft", "f – voiceless": "f – stimmlos",
    "g – voiced": "g – stimmhaft", "k – voiceless": "k – stimmlos",
    "d – voiced": "d – stimmhaft", "t – voiceless": "t – stimmlos",
    "z – voiced": "s – stimmhaft", "s – voiceless": "s – stimmlos",
    "zh – voiced, hard": "sch – stimmhaft, hart", "sh – voiceless, hard": "sch – stimmlos, hart",
    "sh – voiceless, soft, long": "sch – stimmlos, weich, lang",
    "ch – voiceless, soft": "tsch – stimmlos, weich", "ts – voiceless, hard": "z – stimmlos, hart",
    "kh – voiceless, rough": "ch – stimmlos, rau",
    "r – rolled": "r – gerollt",
    "no sound – softens": "kein Laut – erweicht", "no sound – separates (hard)": "kein Laut – trennt (hart)",
    # --- meanings (letters, words) ---
    "Mom": "Mama", "Dad": "Papa", "here is": "da ist", "year": "Jahr", "house": "Haus", "no": "nein",
    "fir tree": "Tanne", "beetle": "Käfer", "hall": "Saal", "and": "und", "my": "mein", "tomcat": "Kater",
    "lamp": "Lampe", "poppy": "Mohn", "nose": "Nase", "who": "wer", "mouth": "Mund", "juice": "Saft",
    "there": "dort", "morning": "Morgen", "photo": "Foto", "choir": "Chor", "center": "Zentrum", "tea": "Tee",
    "school": "Schule", "borscht": "Borschtsch", "object": "Objekt", "we": "wir", "mother": "Mutter",
    "this is": "das ist", "south": "Süden", "I": "ich", "bank": "Bank", "atom": "Atom", "bread": "Brot",
    "water": "Wasser", "milk": "Milch", "meat": "Fleisch", "fish": "Fisch", "soup": "Suppe", "cheese": "Käse",
    "city": "Stadt", "street": "Straße", "park": "Park", "theater": "Theater", "museum": "Museum",
    "subway": "U-Bahn", "taxi": "Taxi", "car": "Auto", "bus": "Bus", "train": "Zug", "coffee": "Kaffee",
    "book": "Buch", "table": "Tisch", "chair": "Stuhl", "window": "Fenster", "door": "Tür", "friend": "Freund",
    "brother": "Bruder", "sister": "Schwester", "son": "Sohn", "daughter": "Tochter", "dog": "Hund",
    "bird": "Vogel", "sun": "Sonne", "sky": "Himmel", "sea": "Meer", "forest": "Wald", "winter": "Winter",
    "summer": "Sommer", "night": "Nacht", "day": "Tag", "pike": "Hecht", "thank you": "danke", "hi": "hallo",
    "yes": "ja", "apple": "Apfel", "cup": "Tasse", "magazine": "Zeitschrift",
    "entrance (of a building)": "Hauseingang", "good": "gut", "big": "groß", "small": "klein",
    # --- sentences ---
    "This is my house.": "Das ist mein Haus.",
    "I love tea.": "Ich liebe Tee.",
    "What's your name?": "Wie heißt du?",
    "My name is Anna.": "Ich heiße Anna.",
    "Where is the subway?": "Wo ist die U-Bahn?",
    "I don't know.": "Ich weiß nicht.",
    "Thanks, everything is fine.": "Danke, alles gut.",
    "We live in Moscow.": "Wir wohnen in Moskau.",
    "The cat is sleeping on the sofa.": "Die Katze schläft auf dem Sofa.",
    "It's cold today.": "Heute ist es kalt.",
    "I have a dog.": "Ich habe einen Hund.",
    "He is reading a book.": "Er liest ein Buch.",
    "She drinks coffee.": "Sie trinkt Kaffee.",
    "Where is the restroom?": "Wo ist hier die Toilette?",
    "I speak English.": "Ich spreche Englisch.",
    "Do you speak Russian?": "Sprichst du Russisch?",
    "How much does this cost?": "Wie viel kostet das?",
    "Good morning!": "Guten Morgen!",
    "Good evening!": "Guten Abend!",
    "Good night!": "Gute Nacht!",
    "How are you?": "Wie geht's?",
    "My brother lives in Berlin.": "Mein Bruder wohnt in Berlin.",
    "This is very interesting.": "Das ist sehr interessant.",
    "I'm thirsty.": "Ich habe Durst.",
    "The train goes to the center.": "Der Zug fährt ins Zentrum.",
    "Mom is cooking borscht.": "Mama kocht Borschtsch.",
    "The children are playing in the park.": "Die Kinder spielen im Park.",
    "I'm learning Russian.": "Ich lerne Russisch.",
    "Where is my phone?": "Wo ist mein Handy?",
    "It snows in winter.": "Im Winter schneit es.",
}

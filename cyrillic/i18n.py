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
    "Exams passed: {}": "Prüfungen bestanden: {}",
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
    "Word": "Wort",
    "Status: {}  ·  Streak {}/{}  ·  Total mistakes {}": "Status: {}  ·  Serie {}/{}  ·  Fehler gesamt {}",
    # --- learn ---
    "Listen only": "Nur hören",
    "Listen again": "Nochmal hören",
    "Cancel exam": "Prüfung abbrechen",
    "Free practice": "Freies Üben",
    "Hint": "Tipp",
    "What does the word you hear mean?": "Was bedeutet das Wort, das du hörst?",
    "Example: {} – {}": "Beispiel: {} – {}",
    "Cognate: once you can read it, you know what it means": "Lehnwort: wer es lesen kann, weiß, was es heißt",
    # example sentences (Medium)
    "Mom is at home.": "Mama ist zu Hause.",
    "Dad is reading.": "Papa liest.",
    "The cat is sleeping.": "Der Kater schläft.",
    "The house is over there.": "Das Haus ist dort.",
    "Who is that?": "Wer ist das?",
    "Yes, that's right.": "Ja, so ist es.",
    "The poppy is red.": "Der Mohn ist rot.",
    "An atom is very small.": "Ein Atom ist sehr klein.",
    "The cat has a black nose.": "Der Kater hat eine schwarze Nase.",
    "Open your mouth.": "Mach den Mund auf.",
    "I drink juice.": "Ich trinke Saft.",
    "The tea is hot.": "Der Tee ist heiß.",
    "The bread is fresh.": "Das Brot ist frisch.",
    "The water is cold.": "Das Wasser ist kalt.",
    "The cat drinks milk.": "Der Kater trinkt Milch.",
    "The meat is on the table.": "Das Fleisch ist auf dem Tisch.",
    "The fish is swimming.": "Der Fisch schwimmt.",
    "The soup is very tasty.": "Die Suppe ist sehr lecker.",
    "I love cheese.": "Ich liebe Käse.",
    "The bank is closed.": "Die Bank ist geschlossen.",
    "This is my photo.": "Das ist mein Foto.",
    "The lamp is on the table.": "Die Lampe ist auf dem Tisch.",
    "The city center is beautiful.": "Das Stadtzentrum ist schön.",
    "The hall is big.": "Der Saal ist groß.",
    "The choir is singing.": "Der Chor singt.",
    "The school is nearby.": "Die Schule ist in der Nähe.",
    "Moscow is a big city.": "Moskau ist eine große Stadt.",
    "The street is long.": "Die Straße ist lang.",
    "The park is green.": "Der Park ist grün.",
    "The theater is in the center.": "Das Theater ist im Zentrum.",
    "The museum is open.": "Das Museum ist geöffnet.",
    "The subway is nearby.": "Die U-Bahn ist in der Nähe.",
    "The taxi is waiting.": "Das Taxi wartet.",
    "The car is new.": "Das Auto ist neu.",
    "The bus goes to the center.": "Der Bus fährt ins Zentrum.",
    "The train goes to Moscow.": "Der Zug fährt nach Moskau.",
    "I drink coffee in the morning.": "Ich trinke morgens Kaffee.",
    "The book is interesting.": "Das Buch ist interessant.",
    "The table is big.": "Der Tisch ist groß.",
    "The chair is by the window.": "Der Stuhl steht am Fenster.",
    "The window is open.": "Das Fenster ist offen.",
    "The door is closed.": "Die Tür ist zu.",
    "He is my friend.": "Er ist mein Freund.",
    "My brother is tall.": "Mein Bruder ist groß.",
    "My sister is at home.": "Meine Schwester ist zu Hause.",
    "The son is playing.": "Der Sohn spielt.",
    "The daughter is reading a book.": "Die Tochter liest ein Buch.",
    "The dog is barking.": "Der Hund bellt.",
    "The bird is singing.": "Der Vogel singt.",
    "The sun is shining.": "Die Sonne scheint.",
    "The sky is blue.": "Der Himmel ist blau.",
    "The sea is warm.": "Das Meer ist warm.",
    "The forest is dark.": "Der Wald ist dunkel.",
    "Winter is cold.": "Der Winter ist kalt.",
    "Summer is warm.": "Der Sommer ist warm.",
    "The night is dark.": "Die Nacht ist dunkel.",
    "Good afternoon!": "Guten Tag!",
    "New Year is coming soon.": "Bald ist Neujahr.",
    "The beetle is small.": "Der Käfer ist klein.",
    "The fir tree is green.": "Die Tanne ist grün.",
    "The south of Russia is warm.": "Der Süden Russlands ist warm.",
    "My mother is a doctor.": "Meine Mutter ist Ärztin.",
    "This is a new object.": "Das ist ein neues Objekt.",
    "A pike is a fish.": "Ein Hecht ist ein Fisch.",
    "The borscht is very tasty.": "Der Borschtsch ist sehr lecker.",
    "Thanks for the tea!": "Danke für den Tee!",
    "Hi, how are you?": "Hallo, wie geht's?",
    "Yes, I'm at home.": "Ja, ich bin zu Hause.",
    "No, thank you.": "Nein, danke.",
    "The apple is red.": "Der Apfel ist rot.",
    "The cup is on the table.": "Die Tasse ist auf dem Tisch.",
    "I'm reading a magazine.": "Ich lese eine Zeitschrift.",
    "We are waiting at the entrance.": "Wir warten am Hauseingang.",
    "Everything is fine.": "Alles ist gut.",
    "This is a big house.": "Das ist ein großes Haus.",
    "This is a small cat.": "Das ist ein kleiner Kater.",
    "Next": "Weiter",
    "name “{}”": "Name „{}“",
    "Example: {} = {} ({})": "Beispiel: {} = {} ({})",
    "{}: looks like Latin “{}”, but is “{}”": "{}: sieht aus wie lateinisches „{}“, ist aber „{}“",
    "е: at the start of a word or after a vowel “ye”, after a consonant “e” and it softens the consonant":
        "е: am Wortanfang oder nach einem Vokal „ye“ (gesprochen je), nach einem Konsonanten „e“ und macht ihn weich",
    "ё: “yo”, always stressed – the two dots are often left out in normal texts":
        "ё: „yo“ (gesprochen jo), immer betont – die zwei Punkte werden in normalen Texten oft weggelassen",
    "й: short “y”, glides after a vowel (like the y in “boy”)":
        "й: kurzes „y“ (wie das i in „Mai“), gleitet nach einem Vokal",
    "ь (soft sign): no sound of its own, softens the consonant before it":
        "ь (Weichheitszeichen): kein eigener Laut, macht den Konsonanten davor weich",
    "ъ (hard sign): no sound of its own, separates the consonant from the next vowel":
        "ъ (Härtezeichen): kein eigener Laut, trennt den Konsonanten vom folgenden Vokal",
    "ы: dull i, tongue pulled back – not the same as и":
        "ы: dumpfes i, Zunge nach hinten gezogen – nicht dasselbe wie и",
    "Free practice · nothing is counted": "Freies Üben · nichts wird gezählt",
    "Exam · not in free practice": "Prüfung · nicht beim freien Üben",
    "Start exam · {} questions": "Prüfung starten · {} Fragen",
    "Exam · from {}× {} ({}/{})": "Prüfung · ab {}× {} ({}/{})",
    "Exam · study plan {} letters (max. {})": "Prüfung · Lernplan {} Buchstaben (max. {})",
    "Study plan": "Lernplan",
    "Study plan · {}": "Lernplan · {}",
    "Study plan · {}/{}× Easy": "Lernplan · {}/{}× Leicht",
    "Study plan · empty": "Lernplan · leer",
    "Exam · question {}/{} · mistakes {} (max. {})": "Prüfung · Frage {}/{} · Fehler {} (max. {})",
    "Correct!  ·  {}": "Richtig!  ·  {}",
    "Wrong — {}": "Falsch — {}",
    "Correct!": "Richtig!",
    "Wrong": "Falsch",
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
    "Study plan empty: no letter is above 0 – well done!\n":
        "Lernplan leer: kein Buchstabe liegt über 0 – gut gemacht!\n",
    "Delete learning curves, confusions, lookups and the study plan?\n(“Easy fully learned” is kept.)":
        "Lernkurven, Verwechslungen, Nachschlagen und Lernplan löschen?\n(„Leicht komplett gelernt“ bleibt.)",
    "Error proneness · ● score  ★ in the study plan  ✓ out of the plan":
        "Fehleranfälligkeit · ● Wert  ★ im Lernplan  ✓ raus aus dem Lernplan",
    "Mistakes ▶": "Fehler ▶",
    "◀ Bonus": "◀ Bonus",
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
    "Right answers": "Richtige Antworten",
    "How it works": "So funktioniert’s",
    "Learning a card": "Eine Karte lernen",
    "Buttons in Learn": "Knöpfe in Lernen",
    "• Levels: Easy (letters), Medium (words), Hard (sentences).\n• Listen only (Medium and Hard): only “what do "
    "you hear?” questions.\n• Study plan: asks only your weak letters. The button shows how many letters are in "
    "the plan, “empty”, or how far you are from unlocking it.\n• Free practice: quiz any level without counting "
    "anything – no progress, no learning data, no completed rounds, no exam."
    " “Hint” behind the word explains how it is written and why, 🔊 plays it. After a "
    "mistake it waits for “Next”.\n• Exam: blue when it can be started,"
    " otherwise it shows what is still missing.\nThe status bar at the bottom shows the learned cards of the "
    "level, the completed rounds and the passed exams per level.":
        "• Stufen: Leicht (Buchstaben), Mittel (Wörter), Schwer (Sätze).\n• Nur hören (Mittel und Schwer): nur "
        "„Was hörst du?“-Fragen.\n• Lernplan: fragt nur deine schwachen Buchstaben ab. Der Knopf zeigt, wie viele "
        "Buchstaben im Lernplan sind, „leer“ oder wie weit du von der Freischaltung entfernt bist.\n• Freies Üben:"
        " jede Stufe abfragen, ohne etwas zu zählen – kein Fortschritt, keine Lerndaten, keine geschafften "
        "Runden, keine Prüfung. „Tipp“ hinter dem Wort erklärt, wie es geschrieben wird und warum, 🔊 spielt es "
        "ab. Nach einem Fehler wartet es auf „Weiter“.\n• Prüfung: blau, wenn sie gestartet werden kann, "
        "sonst steht dort, was noch "
        "fehlt.\nDie Statusleiste unten zeigt die gelernten Karten der Stufe, die geschafften Runden und die "
        "bestandenen Prüfungen pro Stufe.",
    "Answer a card right {} times in a row and it is learned (green); a mistake sets it back to 0 (red). At most "
    "{} cards are in progress at once, new ones come in order of difficulty. The next card is drawn at random, "
    "weighted: red {}, yellow/new {}, green {}. Learned cards come back for review with a {:.0%} chance. When a "
    "whole level is learned it counts +1 and starts again from zero – the first {} times. After that it stays "
    "learned (until you reset it in Settings), and you keep working on your weak letters. "
    "Words (Medium): cognates like музей or метро come first – reading them gives you the meaning. After "
    "every answer you see the word in a short example sentence, and “what does the word you hear mean?” "
    "trains the meaning by ear.":
        "Beantworte eine Karte {}-mal in Folge richtig, dann ist sie gelernt (grün); ein Fehler setzt sie auf 0 "
        "zurück (rot). Höchstens {} Karten sind gleichzeitig in Arbeit, neue kommen nach Schwierigkeit dazu. Die "
        "nächste Karte wird zufällig gezogen, gewichtet: rot {}, gelb/neu {}, grün {}. Gelernte Karten kommen mit"
        " {:.0%} Wahrscheinlichkeit zur Wiederholung. Ist eine ganze Stufe gelernt, zählt sie +1 und beginnt "
        "wieder bei null – die ersten {}-mal. Danach bleibt sie gelernt (bis du sie in den Einstellungen "
        "zurücksetzt), und du arbeitest weiter an deinen schwachen Buchstaben. Wörter (Mittel): Lehnwörter wie "
        "музей oder метро kommen zuerst – wer sie lesen kann, weiß, was sie heißen. Nach jeder Antwort siehst du "
        "das Wort in einem kurzen Beispielsatz, und „Was bedeutet das Wort, das du hörst?“ übt die Bedeutung "
        "übers Hören.",
    "Only questions whose answer is a single letter count. Score per letter:\n• error rate of the "
    "last 10 answers (0–1)\n• +{} per confusion (asked, another letter chosen)\n• +{} per wrongly pressed "
    "(chosen, but another letter was right)\n• +{} per look-up in the Reference\n• +{} per “forgot again” "
    "(a mistake after {} right in a row)\n• {} per right answer\nA mistake halves the right-answer bonus "
    "instead of deleting it."
    "\nIn the chart: mistakes grow to the right, the right-answer bonus to the left, the dot is the score. ★ = in "
    "the study plan, ✓ = dropped out of the plan.":
        "Es zählen nur Fragen, deren Antwort ein einzelner Buchstabe ist. Wert pro Buchstabe:\n• Fehlerquote der "
        "letzten 10 Antworten (0–1)\n• +{} pro Verwechslung (gefragt, anderer Buchstabe gewählt)\n• +{} pro falsch "
        "gedrückt (gewählt, aber ein anderer war richtig)\n• +{} pro Nachschlagen im Tab „Nachschlagen“\n• +{} pro "
        "„wieder vergessen“ (ein Fehler nach {} richtigen in Folge)\n• {} pro richtiger Antwort\nEin Fehler "
        "halbiert den Bonus für richtige Antworten, statt ihn zu löschen."
        "\nIm Diagramm: Fehler wachsen nach rechts, der Bonus für richtige Antworten nach links, der Punkt ist der"
        " Wert. ★ = im Lernplan, ✓ = raus aus dem Lernplan.",
    "Unlocked after completing Easy {} times, then rebuilt after every answer: the letters with a score above 0, "
    "weakest first – as many as there are. Once right answers push a letter to 0 or below it drops out; when "
    "mistakes push it above 0 again, it comes back. An empty plan means no letter is weak. With the plan on, Easy"
    " asks only these letters, Medium and Hard only words that contain one, and the wrong options are your own "
    "confusions.":
        "Freigeschaltet nach {}× Leicht komplett, danach nach jeder Antwort neu erstellt: die Buchstaben mit "
        "einem Wert über 0, die schwächsten zuerst – so viele, wie es gibt. Drücken richtige Antworten einen "
        "Buchstaben auf 0 oder darunter, fällt er raus; drücken Fehler ihn wieder über 0, kommt er zurück. Ein "
        "leerer Lernplan heißt: kein Buchstabe ist schwach. Mit Lernplan fragt Leicht nur diese Buchstaben, "
        "Mittel und Schwer nur Wörter, die einen davon enthalten, und die falschen Antworten sind deine eigenen "
        "Verwechslungen.",
    "One exam per level: {} random questions, passed with at most {} mistakes. Unlocked once "
    "the level was completed {} times and the study plan has at most {} letter. Passed "
    "exams are counted in the status bar.":
        "Eine Prüfung pro Stufe: {} zufällige Fragen, bestanden mit höchstens {} Fehlern. Freigeschaltet, "
        "sobald die Stufe {}-mal geschafft ist und der Lernplan höchstens {} Buchstaben hat. Bestandene Prüfungen "
        "werden unten in der Statusleiste gezählt.",
    "error rate {:.0%} ({:.2f})": "Fehlerquote {:.0%} ({:.2f})",
    # --- letter groups ---
    "Same look, same sound": "Gleiches Aussehen, gleicher Laut",
    "“False friends” (familiar look, different sound) – most common source of mistakes":
        "„Falsche Freunde“ (bekanntes Aussehen, anderer Laut) – häufigste Fehlerquelle",
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

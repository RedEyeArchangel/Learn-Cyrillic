# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# Copyright (c) 2026 RedEyeArchangel
"""Alphabet, words, sentences and sound lists (pure data)."""
from cyrillic.i18n import _


# (upper, lower, name, pronunciation, example word, translation, group)
LETTERS = [
    ("А", "а", "а", "a", "мама", "Mom", 1),
    ("Б", "б", "бэ", "b", "банк", "bank", 3),
    ("В", "в", "вэ", "v", "вот", "here is", 2),
    ("Г", "г", "гэ", "g as in 'go'", "год", "year", 3),
    ("Д", "д", "дэ", "d", "дом", "house", 3),
    ("Е", "е", "е", "ye (after consonants: e with softening)", "нет", "no", 2),
    ("Ё", "ё", "ё", "yo (always stressed)", "ёлка", "fir tree", 4),
    ("Ж", "ж", "жэ", "voiced zh as in 'measure'", "жук", "beetle", 4),
    ("З", "з", "зэ", "z as in 'zoo'", "зал", "hall", 3),
    ("И", "и", "и", "ee as in 'see'", "и", "and", 3),
    ("Й", "й", "и краткое", "short y as in 'boy'", "мой", "my", 4),
    ("К", "к", "ка", "k", "кот", "tomcat", 1),
    ("Л", "л", "эль", "l (mostly dark, at the back of the mouth)", "лампа", "lamp", 3),
    ("М", "м", "эм", "m", "мак", "poppy", 1),
    ("Н", "н", "эн", "n", "нос", "nose", 2),
    ("О", "о", "о", "o (stressed)", "кто", "who", 1),
    ("П", "п", "пэ", "p", "папа", "Dad", 3),
    ("Р", "р", "эр", "rolled r (tip of the tongue)", "рот", "mouth", 2),
    ("С", "с", "эс", "s as in 'sun'", "сок", "juice", 2),
    ("Т", "т", "тэ", "t", "там", "there", 1),
    ("У", "у", "у", "oo as in 'boot'", "утро", "morning", 2),
    ("Ф", "ф", "эф", "f", "фото", "photo", 3),
    ("Х", "х", "ха", "kh as in Scottish 'loch'", "хор", "choir", 2),
    ("Ц", "ц", "цэ", "ts as in 'cats'", "центр", "center", 4),
    ("Ч", "ч", "чэ", "ch as in 'church'", "чай", "tea", 4),
    ("Ш", "ш", "ша", "sh (hard)", "школа", "school", 4),
    ("Щ", "щ", "ща", "long, soft sh", "борщ", "borscht", 4),
    ("Ъ", "ъ", "твёрдый знак", "hard sign: separates a consonant from the following vowel; rare", "объект", "object", 5),
    ("Ы", "ы", "ы", "dull i, with the tongue pulled back", "мы", "we", 4),
    ("Ь", "ь", "мягкий знак", "soft sign: softens (palatalizes) the preceding consonant", "мать", "mother", 5),
    ("Э", "э", "э", "open e as in 'bet'", "это", "this is", 3),
    ("Ю", "ю", "ю", "yu as in 'you'", "юг", "south", 4),
    ("Я", "я", "я", "ya as in 'yard'", "я", "I", 4),
]
LETTERS = [(u, lo, n, _(pr), ex, _(tr), g) for u, lo, n, pr, ex, tr, g in LETTERS]

GROUPS = {
    1: "Same look, same sound",
    2: "“False friends” (familiar look, different sound) – most common source of mistakes",
    3: "New look, familiar sound",
    4: "New sounds and letter combinations (zh, sh, ch, ts, ya …)",
    5: "The two signs without a sound of their own",
}
GROUPS = {g: _(t) for g, t in GROUPS.items()}


# --- Levels: Easy = letters, Medium = words, Hard = sentences ---
WORDS = [
    ("мама", "Mom"), ("папа", "Dad"), ("кот", "tomcat"), ("там", "there"), ("кто", "who"),
    ("так", "so"), ("мак", "poppy"), ("атом", "atom"), ("дом", "house"), ("нос", "nose"),
    ("рот", "mouth"), ("сок", "juice"), ("чай", "tea"), ("хлеб", "bread"), ("вода", "water"),
    ("молоко", "milk"), ("мясо", "meat"), ("рыба", "fish"), ("суп", "soup"), ("сыр", "cheese"),
    ("банк", "bank"), ("фото", "photo"), ("лампа", "lamp"), ("центр", "center"), ("зал", "hall"),
    ("хор", "choir"), ("школа", "school"), ("город", "city"), ("улица", "street"), ("парк", "park"),
    ("театр", "theater"), ("музей", "museum"), ("метро", "subway"), ("такси", "taxi"),
    ("машина", "car"), ("автобус", "bus"), ("поезд", "train"), ("кофе", "coffee"), ("книга", "book"),
    ("стол", "table"), ("стул", "chair"), ("окно", "window"), ("дверь", "door"), ("друг", "friend"),
    ("брат", "brother"), ("сестра", "sister"), ("сын", "son"), ("дочь", "daughter"),
    ("собака", "dog"), ("птица", "bird"), ("солнце", "sun"), ("небо", "sky"), ("море", "sea"),
    ("лес", "forest"), ("зима", "winter"), ("лето", "summer"), ("утро", "morning"), ("ночь", "night"),
    ("день", "day"), ("год", "year"), ("жук", "beetle"), ("ёлка", "fir tree"), ("юг", "south"),
    ("мать", "mother"), ("объект", "object"), ("щука", "pike"), ("борщ", "borscht"),
    ("спасибо", "thank you"), ("привет", "hi"), ("да", "yes"), ("нет", "no"), ("яблоко", "apple"),
    ("чашка", "cup"), ("журнал", "magazine"), ("подъезд", "entrance (of a building)"), ("хорошо", "good"),
    ("большой", "big"), ("маленький", "small"),
]
WORDS = [(ru, _(m)) for ru, m in WORDS]

# Cognates: once you can read them, you know what they mean -> they are introduced first
COGNATES = {"мама", "папа", "атом", "банк", "фото", "лампа", "центр", "хор", "парк", "театр", "музей", "метро",
            "такси", "автобус", "суп", "кофе", "объект", "журнал", "школа", "зал", "борщ"}

# A short example sentence per word (context helps to remember the meaning)
EXAMPLES = {
    "мама": ("Мама дома.", "Mom is at home."),
    "папа": ("Папа читает.", "Dad is reading."),
    "кот": ("Кот спит.", "The cat is sleeping."),
    "там": ("Дом там.", "The house is over there."),
    "кто": ("Кто это?", "Who is that?"),
    "так": ("Да, это так.", "Yes, that's right."),
    "мак": ("Мак красный.", "The poppy is red."),
    "атом": ("Атом очень маленький.", "An atom is very small."),
    "дом": ("Это мой дом.", "This is my house."),
    "нос": ("У кота чёрный нос.", "The cat has a black nose."),
    "рот": ("Открой рот.", "Open your mouth."),
    "сок": ("Я пью сок.", "I drink juice."),
    "чай": ("Чай горячий.", "The tea is hot."),
    "хлеб": ("Хлеб свежий.", "The bread is fresh."),
    "вода": ("Вода холодная.", "The water is cold."),
    "молоко": ("Кот пьёт молоко.", "The cat drinks milk."),
    "мясо": ("Мясо на столе.", "The meat is on the table."),
    "рыба": ("Рыба плавает.", "The fish is swimming."),
    "суп": ("Суп очень вкусный.", "The soup is very tasty."),
    "сыр": ("Я люблю сыр.", "I love cheese."),
    "банк": ("Банк закрыт.", "The bank is closed."),
    "фото": ("Это моё фото.", "This is my photo."),
    "лампа": ("Лампа на столе.", "The lamp is on the table."),
    "центр": ("Центр города красивый.", "The city center is beautiful."),
    "зал": ("Зал большой.", "The hall is big."),
    "хор": ("Хор поёт.", "The choir is singing."),
    "школа": ("Школа рядом.", "The school is nearby."),
    "город": ("Москва — большой город.", "Moscow is a big city."),
    "улица": ("Улица длинная.", "The street is long."),
    "парк": ("Парк зелёный.", "The park is green."),
    "театр": ("Театр в центре.", "The theater is in the center."),
    "музей": ("Музей открыт.", "The museum is open."),
    "метро": ("Метро рядом.", "The subway is nearby."),
    "такси": ("Такси ждёт.", "The taxi is waiting."),
    "машина": ("Машина новая.", "The car is new."),
    "автобус": ("Автобус идёт в центр.", "The bus goes to the center."),
    "поезд": ("Поезд идёт в Москву.", "The train goes to Moscow."),
    "кофе": ("Я пью кофе утром.", "I drink coffee in the morning."),
    "книга": ("Книга интересная.", "The book is interesting."),
    "стол": ("Стол большой.", "The table is big."),
    "стул": ("Стул у окна.", "The chair is by the window."),
    "окно": ("Окно открыто.", "The window is open."),
    "дверь": ("Дверь закрыта.", "The door is closed."),
    "друг": ("Он мой друг.", "He is my friend."),
    "брат": ("Мой брат высокий.", "My brother is tall."),
    "сестра": ("Моя сестра дома.", "My sister is at home."),
    "сын": ("Сын играет.", "The son is playing."),
    "дочь": ("Дочь читает книгу.", "The daughter is reading a book."),
    "собака": ("Собака лает.", "The dog is barking."),
    "птица": ("Птица поёт.", "The bird is singing."),
    "солнце": ("Солнце светит.", "The sun is shining."),
    "небо": ("Небо голубое.", "The sky is blue."),
    "море": ("Море тёплое.", "The sea is warm."),
    "лес": ("Лес тёмный.", "The forest is dark."),
    "зима": ("Зима холодная.", "Winter is cold."),
    "лето": ("Лето тёплое.", "Summer is warm."),
    "утро": ("Доброе утро!", "Good morning!"),
    "ночь": ("Ночь тёмная.", "The night is dark."),
    "день": ("Добрый день!", "Good afternoon!"),
    "год": ("Скоро Новый год.", "New Year is coming soon."),
    "жук": ("Жук маленький.", "The beetle is small."),
    "ёлка": ("Ёлка зелёная.", "The fir tree is green."),
    "юг": ("Юг России тёплый.", "The south of Russia is warm."),
    "мать": ("Моя мать — врач.", "My mother is a doctor."),
    "объект": ("Это новый объект.", "This is a new object."),
    "щука": ("Щука — это рыба.", "A pike is a fish."),
    "борщ": ("Борщ очень вкусный.", "The borscht is very tasty."),
    "спасибо": ("Спасибо за чай!", "Thanks for the tea!"),
    "привет": ("Привет, как дела?", "Hi, how are you?"),
    "да": ("Да, я дома.", "Yes, I'm at home."),
    "нет": ("Нет, спасибо.", "No, thank you."),
    "яблоко": ("Яблоко красное.", "The apple is red."),
    "чашка": ("Чашка на столе.", "The cup is on the table."),
    "журнал": ("Я читаю журнал.", "I'm reading a magazine."),
    "подъезд": ("Мы ждём у подъезда.", "We are waiting at the entrance."),
    "хорошо": ("Всё хорошо.", "Everything is fine."),
    "большой": ("Это большой дом.", "This is a big house."),
    "маленький": ("Это маленький кот.", "This is a small cat."),
}
EXAMPLES = {w: (ru, _(tr)) for w, (ru, tr) in EXAMPLES.items()}

SENTENCES = [
    ("Это мой дом.", "This is my house."),
    ("Я люблю чай.", "I love tea."),
    ("Как тебя зовут?", "What's your name?"),
    ("Меня зовут Анна.", "My name is Anna."),
    ("Где метро?", "Where is the subway?"),
    ("Я не знаю.", "I don't know."),
    ("Спасибо, всё хорошо.", "Thanks, everything is fine."),
    ("Мы живём в Москве.", "We live in Moscow."),
    ("Кот спит на диване.", "The cat is sleeping on the sofa."),
    ("Сегодня холодно.", "It's cold today."),
    ("У меня есть собака.", "I have a dog."),
    ("Он читает книгу.", "He is reading a book."),
    ("Она пьёт кофе.", "She drinks coffee."),
    ("Где здесь туалет?", "Where is the restroom?"),
    ("Я говорю по-английски.", "I speak English."),
    ("Ты говоришь по-русски?", "Do you speak Russian?"),
    ("Сколько это стоит?", "How much does this cost?"),
    ("Доброе утро!", "Good morning!"),
    ("Добрый вечер!", "Good evening!"),
    ("Спокойной ночи!", "Good night!"),
    ("Как дела?", "How are you?"),
    ("Мой брат живёт в Берлине.", "My brother lives in Berlin."),
    ("Это очень интересно.", "This is very interesting."),
    ("Я хочу пить.", "I'm thirsty."),
    ("Поезд идёт в центр.", "The train goes to the center."),
    ("Мама готовит борщ.", "Mom is cooking borscht."),
    ("Дети играют в парке.", "The children are playing in the park."),
    ("Я изучаю русский язык.", "I'm learning Russian."),
    ("Где мой телефон?", "Where is my phone?"),
    ("Зимой идёт снег.", "It snows in winter."),
]
SENTENCES = [(ru, _(m)) for ru, m in SENTENCES]

# Transliteration, simplified English style (close to BGN/PCGN): ж=zh, х=kh, ц=ts, ч=ch, ш=sh, щ=shch
TR = dict(zip("абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
              "a b v g d e yo zh z i y k l m n o p r s t u f kh ts ch sh shch _ y _ e yu ya".split()))
TR["ъ"] = TR["ь"] = ""
VOWELS = "аеёиоуыэюяъь"
# typical misreadings: Latin-looking letters ("false friends") and look-alikes
MISREAD = {"в": "b", "н": "h", "р": "p", "с": "c", "у": "y", "х": "x", "и": "u", "п": "n", "я": "r",
           "ь": "b", "ш": "w", "г": "r", "б": "v", "ц": "ch", "ч": "ts", "щ": "sh", "ы": "i",
           "й": "i", "ё": "e", "э": "ye"}


# Sound for quiz questions: base sound + features (voiced/voiceless, hard/soft), without an example
# word, so you learn the sound and not the example. Must be unique.
SOUND = {
    "А": "a", "О": "o", "У": "u", "Э": "e – open", "Ы": "i – dull (y)", "И": "i – bright, softening",
    "Я": "ya", "Е": "ye", "Ё": "yo – always stressed", "Ю": "yu", "Й": "y – short",
    "Б": "b – voiced", "П": "p – voiceless", "В": "v – voiced", "Ф": "f – voiceless",
    "Г": "g – voiced", "К": "k – voiceless", "Д": "d – voiced", "Т": "t – voiceless",
    "З": "z – voiced", "С": "s – voiceless",
    "Ж": "zh – voiced, hard", "Ш": "sh – voiceless, hard", "Щ": "sh – voiceless, soft, long",
    "Ч": "ch – voiceless, soft", "Ц": "ts – voiceless, hard", "Х": "kh – voiceless, rough",
    "Л": "l", "М": "m", "Н": "n", "Р": "r – rolled",
    "Ь": "no sound – softens", "Ъ": "no sound – separates (hard)",
}
SOUND = {k: _(v) for k, v in SOUND.items()}

# Easily confused letters -> preferred as wrong answers
SIMILAR = ["ШЩЧЦЖ", "БП", "ДТ", "ГК", "ИЙЫ", "ЕЁЭ", "БВР", "ЗС", "ЬЪЫБ", "ЮУЯ", "ПНГТ", "ХЖК", "ЛДП", "ОАЯ", "МТК", "ФВ"]
# Spelling mix-ups for "How do you write this?"
CYR_SWAP = dict("шщ щш цч чц иы ыи йи еэ эе ёе бв вб жш зс сз ьъ ъь юу ую яа ая дт тд пн нп гк кг лм мл хж фв".split())

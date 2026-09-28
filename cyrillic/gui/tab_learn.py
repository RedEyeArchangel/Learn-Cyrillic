# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# Copyright (c) 2026 RedEyeArchangel
"""Tab "Learn": quiz, exam, study plan mode."""
import random
import shutil
import subprocess
import tkinter as tk
from tkinter import font as tkfont, messagebox, ttk

from cyrillic.gui.theme import ACCENT, BAD, BG, CARD, FG, HOVER, MUTED, OK, STATUS_TXT, flat_button
from cyrillic.i18n import LANG, _
from cyrillic.questions import CARDS, LEVEL_TXT, QTYPES, question
from cyrillic.scheduler import EXAM_MAX_WRONG, EXAM_QUESTIONS, MASTER, learned, pick, record, status
from cyrillic.sound import fanfare
from cyrillic.stats import PLAN_UNLOCK, SOUND_KEY, make_plan, partners, plan_cards, record_letter
from cyrillic.storage import save_progress


class LearnTab:
    def build_quiz(self, parent):
        f = ttk.Frame(parent, padding=20, style="Card.TFrame")
        top = ttk.Frame(f, style="Card.TFrame")
        top.pack(fill="x")
        for lv in CARDS:
            ttk.Radiobutton(top, text=f"{_(lv)} · {LEVEL_TXT[lv]}", value=lv, variable=self.level,
                            style="Toolbutton", command=self.change_level).pack(side="left", padx=(0, 4))
        self.listen = tk.BooleanVar()
        self.listen_cb = ttk.Checkbutton(top, text=_("Listen only"), variable=self.listen, style="Card.TCheckbutton",
                                         command=self.next_question)
        self.listen_cb.pack(side="left", padx=16)
        self.use_plan = tk.BooleanVar()
        self.plan_cb = ttk.Checkbutton(top, variable=self.use_plan, style="Card.TCheckbutton",
                                       command=self.next_question)
        self.plan_cb.pack(side="left")
        ttk.Style().configure("Card.TCheckbutton", background=CARD)
        ttk.Style().map("Card.TCheckbutton", background=[("active", CARD)])
        self.exam_btn = ttk.Button(top, command=self.toggle_exam)
        self.exam_btn.pack(side="right")
        self.mode_lbl = ttk.Label(f, style="Card.TLabel", foreground=MUTED, font=("Sans", 13))
        self.mode_lbl.pack(pady=(10, 0))
        self.exam = None

        self.q_lbl = ttk.Label(f, style="Card.TLabel", wraplength=900, justify="center")
        self.q_lbl.pack(pady=5, expand=True)
        self.replay = ttk.Button(f, text=_("🔊 Listen again"), command=lambda: self.say(self.card.say))
        self.feedback = ttk.Label(f, font=("Sans", 16), style="Card.TLabel", wraplength=900, justify="center")
        self.feedback.pack()
        f.bind("<Configure>", lambda e: [w.config(wraplength=e.width - 80) for w in (self.q_lbl, self.feedback)])
        opt_frame = ttk.Frame(f, style="Card.TFrame")
        opt_frame.pack(pady=15)
        self.opt_btns = []
        for i in range(4):
            b = flat_button(opt_frame, width=30, wraplength=380, pady=12, bg=HOVER, activebackground=ACCENT)
            b.grid(row=i // 2, column=i % 2, padx=6, pady=6)
            self.opt_btns.append(b)
        self.update_exam_btn()
        self.update_plan_cb()
        self.listen_cb.state(["disabled"])  # starts on Easy: listening only from Medium on
        return f

    def update_exam_btn(self):
        n = min(EXAM_QUESTIONS, len(CARDS[self.level.get()]))
        self.exam_btn.config(text=_("Cancel exam") if self.exam else
                             _("Exam ({} questions, max. {} mistakes)").format(n, EXAM_MAX_WRONG))

    def update_plan_cb(self):
        """Rebuild the study plan from the current learning data (after every answer) and update the checkbox."""
        done = self.stats["rounds"]["Easy"]
        if done >= PLAN_UNLOCK:
            self.stats["plan"] = make_plan(self.stats)
        ok = done >= PLAN_UNLOCK and self.stats["plan"]
        self.plan_cb.config(text=_("Study plan") if ok else
                            _("Study plan (after {}× Easy, {}/{})").format(PLAN_UNLOCK, min(done, PLAN_UNLOCK),
                                                                           PLAN_UNLOCK)
                            if done < PLAN_UNLOCK else _("Study plan (no weak letters)"))
        self.plan_cb.state(["!disabled"] if ok else ["disabled"])
        if not ok:
            self.use_plan.set(False)

    def change_level(self):
        self.exam = None
        self.listen_cb.state(["disabled"] if self.level.get() == "Easy" else ["!disabled"])
        self.update_exam_btn()
        self.refresh()
        self.next_question()

    def toggle_exam(self):
        cards = CARDS[self.level.get()]
        self.exam = None if self.exam else {"queue": random.sample(cards, min(EXAM_QUESTIONS, len(cards))), "wrong": 0}
        if self.exam:
            self.exam["total"] = len(self.exam["queue"])
        self.update_exam_btn()
        self.next_question()

    def next_question(self):
        lv = self.level.get()
        prog = self.progress[lv]
        if self.exam:
            if not self.exam["queue"]:
                return self.finish_exam()
            self.card = self.exam["queue"].pop()
            done = self.exam["total"] - len(self.exam["queue"])
            info = _("Exam · question {}/{} · mistakes {}").format(done, self.exam["total"], self.exam["wrong"])
        else:
            last = self.card.key if hasattr(self, "card") else None
            plan = self.use_plan.get()
            self.card = pick(prog, plan_cards(self.stats["plan"], lv) if plan else CARDS[lv], last)
            s = min(prog.get(self.card.key, {"streak": 0})["streak"], MASTER)
            info = f"{STATUS_TXT[status(prog.get(self.card.key))]} {'●' * s}{'○' * (MASTER - s)}"
            info += "  ·  " + _("Study plan") if plan else ""
        qtypes = QTYPES[lv]
        if self.listen.get() and lv != "Easy":
            self.qtype, title = qtypes[-1]
        else:  # never the same question type twice in a row
            self.qtype, title = random.choice([q for q in qtypes if q[0] != getattr(self, "qtype", None)])
        self.mode_lbl.config(text=f"{title}     {info}")
        self.answered = False
        self.feedback.config(text="")
        confused = partners(self.stats, self.card.key) if self.use_plan.get() else ()
        prompt, opts, self.right = question(self.card, lv, self.qtype, confused=confused)
        big = self.qtype in ("sound", "read", "meaning")  # Cyrillic text as the question
        size = {"Easy": 100 if big else 48, "Medium": 60 if big else 44, "Hard": 34 if big else 28}[lv]
        self.q_lbl.config(text=prompt, font=("Sans", size))
        if self.qtype == "listen":
            self.replay.pack(before=self.feedback)
            self.say(self.card.say)
        else:
            self.replay.pack_forget()
        if self.qtype in ("letter", "spell"):
            size = 28  # single letters
        elif self.qtype in ("wordgap", "meaning"):
            size = 20
        else:
            size = {"Easy": 18, "Medium": 20, "Hard": 15}[lv]
        self.opts = {}
        for b, o in zip(self.opt_btns, opts):
            b.config(text=o, bg=HOVER, font=("Sans", size), command=lambda o=o, b=b: self.choose(o, b))
            self.opts[o] = b

    def choose(self, o, b):
        if self.answered:
            return
        self.answered = True
        c, lv = self.card, self.level.get()
        correct = o == self.right
        record(self.progress[lv], c.key, correct)
        if self.qtype in ("sound", "letter", "spell"):  # answers that are clearly a single letter
            key = {"sound": SOUND_KEY.get, "letter": lambda x: x[0], "spell": str.upper}[self.qtype]
            record_letter(self.stats, key(self.right), key(o))
        # no "was it full before?" check: a level saved full by an older version must reset too
        if learned(self.progress[lv], CARDS[lv]) == len(CARDS[lv]):
            self.after(900, lambda: self.celebrate(lv))
            self.stats["rounds"][lv] += 1
            self.progress[lv].clear()  # level done -> count it and start again from zero
        self.update_plan_cb()
        save_progress(self.progress)
        self.opts[self.right].config(bg=OK)
        detail = c.info if lv == "Easy" else f"{c.show}  =  {c.answer}  ·  {c.meaning}"
        if correct:
            self.feedback.config(text=_("Correct!  ·  {}").format(detail), foreground=OK)
        else:
            b.config(bg=BAD)
            self.feedback.config(text=_("Wrong — {}").format(detail), foreground=BAD)
            if self.exam:
                self.exam["wrong"] += 1
        reveal = {"listen": c.show, "spell": c.show, "wordgap": c.show}
        if self.qtype in reveal:
            self.q_lbl.config(text=reveal[self.qtype])
        self.say(c.say)
        self.refresh()
        extra = 1500 if lv == "Hard" else 0
        self.after((1500 if correct else 3500) + extra, self.next_question)

    def celebrate(self, lv):
        """Confetti over the whole window + fanfare. Click to close."""
        if shutil.which("paplay"):
            subprocess.Popen(["paplay", fanfare(f"{self.tmp}/fanfare.wav")])
        cv = tk.Canvas(self, bg=BG, highlightthickness=0)
        cv.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.update_idletasks()
        w, h = cv.winfo_width(), cv.winfo_height()
        px = tkfont.Font(family="Sans", size=10).metrics("linespace") / 14  # scale like the font (HiDPI)
        cv.create_text(w / 2, h / 2, anchor="s", text=_("Well done! 🎉"), fill=FG, font=("Sans", 60, "bold"))
        cv.create_text(w / 2, h / 2 + 10 * px, anchor="n", fill=MUTED, font=("Sans", 22),
                       text=_("Level {}: all {} {} learned").format(  # German nouns stay capitalized
                           _(lv), len(CARDS[lv]), LEVEL_TXT[lv] if LANG == "de" else LEVEL_TXT[lv].lower()))
        colors = [ACCENT, OK, "#f2cc60", "#ff7b72", "#d2a8ff", "#56d4dd"]
        bits = []  # ponytail: 120 rectangles, enough for the effect and cheap
        for _n in range(120):
            x, y, s = random.uniform(0, w), random.uniform(-h * .4, 0), random.uniform(6, 12) * px
            bits.append((cv.create_rectangle(x, y, x + s, y + s * .6, fill=random.choice(colors), width=0),
                         random.uniform(-1, 1) * px, random.uniform(3, 6) * px))

        def step():
            if cv.winfo_exists():
                for item, dx, dy in bits:
                    cv.move(item, dx, dy)
                self.after(30, step)

        self.after(4500, lambda: cv.winfo_exists() and cv.destroy())

        cv.bind("<Button-1>", lambda e: cv.destroy())
        step()

    def finish_exam(self):
        wrong = self.exam["wrong"]
        passed = wrong <= EXAM_MAX_WRONG
        self.toggle_exam()
        messagebox.showinfo(_("Exam"), (_("Passed! 🎉") if passed else _("Not passed.")) + "\n" +
                            _("{} mistakes (allowed: {})").format(wrong, EXAM_MAX_WRONG))

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
from cyrillic.data import EXAMPLES
from cyrillic.questions import CARDS, LEVEL_TXT, QTYPES, hint, question
from cyrillic.scheduler import (EXAM_MAX_PLAN, EXAM_MAX_WRONG, EXAM_QUESTIONS, EXAM_UNLOCK, MASTER, complete_level,
                                pick, record, status)
from cyrillic.sound import fanfare
from cyrillic.stats import PLAN_UNLOCK, SOUND_KEY, make_plan, partners, plan_cards, record_letter
from cyrillic.storage import save_progress


LISTEN = ("listen", "hearmeaning")  # question types that play the audio


class LearnTab:
    def build_quiz(self, parent):
        f = ttk.Frame(parent, padding=20, style="Card.TFrame")
        top = ttk.Frame(f, style="Card.TFrame")
        top.pack(fill="x")
        # one row, three groups: level (segmented) · mode toggles · exam
        for lv in CARDS:
            ttk.Radiobutton(top, text=f"{_(lv)} · {LEVEL_TXT[lv]}", value=lv, variable=self.level,
                            style="Toolbutton", command=self.change_level).pack(side="left", padx=(0, 2))
        ttk.Frame(top, style="Card.TFrame", width=24).pack(side="left")  # gap between the groups
        toggle = lambda text, var, cmd: ttk.Checkbutton(top, text=text, variable=var, style="Toolbutton",
                                                        command=cmd, cursor="hand2")
        self.listen, self.use_plan = tk.BooleanVar(), tk.BooleanVar()
        self.listen_cb = toggle(_("Listen only"), self.listen, self.next_question)
        self.plan_cb = toggle("", self.use_plan, self.next_question)
        # free practice: quiz any level without recording anything (no progress, learning data or rounds)
        self.free = tk.BooleanVar()
        self.free_cb = toggle(_("Free practice"), self.free, lambda: (self.update_exam_btn(), self.next_question()))
        for w in (self.listen_cb, self.plan_cb, self.free_cb):
            w.pack(side="left", padx=(0, 2))
        self.exam_btn = ttk.Button(top, command=self.toggle_exam, cursor="hand2")
        self.exam_btn.pack(side="right")
        self.mode_lbl = ttk.Label(f, style="Card.TLabel", foreground=MUTED, font=("Sans", 13))
        self.mode_lbl.pack(pady=(10, 0))
        self.exam = None

        q_row = ttk.Frame(f, style="Card.TFrame")  # the question, in free practice with a hint button behind it
        q_row.pack(pady=5, expand=True)
        self.q_lbl = ttk.Label(q_row, style="Card.TLabel", wraplength=900, justify="center")
        self.q_lbl.pack(side="left")
        self.hint_btn = ttk.Button(q_row, text=_("Hint"), style="Toolbutton", command=self.toggle_hint, cursor="hand2")
        # free practice: after a mistake (or with the hint open) you go on yourself
        self.next_btn = ttk.Button(q_row, text=_("Next"), style="Accent.TButton", command=self.next_question,
                                   cursor="hand2")
        self.advance = None  # pending automatic next question
        self.hint_box = ttk.Frame(f, style="Card.TFrame")  # play the right word + explanation
        ttk.Button(self.hint_box, text="🔊", style="Toolbutton", cursor="hand2",
                   command=lambda: self.say(self.card.say)).pack(side="left", padx=(0, 12), anchor="n")
        self.hint_lbl = ttk.Label(self.hint_box, style="Card.TLabel", justify="left", font=("Sans", 12))
        self.hint_lbl.pack(side="left")
        self.replay = ttk.Button(q_row, text=_("Listen again"), style="Toolbutton", cursor="hand2",
                                 command=lambda: self.say(self.card.say))
        self.feedback = ttk.Label(f, font=("Sans", 16), style="Card.TLabel", wraplength=900, justify="center")
        self.feedback.pack()
        f.bind("<Configure>", lambda e: (self.q_lbl.config(wraplength=e.width - 200), self.feedback.config(
            wraplength=e.width - 80), self.hint_lbl.config(wraplength=e.width - 200)))
        # fixed cells, so the buttons keep the same size for every level and question type:
        # full width, as high as a letter button (28 pt)
        opt_frame = ttk.Frame(f, style="Card.TFrame")
        opt_frame.pack(pady=15, fill="x")
        row_h = tkfont.Font(family="Sans", size=28).metrics("linespace") + 2 * 12 + 20
        for i in range(2):
            opt_frame.columnconfigure(i, weight=1, uniform="opt")
            opt_frame.rowconfigure(i, minsize=row_h, uniform="opt")
        self.opt_btns = []
        for i in range(4):
            b = flat_button(opt_frame, width=1, pady=12, bg=HOVER, activebackground=ACCENT)
            b.grid(row=i // 2, column=i % 2, padx=6, pady=6, sticky="nsew")
            b.bind("<Configure>", lambda e: e.widget.config(wraplength=e.width - 30))
            self.opt_btns.append(b)
        self.update_exam_btn()
        self.update_plan_cb()
        self.listen_cb.state(["disabled"])  # starts on Easy: listening only from Medium on
        return f

    def update_exam_btn(self):
        lv = self.level.get()
        n = min(EXAM_QUESTIONS, len(CARDS[lv]))
        done, plan = self.stats["rounds"][lv], len(self.stats["plan"])
        if self.exam:
            text, ok = _("Cancel exam"), True
        elif self.free.get():
            text, ok = _("Exam · not in free practice"), False
        elif done < EXAM_UNLOCK:
            text, ok = _("Exam · from {}× {} ({}/{})").format(EXAM_UNLOCK, _(lv), done, EXAM_UNLOCK), False
        elif plan > EXAM_MAX_PLAN:
            text, ok = _("Exam · study plan {} letters (max. {})").format(plan, EXAM_MAX_PLAN), False
        else:
            text, ok = _("Start exam · {} questions").format(n), True
        # blue = can be started now
        self.exam_btn.config(text=text, style="Accent.TButton" if ok and not self.exam else "TButton")
        self.exam_btn.state(["!disabled"] if ok else ["disabled"])

    def update_plan_cb(self):
        """Rebuild the study plan from the current learning data (after every answer) and update the checkbox."""
        done = self.stats["rounds"]["Easy"]
        if done >= PLAN_UNLOCK:
            self.stats["plan"] = make_plan(self.stats)
        ok = done >= PLAN_UNLOCK and self.stats["plan"]
        self.plan_cb.config(text=_("Study plan · {}").format(len(self.stats["plan"])) if ok else
                            _("Study plan · {}/{}× Easy").format(min(done, PLAN_UNLOCK), PLAN_UNLOCK)
                            if done < PLAN_UNLOCK else _("Study plan · empty"))
        self.plan_cb.state(["!disabled"] if ok else ["disabled"])
        if not ok:
            self.use_plan.set(False)
        self.update_exam_btn()  # the exam depends on the plan size

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
        self.free_cb.state(["disabled"] if self.exam else ["!disabled"])
        self.update_exam_btn()
        self.next_question()

    def next_question(self):
        if self.advance:  # e.g. "Next" pressed or level changed while the timer was still running
            self.after_cancel(self.advance)
            self.advance = None
        self.next_btn.pack_forget()
        lv = self.level.get()
        prog = self.progress[lv]
        if self.exam:
            if not self.exam["queue"]:
                return self.finish_exam()
            self.card = self.exam["queue"].pop()
            done = self.exam["total"] - len(self.exam["queue"])
            info = _("Exam · question {}/{} · mistakes {} (max. {})").format(
                done, self.exam["total"], self.exam["wrong"], EXAM_MAX_WRONG)
        else:
            last = self.card.key if hasattr(self, "card") else None
            plan = self.use_plan.get()
            cards = plan_cards(self.stats["plan"], lv) if plan else CARDS[lv]
            if self.free.get():  # any card at random, the progress is not used
                self.card = random.choice([c for c in cards if c.key != last] or cards)
                info = _("Free practice · nothing is counted")
            else:
                self.card = pick(prog, cards, last)
                s = min(prog.get(self.card.key, {"streak": 0})["streak"], MASTER)
                info = f"{STATUS_TXT[status(prog.get(self.card.key))]} {'●' * s}{'○' * (MASTER - s)}"
            info += "  ·  " + _("Study plan") if plan else ""
        qtypes = QTYPES[lv]
        if self.listen.get() and lv != "Easy":  # listening types only ("listen", Medium also "hearmeaning")
            self.qtype, title = random.choice([q for q in qtypes if q[0] in LISTEN])
        else:  # never the same question type twice in a row
            self.qtype, title = random.choice([q for q in qtypes if q[0] != getattr(self, "qtype", None)])
        self.mode_lbl.config(text=f"{title}     {info}")
        self.hint_box.pack_forget()
        self.hint_open = False
        # buttons behind the question, in this order: listen again · hint (· next, packed later)
        for w in (self.replay, self.hint_btn):
            w.pack_forget()
        if self.qtype in LISTEN:
            self.replay.pack(side="left", padx=(24, 0))
        if self.free.get() and not self.exam:
            self.hint_btn.pack(side="left", padx=(8 if self.qtype in LISTEN else 24, 0))
        self.answered = False
        self.feedback.config(text="")
        confused = partners(self.stats, self.card.key) if self.use_plan.get() else ()
        prompt, opts, self.right = question(self.card, lv, self.qtype, confused=confused)
        big = self.qtype in ("sound", "read", "meaning")  # Cyrillic text as the question
        size = {"Easy": 100 if big else 48, "Medium": 60 if big else 44, "Hard": 34 if big else 28}[lv]
        self.q_size = size  # the hint shrinks it temporarily
        self.q_lbl.config(text=prompt, font=("Sans", size))
        if self.qtype in LISTEN:
            self.say(self.card.say)
        if self.qtype in ("letter", "spell"):
            size = 28  # single letters
        elif self.qtype in ("wordgap", "meaning", "hearmeaning"):
            size = 20
        else:
            size = {"Easy": 18, "Medium": 20, "Hard": 15}[lv]
        self.opts = {}
        for b, o in zip(self.opt_btns, opts):
            b.config(text=o, bg=HOVER, font=("Sans", size), command=lambda o=o, b=b: self.choose(o, b))
            self.opts[o] = b

    def toggle_hint(self):
        """Show / hide how the current card is written and why (free practice only)."""
        if self.hint_open:  # (winfo_ismapped is only true after a redraw)
            self.hint_open = False
            self.q_lbl.config(font=("Sans", self.q_size))
            if self.answered:
                self.feedback.config(text=self.full_feedback)
            return self.hint_box.pack_forget()
        if self.answered:  # reading the hint after answering: stop the timer, go on with "Next"
            self.wait_for_next()
            self.feedback.config(text=self.verdict)  # the details are in the hint now
        self.q_lbl.config(font=("Sans", int(self.q_size * .6)))  # make room so the answer buttons stay visible
        self.hint_lbl.config(text=hint(self.card, self.level.get()))
        self.hint_box.pack(before=self.feedback, pady=(0, 10))
        self.hint_open = True

    def choose(self, o, b):
        if self.answered:
            return
        self.answered = True
        c, lv = self.card, self.level.get()
        correct = o == self.right
        if not self.free.get():  # free practice records nothing (no exam possible then)
            record(self.progress[lv], c.key, correct)
            if self.qtype in ("sound", "letter", "spell"):  # answers that are clearly a single letter
                key = {"sound": SOUND_KEY.get, "letter": lambda x: x[0], "spell": str.upper}[self.qtype]
                record_letter(self.stats, key(self.right), key(o))
            if complete_level(self.progress[lv], self.stats["rounds"], lv, CARDS[lv]):
                self.after(900, lambda: self.celebrate(lv))
            self.update_plan_cb()
            save_progress(self.progress)
        self.opts[self.right].config(bg=OK)
        detail = c.info if lv == "Easy" else f"{c.show}  =  {c.answer}  ·  {c.meaning}"
        if c.key in EXAMPLES:  # Medium: the word in a short sentence
            detail += "\n{} – {}".format(*EXAMPLES[c.key])
        # full feedback, or only the verdict while the hint is open (it already shows all of it, and space is short)
        self.verdict = _("Correct!") if correct else _("Wrong")
        self.full_feedback = _("Correct!  ·  {}").format(detail) if correct else _("Wrong — {}").format(detail)
        self.feedback.config(text=self.verdict if self.hint_open else self.full_feedback,
                             foreground=OK if correct else BAD)
        if not correct:
            b.config(bg=BAD)
            if self.exam:
                self.exam["wrong"] += 1
        reveal = {"listen": c.show, "hearmeaning": c.show, "spell": c.show, "wordgap": c.show}
        if self.qtype in reveal:
            self.q_lbl.config(text=reveal[self.qtype])
        self.say(c.say)
        self.refresh()
        extra = 1500 if lv == "Hard" else 0
        if self.free.get() and not correct:  # free practice: take your time, open the hint if you want
            self.wait_for_next()
        else:
            self.advance = self.after((1500 if correct else 3500) + extra, self.next_question)

    def wait_for_next(self):
        if self.advance:
            self.after_cancel(self.advance)
            self.advance = None
        self.next_btn.pack(side="left", padx=(8, 0))

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
        if passed:  # counted per level in the status bar
            self.stats["exams"][self.level.get()] += 1
            save_progress(self.progress)
        self.toggle_exam()
        self.refresh()
        messagebox.showinfo(_("Exam"), (_("Passed! 🎉") if passed else _("Not passed.")) + "\n" +
                            _("{} mistakes (allowed: {})").format(wrong, EXAM_MAX_WRONG))

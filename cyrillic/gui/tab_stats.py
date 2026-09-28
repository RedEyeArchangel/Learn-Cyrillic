# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# Copyright (c) 2026 RedEyeArchangel
"""Tab "Learning data": learning curves, error proneness, study plan."""
import math
import tkinter as tk
from tkinter import font as tkfont, messagebox, ttk

from cyrillic.data import LETTERS
from cyrillic.gui.theme import CARD, FG, HOVER, MUTED, OK, SERIES, STYLES, flat_button
from cyrillic.i18n import _
from cyrillic.scheduler import BATCH, EXAM_MAX_WRONG, EXAM_QUESTIONS, MASTER, REVIEW_CHANCE, WEIGHT
from cyrillic.stats import PARTS, PLAN_UNLOCK, RELAPSE, explain, moving, weakness, weakness_parts
from cyrillic.storage import save_progress


class StatsTab:
    def build_stats(self, parent):
        f = ttk.Frame(parent, padding=16, style="Card.TFrame")
        left = ttk.Frame(f, style="Card.TFrame")
        left.pack(side="left", fill="y")
        ttk.Label(left, text=_("Letters in the chart (click)"), style="Card.TLabel",
                  foreground=MUTED).pack(anchor="w")
        grid = ttk.Frame(left, style="Card.TFrame")
        grid.pack(anchor="w", pady=(4, 10))
        self.stat_tiles = {}
        for i, l in enumerate(LETTERS):
            b = flat_button(grid, text=l[0], font=("Sans", 13), width=2, command=lambda k=l[0]: self.toggle_curve(k))
            b.grid(row=i // 8, column=i % 8, padx=2, pady=2)
            self.stat_tiles[l[0]] = b
        # in the free last row below the letters, costs no height
        ttk.Style().configure("Small.TButton", padding=(6, 4))
        row = ttk.Frame(grid, style="Card.TFrame")
        row.grid(row=4, column=1, columnspan=7, sticky="w")
        ttk.Button(row, text=_("Show all"), style="Small.TButton",
                   command=lambda: self.show_curves(LETTERS)).pack(side="left", padx=2)
        ttk.Button(row, text=_("Hide all"), style="Small.TButton",
                   command=lambda: self.show_curves([])).pack(side="left", padx=2)
        ttk.Label(left, text=_("Confusions"), style="Card.TLabel", foreground=MUTED).pack(anchor="w")
        fnt = tkfont.Font(family="Sans", size=11)  # row height from font metrics (HiDPI)
        ttk.Style().configure("Stats.Treeview", font=fnt, rowheight=fnt.metrics("linespace") + 6)
        self.conf_tree = ttk.Treeview(left, style="Stats.Treeview", columns=("n",), height=5)
        self.conf_tree.heading("#0", text=_("correct → chosen"))
        self.conf_tree.heading("n", text=_("Count"))
        self.conf_tree.column("n", width=fnt.measure(_("Count")) + 20, stretch=False, anchor="e")
        self.conf_tree.pack(fill="x", pady=(4, 10))
        self.lookup_lbl = ttk.Label(left, style="Card.TLabel")
        self.lookup_lbl.pack(anchor="w", pady=(0, 6))
        self.done_lbl = ttk.Label(left, style="Card.TLabel")
        self.done_lbl.pack(anchor="w", pady=(0, 6))
        self.plan_lbl = ttk.Label(left, style="Card.TLabel", justify="left", text="\n")  # reserve 2 lines
        self.plan_lbl.pack(anchor="w", fill="x")
        left.bind("<Configure>", lambda e: self.plan_lbl.config(wraplength=e.width))
        right = ttk.Frame(f, style="Card.TFrame")
        right.pack(side="left", fill="both", expand=True, padx=(16, 0))
        views = ttk.Frame(right, style="Card.TFrame")
        views.pack(anchor="w", pady=(0, 8))
        self.view = tk.StringVar(value="curve")
        for v, t in (("curve", _("Learning curves")), ("bars", _("Error proneness")), ("help", _("How it works"))):
            ttk.Radiobutton(views, text=t, value=v, variable=self.view, style="Toolbutton",
                            command=self.draw_chart).pack(side="left", padx=(0, 4))
        self.chart = tk.Canvas(right, bg=CARD, highlightthickness=0, width=560, height=340)
        self.chart.pack(fill="both", expand=True)
        self.chart.bind("<Configure>", lambda e: self.draw_chart())
        return f

    def refresh_stats(self):
        st = self.stats
        if self.preselect:  # preselection: the plan, or the 5 weakest
            self.preselect = False
            pre = st["plan"] or [k for k, _ in weakness(st).most_common(5)]
            for k in [k for k in pre if st["hist"].get(k)][:len(SERIES)]:
                self.toggle_curve(k, draw=False)
        for k, b in self.stat_tiles.items():
            b.config(bg=self.curves[k][0] if k in self.curves else CARD, fg=FG if st["hist"].get(k) else MUTED)
        self.conf_tree.delete(*self.conf_tree.get_children())
        rows = sorted(((n, r, c) for r, d in st["conf"].items() for c, n in d.items()), reverse=True)
        for n, r, c in rows:
            self.conf_tree.insert("", "end", text=f"{r}  →  {c}", values=(n,))
        unlocked = st["rounds"]["Easy"] >= PLAN_UNLOCK
        self.done_lbl.config(text=_("Easy fully learned: {}× ({})").format(
            st["rounds"]["Easy"], _("study plan unlocked") if unlocked else _("{}× needed").format(PLAN_UNLOCK)))
        looked = sorted(st["lookup"].items(), key=lambda x: -x[1])
        self.lookup_lbl.config(text=_("Looked up: ") + (" · ".join(f"{k} {n}×" for k, n in looked[:8]) or "–"))
        plan = " · ".join(st["plan"])  # reasons per letter: "Error proneness" chart
        self.plan_lbl.config(text=_("Your study plan: {}\n(Reasons: “Error proneness”, hover a bar)").format(plan)
                             if plan else _("No study plan yet.\n"))
        self.draw_chart()

    def toggle_curve(self, k, draw=True):
        if k in self.curves:
            del self.curves[k]
        else:
            self.curves[k] = next(c for c in STYLES if c not in self.curves.values())
        if draw:
            self.refresh_stats()

    def show_curves(self, letters):
        """Show/hide all; only letters with data are shown."""
        self.curves.clear()
        for l in letters:
            if self.stats["hist"].get(l[0]):
                self.toggle_curve(l[0], draw=False)
        self.refresh_stats()

    def reset_stats(self):
        if messagebox.askyesno(_("Reset learning data"), _("Delete learning curves, confusions, lookups and the "
                                                           "study plan?\n(“Easy fully learned” is kept.)")):
            for k in ("hist", "conf", "lookup"):
                self.stats[k].clear()
            self.stats["plan"] = []
            save_progress(self.progress)
            self.curves.clear()
            self.preselect = True
            self.update_plan_cb()
            self.refresh_stats()

    def draw_chart(self):
        {"bars": self.draw_bars, "help": self.draw_help}.get(self.view.get(), self.draw_curves)()

    def draw_help(self):
        """How learning works, built from the real constants so it never goes stale."""
        cv, fnt = self.chart, tkfont.Font(family="Sans", size=10)
        cv.delete("all")
        w = [wt for _n, wt in PARTS]
        sections = [
            (_("Learning a card"), _(
                "Answer a card right {} times in a row and it is learned (green); a mistake sets it back to 0 (red). "
                "At most {} cards are in progress at once, new ones come in order of difficulty. The next card is "
                "drawn at random, weighted: red {}, yellow/new {}, green {}. Learned cards come back for review "
                "with a {:.0%} chance. When a whole level is learned it counts +1 and starts again from zero.").format(
                MASTER, BATCH, WEIGHT["red"], WEIGHT["yellow"], WEIGHT["green"], REVIEW_CHANCE)),
            (_("Error proneness"), _(
                "Only questions whose answer is a single letter count. Score per letter:\n• error rate of the "
                "last 10 answers (0–1)\n• +{} per confusion (asked, another letter chosen)\n• +{} per wrongly pressed "
                "(chosen, but another letter was right)\n• +{} per look-up in the Reference\n• +{} per “forgot again” "
                "(a mistake after {} right in a row)\n• {} per right answer in the current run\nA mistake ends the "
                "run and its bonus.").format(w[1], w[2], w[3], w[4], RELAPSE, w[5])),
            (_("Study plan"), _(
                "Unlocked after completing Easy {} times, then rebuilt after every answer: the letters with a "
                "score above 0, weakest first, each with the two letters you mix it up with most, about 8 in "
                "total. With the plan on, Easy asks only these letters, Medium and Hard only words that contain "
                "one, and the wrong options are your own confusions.").format(PLAN_UNLOCK)),
            (_("Exam"), _("{} random questions of the level, passed with at most {} mistakes.").format(
                EXAM_QUESTIONS, EXAM_MAX_WRONG)),
        ]
        y, width = 2, cv.winfo_width() - 8
        for head, body in sections:
            y = cv.bbox(cv.create_text(4, y, anchor="nw", fill=FG, font=("Sans", 12, "bold"), text=head))[3] + 2
            y = cv.bbox(cv.create_text(4, y, anchor="nw", fill=FG, font=fnt, width=width, text=body))[3] + 10

    def draw_bars(self):
        """Error proneness as rows: mistakes to the right of zero, the right-answer bonus to the left,
        a dot at the real score. Hover a row for the breakdown."""
        cv, fnt, bold = self.chart, tkfont.Font(family="Sans", size=10), ("Sans", 11, "bold")
        cv.delete("all")
        w, h, lh = cv.winfo_width(), cv.winfo_height(), fnt.metrics("linespace")
        plan = self.stats["plan"]
        # letters that ever had a mistake; plan letters first (partners can have a low score), then by score
        rows = sorted(((sum(v), k, v) for k, v in weakness_parts(self.stats).items() if any(x > 0 for x in v)),
                      key=lambda r: (r[1] in plan, r[0]), reverse=True)
        cv.create_text(4, 2, anchor="nw", fill=FG, font=("Sans", 12, "bold"),
                       text=_("Error proneness · ● score  ★ in the study plan  ✓ out of the plan"))
        x, y = 4, 2 * lh
        for (name, _wt), col in zip(PARTS, SERIES):  # legend, wraps when out of space
            if x > 4 and x + lh * 1.1 + fnt.measure(name) > w:
                x, y = 4, y + 1.3 * lh
            cv.create_rectangle(x, y, x + lh * .8, y + .8 * lh, fill=col, width=0)
            cv.create_text(x + lh * 1.1, y + .4 * lh, anchor="w", fill=FG, font=fnt, text=name)
            x += lh * 2.5 + fnt.measure(name)
        detail = cv.create_text(4, h - 4, anchor="sw", fill=FG, font=fnt, width=w - 8,
                                text=explain(rows[0][1], rows[0][2]) if rows else "")
        if not rows:
            return cv.create_text(w / 2, h / 2, fill=MUTED, font=("Sans", 13), text=_("No data yet"))
        y0, y1 = y + 3 * lh, h - 3 * lh  # rows area, detail line below
        x0, x1 = 3.5 * lh, w - fnt.measure("-0.00 ✓") - 1.5 * lh
        rh = 1.4 * lh
        fit = max(1, int((y1 - y0) / rh))
        more = len(rows) - fit + 1 if len(rows) > fit else 0
        shown = rows[:fit - 1] if more else rows
        pos = max(sum(x for x in v if x > 0) for _t, _k, v in rows) or 1
        neg = max(-sum(x for x in v if x < 0) for _t, _k, v in rows)
        scale = (x1 - x0) / (pos + neg)
        zx = x0 + neg * scale
        cv.create_text(zx + 6, y0 - lh, anchor="w", fill=MUTED, font=fnt, text=_("Mistakes ▶"))
        if neg:
            cv.create_text(zx - 6, y0 - lh, anchor="e", fill=MUTED, font=fnt, text=_("◀ Bonus"))
        for i, (tot, k, v) in enumerate(shown):
            cy, tag, bar = y0 + rh * (i + .5), f"row{i}", rh * .3
            bg = cv.create_rectangle(0, cy - rh / 2, w, cy + rh / 2, fill=CARD, width=0, tags=tag)
            done = tot <= 0 and k not in plan
            cv.create_text(4, cy, anchor="w", fill=FG, font=bold, text="★" if k in plan else "", tags=tag)
            cv.create_text(1.6 * lh, cy, anchor="w", fill=MUTED if done else FG, font=bold, text=k, tags=tag)
            x = zx
            for val, col in zip(v, SERIES):
                if val > 0:  # 2 px gap between segments via an outline in the background color
                    cv.create_rectangle(x, cy - bar, x + val * scale, cy + bar, fill=col, outline=CARD, width=2,
                                        tags=tag)
                    x += val * scale
                elif val < 0:
                    cv.create_rectangle(zx + val * scale, cy - bar, zx, cy + bar, fill=col, outline=CARD, width=2,
                                        tags=tag)
            dx = zx + tot * scale
            cv.create_oval(dx - .35 * lh, cy - .35 * lh, dx + .35 * lh, cy + .35 * lh, fill=FG, outline=CARD,
                           width=2, tags=tag)
            cv.create_text(x1 + lh, cy, anchor="w", fill=OK if done else FG, font=fnt,
                           text=f"{tot:.2f}" + ("  ✓" if done else ""), tags=tag)
            cv.tag_bind(tag, "<Enter>", lambda e, k=k, v=v, bg=bg: (cv.itemconfig(detail, text=explain(k, v)),
                                                                     cv.itemconfig(bg, fill=HOVER)))
            cv.tag_bind(tag, "<Leave>", lambda e, bg=bg: cv.itemconfig(bg, fill=CARD))
        cv.create_line(zx, y0 - .3 * lh, zx, y0 + rh * len(shown), fill=MUTED)
        if more:
            cv.create_text(1.6 * lh, y0 + rh * (len(shown) + .5), anchor="w", fill=MUTED, font=fnt,
                           text=_("+{} more").format(more))

    def draw_curves(self):
        """Learning curves: moving hit rate (5 attempts) per selected letter."""
        cv, fnt = self.chart, tkfont.Font(family="Sans", size=10)
        cv.delete("all")
        w, h, lh = cv.winfo_width(), cv.winfo_height(), fnt.metrics("linespace")
        series = {k: moving(self.stats["hist"][k]) for k in self.curves if self.stats["hist"].get(k)}
        # legend on the right, alphabetical; several columns with many curves so it fits the height
        cols = max(1, math.ceil(len(series) * 1.2 * lh / max(h - 5 * lh, lh)))
        per_col = math.ceil(len(series) / cols) if series else 1
        x0, x1, y0, y1 = fnt.measure("100%") + 14, w - (1 + 3.5 * cols) * lh, lh, h - 2.5 * lh
        cv.create_text(x0, 2, anchor="nw", fill=FG, font=("Sans", 12, "bold"),
                       text=_("Learning curve · hit rate (average of the last 5 attempts)"))
        y0 += lh
        n = max((len(v) for v in series.values()), default=0)
        X = lambda i: x0 + (x1 - x0) * (i / max(n - 1, 1))
        Y = lambda v: y1 - (y1 - y0) * v
        for v in (0, .5, 1):
            cv.create_line(x0, Y(v), x1, Y(v), fill=HOVER)
            cv.create_text(x0 - 8, Y(v), anchor="e", fill=MUTED, font=fnt, text=f"{v:.0%}")
        for i in sorted({0, (n - 1) // 2, n - 1}) if n else ():
            cv.create_text(X(i), y1 + 6, anchor="n", fill=MUTED, font=fnt, text=i + 1)
        cv.create_text((x0 + x1) / 2, h - 4, anchor="s", fill=MUTED, font=fnt, text=_("Attempt"))
        if not series:
            cv.create_text((x0 + x1) / 2, (y0 + y1) / 2, fill=MUTED, font=("Sans", 13),
                           text=_("No data yet – pick letters or practice on “Easy”"))
        for k, v in series.items():
            pts = [(X(i), Y(y)) for i, y in enumerate(v)]
            if len(pts) > 1:
                col, dash = self.curves[k]
                cv.create_line(*[c for p in pts for c in p], fill=col, width=2, dash=dash)
            ex, ey = pts[-1]
            cv.create_oval(ex - 4, ey - 4, ex + 4, ey + 4, fill=self.curves[k][0], outline=CARD, width=2)
        order = [l[0] for l in LETTERS if l[0] in series]
        for i, k in enumerate(order):
            x = x1 + lh + (i // per_col) * 3.5 * lh
            y = y0 + (i % per_col) * 1.2 * lh
            col, dash = self.curves[k]
            cv.create_line(x, y, x + 1.4 * lh, y, fill=col, width=3, dash=dash)
            cv.create_text(x + 1.7 * lh, y, anchor="w", fill=FG, font=("Sans", 11, "bold"), text=k)

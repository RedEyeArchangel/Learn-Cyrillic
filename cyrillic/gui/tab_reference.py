# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# Copyright (c) 2026 RedEyeArchangel
"""Tab "Reference"."""
from tkinter import font as tkfont, ttk

from cyrillic.data import GROUPS, LETTERS
from cyrillic.gui.theme import CARD, MUTED
from cyrillic.storage import save_progress


class ReferenceTab:
    def build_reference(self, parent):
        f = ttk.Frame(parent, padding=10, style="Card.TFrame")
        fnt = tkfont.Font(family="Sans", size=14)
        bold = tkfont.Font(family="Sans", size=14, weight="bold")
        # row height from font metrics, otherwise clipped with HiDPI scaling
        ttk.Style().configure("Ref.Treeview", font=fnt, rowheight=fnt.metrics("linespace") + 10)
        ttk.Style().configure("Ref.Treeview.Heading", font=bold)
        tree = ttk.Treeview(f, style="Ref.Treeview", columns=("sound", "example"))
        tree.heading("#0", text="Letter")
        tree.heading("sound", text="Pronunciation / function")
        tree.heading("example", text="Example")
        pad = fnt.measure("MMM")  # indentation + expand arrow
        tree.column("#0", width=bold.measure("Group 5") + pad, stretch=False)
        tree.column("sound", width=fnt.measure("x" * 40))
        tree.column("example", width=max(fnt.measure(f"{l[4]} ({l[5]})") for l in LETTERS) + pad, stretch=False)
        rows = {}
        for g, title in GROUPS.items():
            gid = tree.insert("", "end", text=f"Group {g}", values=(title, ""), open=True, tags=("group",))
            for l in LETTERS:
                if l[6] == g:
                    rows[tree.insert(gid, "end", text=f"{l[0]} {l[1]}", values=(l[3], f"{l[4]} ({l[5]})"))] = l
        tree.tag_configure("group", font=bold, background=CARD)
        sb = ttk.Scrollbar(f, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)
        ttk.Label(f, text="Click a row to hear the example word", style="Card.TLabel",
                  foreground=MUTED).pack(anchor="w", pady=(6, 0))
        tree.bind("<<TreeviewSelect>>", lambda e: (l := rows.get(tree.focus())) and self.look_up(l))
        return f

    def look_up(self, l):
        """Looking up counts towards the study plan (uncertainty with this letter)."""
        self.stats["lookup"][l[0]] = self.stats["lookup"].get(l[0], 0) + 1
        save_progress(self.progress)
        self.say(l[4])

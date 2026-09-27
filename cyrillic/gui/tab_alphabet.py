# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# Copyright (c) 2026 RedEyeArchangel
"""Tab "Alphabet"."""
import tkinter as tk
from tkinter import ttk

from cyrillic.data import LETTERS
from cyrillic.gui.theme import MUTED, STATUS_BG, STATUS_TXT, flat_button
from cyrillic.scheduler import MASTER, status


class AlphabetTab:
    def build_alphabet(self, parent):
        f = ttk.Frame(parent, padding=16, style="Card.TFrame")
        left = ttk.Frame(f, style="Card.TFrame")
        left.pack(side="left", fill="y")
        grid = ttk.Frame(left, style="Card.TFrame")
        grid.pack()
        self.tiles = {}
        for i, l in enumerate(LETTERS):
            b = flat_button(grid, text=f"{l[0]}{l[1]}", font=("Sans", 17), width=3, pady=6,
                            command=lambda l=l: self.show(l))
            b.grid(row=i // 6, column=i % 6, padx=3, pady=3)
            self.tiles[l[0]] = b
        legend = ttk.Frame(left, style="Card.TFrame")
        legend.pack(pady=(12, 0), anchor="w")
        for s, txt in STATUS_TXT.items():
            tk.Label(legend, bg=STATUS_BG[s], width=2).pack(side="left", padx=(8, 3))
            ttk.Label(legend, text=txt, style="Card.TLabel").pack(side="left")

        right = ttk.Frame(f, padding=20, style="Card.TFrame")
        right.pack(side="left", fill="both", expand=True)
        self.big = ttk.Label(right, font=("Sans", 110), style="Card.TLabel")
        self.big.pack()
        self.hint = ttk.Label(right, font=("Sans", 17), wraplength=500, justify="center", style="Card.TLabel")
        self.hint.pack(pady=5)
        self.word = ttk.Label(right, font=("Sans", 22), style="Card.TLabel")
        self.word.pack(pady=10)
        self.letter_stat = ttk.Label(right, style="Card.TLabel", foreground=MUTED)
        self.letter_stat.pack()
        btns = ttk.Frame(right, style="Card.TFrame")
        btns.pack(pady=10)
        ttk.Button(btns, text="🔊 Letter", command=lambda: self.say(self.cur[2])).pack(side="left", padx=5)
        ttk.Button(btns, text="🔊 Word", command=lambda: self.say(self.cur[4])).pack(side="left", padx=5)
        return f

    def show(self, l, speak=True):
        self.cur = l
        prog = self.progress["Easy"]
        p = prog.get(l[0], {"streak": 0, "wrong": 0})
        self.big.config(text=f"{l[0]} {l[1]}")
        self.hint.config(text=f"Name: {l[2]}  —  {l[3]}")
        self.word.config(text=f"{l[4]}  =  {l[5]}")
        self.letter_stat.config(text=f"Status: {STATUS_TXT[status(prog.get(l[0]))]}  ·  "
                                     f"Streak {min(p['streak'], MASTER)}/{MASTER}  ·  Total mistakes {p['wrong']}")
        if speak:
            self.say(l[2])

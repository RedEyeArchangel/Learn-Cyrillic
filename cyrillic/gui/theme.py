# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# Copyright (c) 2026 RedEyeArchangel
"""Flat dark theme, only ttk "clam" + colors, no extra packages."""
import tkinter as tk
from tkinter import ttk

from cyrillic.i18n import _


BG, CARD, HOVER, FG, MUTED, ACCENT = "#1b1d22", "#262930", "#323640", "#e8e8ea", "#9197a3", "#4f8cff"
STATUS_BG = {"new": "#323640", "red": "#8e3434", "yellow": "#8a6a1c", "green": "#2e7042"}
STATUS_TXT = {"new": _("new"), "red": _("wrong"), "yellow": _("in progress"), "green": _("learned")}
OK, BAD = "#2ea043", "#da3633"
# Learning curves: fixed color order (dataviz palette, dark steps), a color stays with its letter
SERIES = ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300", "#9085e9", "#e66767"]
# More than 8 curves: same colors, but with dash patterns (color + pattern instead of new hues)
STYLES = [(c, d) for d in ("", (8, 4), (2, 4), (10, 4, 2, 4), (16, 6)) for c in SERIES]


def apply_theme(root):
    root.configure(bg=BG)
    st = ttk.Style(root)
    st.theme_use("clam")
    st.configure(".", background=BG, foreground=FG, fieldbackground=CARD, bordercolor=BG,
                 lightcolor=BG, darkcolor=BG, troughcolor=CARD, font=("Sans", 11))
    st.configure("TNotebook", borderwidth=0, tabmargins=0)
    st.configure("TNotebook.Tab", background=BG, foreground=MUTED, padding=(20, 8), borderwidth=0,
                 bordercolor=BG, lightcolor=BG, darkcolor=BG)
    st.map("TNotebook.Tab", background=[("selected", CARD)], foreground=[("selected", FG)],
           lightcolor=[("selected", CARD)], bordercolor=[("selected", CARD)], expand=[("selected", 0)])
    st.configure("TButton", background=CARD, padding=(14, 6), borderwidth=0, focuscolor=CARD)
    st.map("TButton", background=[("active", HOVER)])
    st.configure("TCheckbutton", indicatorbackground=CARD, indicatorforeground=ACCENT)
    st.map("TCheckbutton", background=[("active", BG)])
    st.configure("Toolbutton", background=HOVER, padding=(14, 6), borderwidth=0)
    st.map("Toolbutton", background=[("selected", ACCENT), ("active", "#3d4250")],
           foreground=[("selected", "white")])
    st.configure("Card.TFrame", background=CARD)
    st.configure("Card.TLabel", background=CARD)
    st.configure("Muted.TLabel", foreground=MUTED)
    st.configure("TProgressbar", background=OK, lightcolor=OK, darkcolor=OK, bordercolor=CARD, thickness=10)
    st.configure("TCombobox", background=CARD, arrowcolor=FG, selectbackground=CARD, selectforeground=FG)
    st.map("TCombobox", fieldbackground=[("readonly", CARD)], foreground=[("readonly", FG)],
           background=[("active", HOVER), ("readonly", CARD)])
    root.option_add("*TCombobox*Listbox.background", CARD)
    root.option_add("*TCombobox*Listbox.foreground", FG)
    st.configure("Treeview", background=BG, fieldbackground=BG, borderwidth=0)
    st.configure("Treeview.Heading", background=CARD, relief="flat")
    st.map("Treeview", background=[("selected", ACCENT)])
    st.map("Treeview.Heading", background=[("active", HOVER)])


def flat_button(parent, **kw):
    kw = {"relief": "flat", "bd": 0, "highlightthickness": 0, "bg": CARD, "fg": FG,
          "activebackground": HOVER, "activeforeground": FG, "cursor": "hand2", **kw}
    return tk.Button(parent, **kw)

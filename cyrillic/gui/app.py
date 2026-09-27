# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# Copyright (c) 2026 RedEyeArchangel
"""Main window: tabs, status bar, export/import, settings, speech output."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import tkinter as tk
import wave
from datetime import date
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from cyrillic.data import LETTERS
from cyrillic.gui.tab_alphabet import AlphabetTab
from cyrillic.gui.tab_learn import LearnTab
from cyrillic.gui.tab_reference import ReferenceTab
from cyrillic.gui.tab_stats import StatsTab
from cyrillic.gui.theme import MUTED, STATUS_BG, apply_theme
from cyrillic import i18n
from cyrillic.i18n import LANGUAGES, _
from cyrillic.questions import CARDS, LEVEL_TXT
from cyrillic.scheduler import status
from cyrillic.settings import SETTINGS, save_settings
from cyrillic.sound import VOICE_DIR, PiperVoice
from cyrillic.storage import load_progress, normalize, save_progress


class App(AlphabetTab, LearnTab, StatsTab, ReferenceTab, tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(_("Learn Cyrillic"))
        apply_theme(self)
        self.progress = load_progress()
        self.stats = self.progress["stats"]
        self.curves = {}  # letter -> (color, dash pattern) in the chart
        self.preselect = True  # on first open, preselect the weakest letters
        self.level = tk.StringVar(value="Easy")
        self.status_msg = tk.StringVar()
        self.voices = sorted(VOICE_DIR.glob("*.onnx")) if PiperVoice else []
        names = [v.stem for v in self.voices]
        self.voice_name = tk.StringVar(value=SETTINGS.get("voice") if SETTINGS.get("voice") in names else
                                       names[0] if names else "")
        self.loaded, self.cache, self.player = {}, {}, None
        self.tmp = tempfile.mkdtemp(prefix="cyr-")

        nb = self.nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=10, pady=(10, 0))
        nb.add(self.build_alphabet(nb), text=_("Alphabet"))
        nb.add(self.build_quiz(nb), text=_("Learn"))
        nb.add(self.build_stats(nb), text=_("Learning data"))
        nb.add(self.build_reference(nb), text=_("Reference"))
        nb.add(self.build_settings(nb), text=_("Settings"))
        nb.bind("<<NotebookTabChanged>>", lambda e: self.refresh_stats())
        self.build_bar()
        self.refresh()
        self.show(LETTERS[0], speak=False)
        self.next_question()
        self.update_idletasks()  # freeze the size, otherwise the window jumps when switching levels
        self.geometry(f"{self.winfo_reqwidth()}x{self.winfo_reqheight()}")

    def build_bar(self):
        bar = ttk.Frame(self, padding=(10, 8))
        bar.pack(fill="x", side="bottom", before=self.nb)  # bar stays visible even if a tab grows
        self.learned_lbl = ttk.Label(bar)
        self.learned_lbl.pack(side="left")
        self.pbar = ttk.Progressbar(bar, length=260)
        self.pbar.pack(side="left", padx=10)
        self.rounds_lbl = ttk.Label(bar, style="Muted.TLabel")
        self.rounds_lbl.pack(side="left")
        ttk.Label(bar, textvariable=self.status_msg, style="Muted.TLabel").pack(side="left", padx=10)

    def build_settings(self, parent):
        f = ttk.Frame(parent, padding=20, style="Card.TFrame")
        ttk.Label(f, text=_("Language"), style="Card.TLabel").grid(row=0, column=0, sticky="w", pady=6)
        self.lang = tk.StringVar(value=LANGUAGES.get(i18n.LANG, "English"))
        lang_box = ttk.Combobox(f, textvariable=self.lang, state="readonly", width=22, values=list(LANGUAGES.values()))
        lang_box.grid(row=0, column=1, sticky="w", padx=12)
        lang_box.bind("<<ComboboxSelected>>", lambda e: self.change_language())
        ttk.Label(f, text=_("Voice"), style="Card.TLabel").grid(row=1, column=0, sticky="w", pady=6)
        row = ttk.Frame(f, style="Card.TFrame")
        row.grid(row=1, column=1, sticky="w", padx=12)
        if self.voices:
            voice_box = ttk.Combobox(row, textvariable=self.voice_name, state="readonly", width=22,
                                     values=[v.stem for v in self.voices])
            voice_box.pack(side="left")
            voice_box.bind("<<ComboboxSelected>>", lambda e: self.change_voice())
        else:
            ttk.Label(row, text=_("Basic voice (espeak). Better voice: start with .venv/bin/python"),
                      style="Card.TLabel", foreground=MUTED).pack(side="left")
        ttk.Button(row, text=_("🔊 Test"), command=lambda: self.say("Привет! Это мой дом.")).pack(side="left", padx=6)
        ttk.Label(f, text=_("Progress"), style="Card.TLabel").grid(row=2, column=0, sticky="w", pady=(18, 6))
        row = ttk.Frame(f, style="Card.TFrame")
        row.grid(row=2, column=1, sticky="w", padx=12, pady=(18, 6))
        ttk.Button(row, text=_("Export"), command=self.export_progress).pack(side="left")
        ttk.Button(row, text=_("Import"), command=self.import_progress).pack(side="left", padx=6)
        ttk.Label(f, text=_("Reset"), style="Card.TLabel").grid(row=3, column=0, sticky="w", pady=6)
        row = ttk.Frame(f, style="Card.TFrame")
        row.grid(row=3, column=1, sticky="w", padx=12)
        for lv in CARDS:
            ttk.Button(row, text=f"{_(lv)} · {LEVEL_TXT[lv]}", command=lambda lv=lv: self.reset(lv)).pack(side="left",
                                                                                                          padx=(0, 6))
        ttk.Button(row, text=_("Learning data"), command=self.reset_stats).pack(side="left")
        return f

    def change_voice(self):
        SETTINGS["voice"] = self.voice_name.get()
        save_settings()
        self.say("Привет! Это мой дом.")

    def change_language(self):
        code = next(k for k, v in LANGUAGES.items() if v == self.lang.get())
        if code == i18n.LANG:
            return
        SETTINGS["lang"] = code
        save_settings()
        # the cards are translated at import, so a restart is the simple way to switch everything
        if messagebox.askyesno(_("Language"), _("Restart now to switch the language?")):
            os.execv(sys.executable, [sys.executable, *sys.argv])

    def refresh(self):
        for l in LETTERS:
            self.tiles[l[0]].config(bg=STATUS_BG[status(self.progress["Easy"].get(l[0]))])
        lv, cards = self.level.get(), CARDS[self.level.get()]
        n = sum(status(self.progress[lv].get(c.key)) == "green" for c in cards)
        self.pbar.config(value=n, maximum=len(cards))
        self.learned_lbl.config(text=_("{} learned: {}/{}").format(LEVEL_TXT[lv], n, len(cards)))
        rounds = self.stats["rounds"]
        self.rounds_lbl.config(text=_("Completed: {}").format(" · ".join(f"{_(lv)} {rounds[lv]}×" for lv in CARDS)))

    def export_progress(self):
        path = filedialog.asksaveasfilename(title=_("Export progress"), defaultextension=".json",
                                            initialfile=f"cyrillic-progress-{date.today()}.json",
                                            filetypes=[("JSON", "*.json")])
        if path:
            Path(path).write_text(json.dumps(self.progress, ensure_ascii=False, indent=1), encoding="utf-8")
            self.status_msg.set(_("Exported: {}").format(Path(path).name))

    def import_progress(self):
        path = filedialog.askopenfilename(title=_("Import progress"), filetypes=[("JSON", "*.json")])
        if not path:
            return
        try:
            data = normalize(json.loads(Path(path).read_text(encoding="utf-8")))
        except (OSError, ValueError) as e:  # JSONDecodeError is a ValueError
            return messagebox.showerror(_("Import"), _("Cannot read the file:\n{}").format(e))
        if not messagebox.askyesno(_("Import"),
                                   _("Replace your current progress and all learning data with this file?")):
            return
        self.progress, self.stats, self.exam = data, data["stats"], None
        save_progress(self.progress)
        self.curves.clear()
        self.preselect = True
        self.update_plan_cb()
        self.update_exam_btn()
        self.refresh()
        self.refresh_stats()
        self.next_question()
        self.status_msg.set(_("Imported: {}").format(Path(path).name))

    def reset(self, lv):
        if messagebox.askyesno(_("Reset"), _("Delete progress for “{} · {}”?").format(_(lv), LEVEL_TXT[lv])):
            self.progress[lv].clear()
            save_progress(self.progress)
            self.refresh()
            self.next_question()

    def say(self, text):
        if self.voices:
            return self.say_piper(text)
        if not shutil.which("spd-say"):
            self.status_msg.set(_("No speech output: 'spd-say' missing (sudo apt install speech-dispatcher espeak-ng)"))
            return
        subprocess.run(["spd-say", "-C"])  # stop the current output
        subprocess.Popen(["spd-say", "-l", "ru", text])

    def say_piper(self, text):
        name = self.voice_name.get()
        key = (name, text)
        if key not in self.cache:  # ponytail: WAVs only in the temp folder, no cleanup needed
            if name not in self.loaded:
                self.loaded[name] = PiperVoice.load(str(VOICE_DIR / f"{name}.onnx"))
            path = f"{self.tmp}/{len(self.cache)}.wav"
            with wave.open(path, "wb") as w:
                self.loaded[name].synthesize_wav(text, w)
            self.cache[key] = path
        if self.player:
            self.player.kill()
        self.player = subprocess.Popen(["paplay", self.cache[key]])

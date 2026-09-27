# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# Copyright (c) 2026 RedEyeArchangel
"""Main window: tabs, status bar, export/import, speech output."""
import json
import shutil
import subprocess
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
from cyrillic.gui.theme import STATUS_BG, apply_theme
from cyrillic.questions import CARDS, LEVEL_TXT
from cyrillic.scheduler import status
from cyrillic.sound import VOICE_DIR, PiperVoice
from cyrillic.storage import load_progress, normalize, save_progress


class App(AlphabetTab, LearnTab, StatsTab, ReferenceTab, tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Learn Cyrillic")
        apply_theme(self)
        self.progress = load_progress()
        self.stats = self.progress["stats"]
        self.curves = {}  # letter -> (color, dash pattern) in the chart
        self.preselect = True  # on first open, preselect the weakest letters
        self.level = tk.StringVar(value="Easy")
        self.status_msg = tk.StringVar()
        self.voices = sorted(VOICE_DIR.glob("*.onnx")) if PiperVoice else []
        self.voice_name = tk.StringVar(value=self.voices[0].stem if self.voices else "")
        self.loaded, self.cache, self.player = {}, {}, None
        self.tmp = tempfile.mkdtemp(prefix="cyr-")

        nb = self.nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=10, pady=(10, 0))
        nb.add(self.build_alphabet(nb), text="Alphabet")
        nb.add(self.build_quiz(nb), text="Learn")
        nb.add(self.build_stats(nb), text="Learning data")
        nb.add(self.build_reference(nb), text="Reference")
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
        ttk.Button(bar, text="Reset", command=self.reset).pack(side="left")
        ttk.Button(bar, text="Export", command=self.export_progress).pack(side="left", padx=(6, 0))
        ttk.Button(bar, text="Import", command=self.import_progress).pack(side="left", padx=(6, 0))
        ttk.Label(bar, textvariable=self.status_msg, style="Muted.TLabel").pack(side="left", padx=10)
        if self.voices:
            ttk.Combobox(bar, textvariable=self.voice_name, state="readonly", width=22,
                         values=[v.stem for v in self.voices]).pack(side="right")
            ttk.Label(bar, text="Voice ", style="Muted.TLabel").pack(side="right")
        else:
            self.status_msg.set("Basic voice (espeak). Better voice: start with .venv/bin/python")

    def refresh(self):
        for l in LETTERS:
            self.tiles[l[0]].config(bg=STATUS_BG[status(self.progress["Easy"].get(l[0]))])
        lv, cards = self.level.get(), CARDS[self.level.get()]
        n = sum(status(self.progress[lv].get(c.key)) == "green" for c in cards)
        self.pbar.config(value=n, maximum=len(cards))
        self.learned_lbl.config(text=f"{LEVEL_TXT[lv]} learned: {n}/{len(cards)}")

    def export_progress(self):
        path = filedialog.asksaveasfilename(title="Export progress", defaultextension=".json",
                                            initialfile=f"cyrillic-progress-{date.today()}.json",
                                            filetypes=[("JSON", "*.json")])
        if path:
            Path(path).write_text(json.dumps(self.progress, ensure_ascii=False, indent=1), encoding="utf-8")
            self.status_msg.set(f"Exported: {Path(path).name}")

    def import_progress(self):
        path = filedialog.askopenfilename(title="Import progress", filetypes=[("JSON", "*.json")])
        if not path:
            return
        try:
            data = normalize(json.loads(Path(path).read_text(encoding="utf-8")))
        except (OSError, ValueError) as e:  # JSONDecodeError is a ValueError
            return messagebox.showerror("Import", f"Cannot read the file:\n{e}")
        if not messagebox.askyesno("Import", "Replace your current progress and all learning data with this file?"):
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
        self.status_msg.set(f"Imported: {Path(path).name}")

    def reset(self):
        lv = self.level.get()
        if messagebox.askyesno("Reset", f"Delete progress for “{lv} · {LEVEL_TXT[lv]}”?"):
            self.progress[lv].clear()
            save_progress(self.progress)
            self.refresh()
            self.next_question()

    def say(self, text):
        if self.voices:
            return self.say_piper(text)
        if not shutil.which("spd-say"):
            self.status_msg.set("No speech output: 'spd-say' missing (sudo apt install speech-dispatcher espeak-ng)")
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

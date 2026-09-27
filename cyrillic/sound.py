# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# Copyright (c) 2026 RedEyeArchangel
"""Voices (Piper) and fanfare."""
import array
import math
import wave
from pathlib import Path


VOICE_DIR = Path(__file__).parent.parent / "voices"
try:
    from piper import PiperVoice  # neural voice, see .venv
except ImportError:
    PiperVoice = None


def fanfare(path, rate=22050):
    """Short victory fanfare (C-E-G-C + chord) as WAV, standard library only."""
    notes = [(523, .12), (659, .12), (784, .12), (1047, .25), (0, .05), ((523, 659, 784, 1047), .9)]
    samples = array.array("h")
    for freq, dur in notes:
        freqs = freq if isinstance(freq, tuple) else (freq,)
        n = int(rate * dur)
        for i in range(n):
            env = math.exp(-3 * i / n)  # fade out
            v = sum(math.sin(2 * math.pi * f * i / rate) for f in freqs if f) / len(freqs)
            samples.append(int(9000 * env * v))
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(samples.tobytes())
    return path
